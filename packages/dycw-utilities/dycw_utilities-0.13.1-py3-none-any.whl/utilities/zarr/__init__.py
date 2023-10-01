from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import Any, Literal, cast

from numpy import array, datetime64, isin, ndarray, prod
from numpy.typing import NDArray
from typing_extensions import override
from zarr import JSON, Array, Group, group
from zarr.convenience import open_group
from zarr.core import Attributes

from utilities.atomicwrites import writer
from utilities.class_name import get_class_name
from utilities.datetime import ensure_date, ensure_datetime
from utilities.iterables import is_iterable_not_str
from utilities.numpy import (
    MultipleTrueElementsError,
    NoTrueElementsError,
    _ffill_non_nan_slices_helper,
    array_indexer,
    datetime64D,
    datetime64ns,
    datetime64Y,
    flatn0,
    get_fill_value,
    has_dtype,
)
from utilities.numpy.typing import NDArray1, NDArrayB1, NDArrayI1
from utilities.pathlib import PathLike
from utilities.re import extract_group
from utilities.sentinel import Sentinel, sentinel


def ffill_non_nan_slices(
    array: Array, /, *, limit: int | None = None, axis: int = -1
) -> None:
    """Forward fill the slices in an array which contain non-nan values."""
    ndim = array.ndim
    arrays = (
        array.oindex[array_indexer(i, ndim, axis=axis)]
        for i in range(array.shape[axis])
    )
    for i, repl_i in _ffill_non_nan_slices_helper(arrays, limit=limit):
        array.oindex[array_indexer(i, ndim, axis=axis)] = repl_i


@contextmanager
def yield_array_with_indexes(
    indexes: Mapping[str, NDArray1],
    path: PathLike,
    /,
    *,
    overwrite: bool = False,
    dtype: Any = float,
    fill_value: Any = sentinel,
    chunks: bool | int | tuple[int | None, ...] = True,
) -> Iterator[Array]:
    """Save an `ndarray` with indexes, yielding a view into its values."""
    with yield_group_and_array(
        indexes,
        path,
        overwrite=overwrite,
        dtype=dtype,
        fill_value=fill_value,
        chunks=chunks,
    ) as (_, array):
        yield array


@contextmanager
def yield_group_and_array(
    indexes: Mapping[str, NDArray1],
    path: PathLike,
    /,
    *,
    overwrite: bool = False,
    dtype: Any = float,
    fill_value: Any = sentinel,
    chunks: bool | int | tuple[int | None, ...] = True,
) -> Iterator[tuple[Group, Array]]:
    """Core context manager for the group and array.

    The dimensions must be JSON-serializable.
    """
    with writer(path, overwrite=overwrite) as temp:
        root = group(store=temp)
        root.attrs["dims"] = tuple(indexes)
        if isinstance(fill_value, Sentinel):
            fill_value_use = get_fill_value(dtype)
        else:
            fill_value_use = fill_value
        for i, index in enumerate(indexes.values()):
            _ = root.array(f"index_{i}", index, **_codec(index.dtype))
        shape = tuple(map(len, indexes.values()))
        shape_use = (1,) if shape == () else shape
        root.attrs["shape"] = shape
        array = root.full(
            "values",
            fill_value=fill_value_use,
            shape=shape_use,
            chunks=chunks,
            dtype=dtype,
            **_codec(dtype),
        )
        yield root, array


class NoIndexesError(ValueError):
    """Raised when there are no indexes."""


IselIndexer = int | slice | Sequence[int] | NDArrayB1 | NDArrayI1


def _codec(dtype: Any, /) -> dict[str, Any]:
    """Generate the object codec if necesary."""
    return {"object_codec": JSON()} if dtype == object else {}


