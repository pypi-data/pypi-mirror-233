from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING
from typing import Any

from hypothesis.extra.numpy import array_shapes
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import composite
from xarray import DataArray

from utilities.hypothesis import lift_draw
from utilities.hypothesis import lists_fixed_length
from utilities.hypothesis import text_ascii
from utilities.hypothesis.numpy import bool_arrays
from utilities.hypothesis.numpy import float_arrays
from utilities.hypothesis.numpy import int_arrays
from utilities.hypothesis.numpy import str_arrays
from utilities.hypothesis.pandas import int_indexes
from utilities.hypothesis.typing import MaybeSearchStrategy
from utilities.xarray.typing import DataArrayB
from utilities.xarray.typing import DataArrayF
from utilities.xarray.typing import DataArrayI
from utilities.xarray.typing import DataArrayO

if TYPE_CHECKING:  # pragma: no cover
    from utilities.pandas.typing import IndexA
    from utilities.pandas.typing import IndexI


@composite
def dicts_of_indexes(
    _draw: Any,
    /,
    *,
    min_dims: int = 1,
    max_dims: int | None = None,
    min_side: int = 1,
    max_side: int | None = None,
) -> dict[str, IndexI]:
    """Strategy for generating dictionaries of indexes."""
    draw = lift_draw(_draw)
    shape = draw(
        array_shapes(
            min_dims=min_dims,
            max_dims=max_dims,
            min_side=min_side,
            max_side=max_side,
        )
    )
    ndims = len(shape)
    dims = draw(lists_fixed_length(text_ascii(), ndims, unique=True))
    indexes = (draw(int_indexes(n=length)) for length in shape)
    return dict(zip(dims, indexes, strict=True))


@composite
def bool_data_arrays(
    _draw: Any,
    indexes: MaybeSearchStrategy[Mapping[str, IndexA]] | None = None,
    /,
    *,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
    name: MaybeSearchStrategy[str | None] = None,
    **indexes_kwargs: MaybeSearchStrategy[IndexA],
) -> DataArrayB:
    """Strategy for generating data arrays of booleans."""
    draw = lift_draw(_draw)
    indexes_ = draw(_merge_into_dict_of_indexes(indexes, **indexes_kwargs))
    shape = tuple(map(len, indexes_.values()))
    values = draw(bool_arrays(shape=shape, fill=fill, unique=unique))
    return DataArray(
        data=values, coords=indexes_, dims=list(indexes_), name=draw(name)
    )


@composite
def float_data_arrays(
    _draw: Any,
    indexes: MaybeSearchStrategy[Mapping[str, IndexA]] | None = None,
    /,
    *,
    min_value: MaybeSearchStrategy[float | None] = None,
    max_value: MaybeSearchStrategy[float | None] = None,
    allow_nan: MaybeSearchStrategy[bool] = False,
    allow_inf: MaybeSearchStrategy[bool] = False,
    allow_pos_inf: MaybeSearchStrategy[bool] = False,
    allow_neg_inf: MaybeSearchStrategy[bool] = False,
    integral: MaybeSearchStrategy[bool] = False,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
    name: MaybeSearchStrategy[str | None] = None,
    **indexes_kwargs: MaybeSearchStrategy[IndexA],
) -> DataArrayF:
    """Strategy for generating data arrays of floats."""
    draw = lift_draw(_draw)
    indexes_ = draw(_merge_into_dict_of_indexes(indexes, **indexes_kwargs))
    shape = tuple(map(len, indexes_.values()))
    values = draw(
        float_arrays(
            shape=shape,
            min_value=min_value,
            max_value=max_value,
            allow_nan=allow_nan,
            allow_inf=allow_inf,
            allow_pos_inf=allow_pos_inf,
            allow_neg_inf=allow_neg_inf,
            integral=integral,
            fill=fill,
            unique=unique,
        )
    )
    return DataArray(
        data=values, coords=indexes_, dims=list(indexes_), name=draw(name)
    )


@composite
def int_data_arrays(
    _draw: Any,
    indexes: MaybeSearchStrategy[Mapping[str, IndexA]] | None = None,
    /,
    *,
    min_value: MaybeSearchStrategy[int | None] = None,
    max_value: MaybeSearchStrategy[int | None] = None,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
    name: MaybeSearchStrategy[str | None] = None,
    **indexes_kwargs: MaybeSearchStrategy[IndexA],
) -> DataArrayI:
    """Strategy for generating data arrays of ints."""
    draw = lift_draw(_draw)
    indexes_ = draw(_merge_into_dict_of_indexes(indexes, **indexes_kwargs))
    shape = tuple(map(len, indexes_.values()))
    values = draw(
        int_arrays(
            shape=shape,
            min_value=min_value,
            max_value=max_value,
            fill=fill,
            unique=unique,
        )
    )
    return DataArray(
        data=values, coords=indexes_, dims=list(indexes_), name=draw(name)
    )


@composite
def str_data_arrays(
    _draw: Any,
    indexes: MaybeSearchStrategy[Mapping[str, IndexA]] | None = None,
    /,
    *,
    min_size: MaybeSearchStrategy[int] = 0,
    max_size: MaybeSearchStrategy[int | None] = None,
    allow_none: MaybeSearchStrategy[bool] = False,
    fill: SearchStrategy[Any] | None = None,
    unique: MaybeSearchStrategy[bool] = False,
    name: MaybeSearchStrategy[str | None] = None,
    **indexes_kwargs: MaybeSearchStrategy[IndexA],
) -> DataArrayO:
    """Strategy for generating data arrays of strings."""
    draw = lift_draw(_draw)
    indexes_ = draw(_merge_into_dict_of_indexes(indexes, **indexes_kwargs))
    shape = tuple(map(len, indexes_.values()))
    values = draw(
        str_arrays(
            shape=shape,
            min_size=min_size,
            max_size=max_size,
            allow_none=allow_none,
            fill=fill,
            unique=unique,
        )
    )
    return DataArray(
        data=values, coords=indexes_, dims=list(indexes_), name=draw(name)
    )


@composite
def _merge_into_dict_of_indexes(
    _draw: Any,
    indexes: MaybeSearchStrategy[Mapping[str, IndexA]] | None = None,
    /,
    **indexes_kwargs: MaybeSearchStrategy[IndexA],
) -> dict[str, IndexA]:
    """Merge positional & kwargs of indexes into a dictionary."""
    draw = lift_draw(_draw)
    if (indexes is None) and (len(indexes_kwargs) == 0):
        return draw(dicts_of_indexes())
    indexes_out: dict[str, IndexA] = {}
    if indexes is not None:
        indexes_out |= dict(draw(indexes))
    indexes_out |= {k: draw(v) for k, v in indexes_kwargs.items()}
    return indexes_out
