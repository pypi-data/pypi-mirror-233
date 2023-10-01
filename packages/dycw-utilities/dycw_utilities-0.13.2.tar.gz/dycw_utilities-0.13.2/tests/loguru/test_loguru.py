from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Sequence
from pathlib import Path
from re import search
from time import sleep

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import dictionaries
from hypothesis.strategies import lists
from hypothesis.strategies import none
from hypothesis.strategies import sampled_from
from loguru import logger

from utilities.hypothesis import temp_paths
from utilities.hypothesis import text_ascii
from utilities.logging import LogLevel
from utilities.loguru import _FILES_ENV_VAR
from utilities.loguru import _augment_levels
from utilities.loguru import _get_files_path
from utilities.loguru import setup_loguru
from utilities.os import temp_environ
from utilities.pathlib import PathLike


class TestSetupLoguru:
    def test_disabled(self) -> None:
        setup_loguru()
        logger.info("test")

    @given(levels=dictionaries(text_ascii(min_size=1), sampled_from(LogLevel)))
    def test_level(self, levels: dict[str, LogLevel]) -> None:
        setup_loguru(levels=levels)
        logger.info("test")

    @given(module=text_ascii(min_size=1))
    def test_standard(self, module: str) -> None:
        setup_loguru(levels={module: LogLevel.INFO})
        logger.info("test")

    @given(enable=lists(text_ascii(min_size=1)))
    def test_enable(self, enable: Sequence[str]) -> None:
        setup_loguru(enable=enable)
        logger.info("test")

    @given(level=sampled_from(LogLevel))
    def test_luigi(self, level: LogLevel) -> None:
        setup_loguru(levels={"luigi": level})
        logger.info("test")

    @given(root=temp_paths(), files=text_ascii(min_size=1))
    @settings(max_examples=1)
    def test_files(self, root: Path, files: str) -> None:
        setup_loguru(files=files, files_root=root)
        sleep(0.05)
        logger.info("message")
        sleep(0.05)
        (files_dir,) = root.iterdir()
        assert files_dir.name == files
        results = {path.name for path in files_dir.iterdir()}
        expected = {"debug", "info", "warning", "error", "log"}
        assert results == expected
        with files_dir.joinpath("log").open() as fh:
            (line,) = fh.read().splitlines()
        assert search(
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}  INFO  \w+\-\d+  "
            r"[\w\.\-]+  message$",
            line,
        )


env_var_prefixes = text_ascii(min_size=20)
modules = text_ascii(min_size=1).map(str.lower)


class TestAugmentLevels:
    def test_none(self) -> None:
        result = _augment_levels()
        assert result == {}

    @given(levels=dictionaries(text_ascii(min_size=1), sampled_from(LogLevel)))
    def test_main(self, levels: Mapping[str, LogLevel] | None) -> None:
        result = _augment_levels(levels=levels)
        assert result == levels

    @given(
        env_var_prefix=env_var_prefixes,
        module=modules,
        level=sampled_from(LogLevel),
    )
    def test_with_env_var(
        self, env_var_prefix: str, module: str, level: LogLevel
    ) -> None:
        with temp_environ({f"{env_var_prefix}_{module}": level}):
            result = _augment_levels(env_var_prefix=env_var_prefix)
        assert result == {module: level}

    @given(
        env_var_prefix=env_var_prefixes,
        module=modules,
        level=sampled_from(LogLevel),
    )
    def test_without_env_var(
        self, env_var_prefix: str, module: str, level: LogLevel
    ) -> None:
        with temp_environ({f"{env_var_prefix}_{module}": level}):
            result = _augment_levels(env_var_prefix=None)
        assert result == {}

    @given(
        env_var_prefix=env_var_prefixes,
        module=modules,
        level_direct=sampled_from(LogLevel),
        level_env_var=sampled_from(LogLevel),
    )
    def test_both(
        self,
        level_direct: LogLevel,
        env_var_prefix: str,
        module: str,
        level_env_var: LogLevel,
    ) -> None:
        with temp_environ({f"{env_var_prefix}_{module}": level_env_var}):
            result = _augment_levels(
                levels={module: level_direct}, env_var_prefix=env_var_prefix
            )
        assert result == {module: level_env_var}


class TestGetFilesPath:
    @given(files=text_ascii(min_size=1) | none())
    def test_main(self, files: PathLike | None) -> None:
        result = _get_files_path(files=files)
        assert result == files

    @given(env_var=text_ascii(min_size=1), files=text_ascii(min_size=1))
    def test_with_env_var(self, env_var: str, files: str) -> None:
        with temp_environ({env_var: files}):
            result = _get_files_path(env_var=env_var)
        assert result == files

    @given(files=text_ascii(min_size=1))
    def test_without_env_var(self, files: str) -> None:
        with temp_environ({_FILES_ENV_VAR: files}):
            result = _get_files_path(env_var=None)
        assert result is None

    @given(
        files=text_ascii(min_size=1),
        env_var_key=env_var_prefixes,
        env_var_value=text_ascii(min_size=1),
    )
    def test_both(
        self, files: str, env_var_key: str, env_var_value: str
    ) -> None:
        with temp_environ({env_var_key: env_var_value}):
            result = _get_files_path(files=files, env_var=env_var_key)
        assert result == files