class NDArrayWithIndexes:
    """An `ndarray` with indexes stored on disk."""

    def __init__(
        self,
        path: PathLike,
        /,
        *,
        mode: Literal["r", "r+", "a", "w", "w-"] = "a",
    ) -> None:
        super().__init__()
        self._path = Path(path)
        if not self._path.exists():
            msg = f"{self._path}"
            raise FileNotFoundError(msg)
        self._mode = mode

    @override
    def __repr__(self) -> str:
        cls = get_class_name(self)
        path = self._path.as_posix()
        return f"{cls}({path!r})"

    @override
    def __str__(self) -> str:
        cls = get_class_name(self)
        path = self._path.as_posix()
        return f"{cls}({path})"

    @property
    def array(self) -> Array:
        """The underlying `zarr.Array`."""
        return cast(Array, self.group["values"])

    @property
    def attrs(self) -> Attributes:
        """The underlying attributes."""
        return self.group.attrs

    @property
    def dims(self) -> tuple[str, ...]:
        """The dimensions of the underlying array."""
        return tuple(self.attrs["dims"])

    @property
    def dtype(self) -> Any:
        """The type of the underlying array."""
        return self.array.dtype

    @property
    def group(self) -> Group:
        """The dimensions of the underlying array."""
        return open_group(self._path, mode=self._mode)

    @property
    def indexes(self) -> dict[str, NDArray1]:
        """The indexes of the underlying array."""
        return {
            dim: self._get_index_by_int(i) for i, dim in enumerate(self.dims)
        }

    @property
    def is_scalar(self) -> bool:
        """Whether the underlying array is scalar or not."""
        return self.shape == ()

    @property
    def is_non_scalar(self) -> bool:
        """Whether the underlying array is empty or not."""
        return self.shape != ()

    def isel(
        self,
        indexers: Mapping[str, IselIndexer] | None = None,
        /,
        **indexer_kwargs: IselIndexer,
    ) -> Any:
        """Select orthogonally using integer indexes."""
        merged = ({} if indexers is None else dict(indexers)) | indexer_kwargs
        func = partial(self._get_isel_indexer, indexers=merged)
        i = tuple(map(func, self.dims))
        return self.array.oindex[i]

    @property
    def ndarray(self) -> NDArray[Any]:
        """The underlying `numpy.ndarray`."""
        arr = self.array[:]
        if self.is_scalar:
            return array(arr.item(), dtype=arr.dtype)
        return arr

    @property
    def ndim(self) -> int:
        """The number of dimensions of the underlying array."""
        return len(self.shape)

    def sel(
        self,
        indexers: Mapping[str, Any] | None = None,
        /,
        **indexer_kwargs: Any,
    ) -> Any:
        """Select orthogonally using index values."""
        merged = ({} if indexers is None else dict(indexers)) | indexer_kwargs
        func = partial(self._get_sel_indexer, indexers=merged)
        i = tuple(map(func, self.dims))
        return self.array.oindex[i]

    @property
    def shape(self) -> tuple[int, ...]:
        """The shape of the underlying array."""
        return tuple(self.attrs["shape"])

    @property
    def size(self) -> int:
        """The size of the underlying array."""
        return 0 if self.is_scalar else int(prod(self.shape).item())

    @property
    def sizes(self) -> dict[str, int]:
        """The sizes of the underlying array."""
        return {dim: len(index) for dim, index in self.indexes.items()}

    def _get_index_by_int(self, i: int, /) -> NDArray1:
        """Get the index of a given dimension, by its integer index."""
        return cast(NDArray1, self.group[f"index_{i}"][:])

    def _get_index_by_name(self, dim: str, /) -> NDArray1:
        """Get the index of a given dimension, by its dimension name."""
        try:
            i = self.dims.index(dim)
        except ValueError:
            msg = f"{dim=}"
            raise InvalidDimensionError(msg) from None
        return self._get_index_by_int(i)

    def _get_isel_indexer(
        self, dim: str, /, *, indexers: Mapping[str, IselIndexer]
    ) -> Any:
        """Get the integer-indexer for a given dimension."""
        try:
            indexer = indexers[dim]
        except KeyError:
            return slice(None)
        if isinstance(indexer, int | ndarray | slice):
            return indexer
        return array(indexer, dtype=int)

    def _get_sel_indexer(
        self, dim: str, /, *, indexers: Mapping[str, Any]
    ) -> Any:
        """Get the value-indexer for a given dimension."""
        try:
            indexer = indexers[dim]
        except KeyError:
            return slice(None)
        index = self._get_index_by_name(dim)
        if has_dtype(index, (datetime64D, datetime64Y)):
            indexer = self._cast_date_indexer(indexer, index.dtype, ensure_date)
        elif has_dtype(index, datetime64ns):
            indexer = self._cast_date_indexer(
                indexer, index.dtype, ensure_datetime
            )
        if is_iterable_not_str(indexer):
            bool_indexer = isin(index, indexer)
            if sum(bool_indexer) == len(indexer):
                return bool_indexer
            msg = f"{dim=}, {indexer=}"
            raise InvalidIndexValueError(msg) from None
        try:
            return flatn0(index == indexer)
        except (NoTrueElementsError, MultipleTrueElementsError):
            msg = f"{dim=}, {indexer=}"
            raise InvalidIndexValueError(msg) from None

    def _cast_date_indexer(
        self, indexer: Any, dtype: Any, ensure: Callable[[Any], Any], /
    ) -> Any:
        """Cast a `dt.date` or `dt.datetime` indexer."""
        suffix = extract_group(r"^datetime64\[(\w+)\]$", dtype.name)

        def cast(x: Any, /) -> Any:
            return datetime64(ensure(x), suffix)

        if is_iterable_not_str(indexer):
            return list(map(cast, indexer))
        return cast(indexer)


class InvalidDimensionError(ValueError):
    """Raised when an dimension is invalid."""


class InvalidIndexValueError(ValueError):
    """Raised when an index value is invalid."""
