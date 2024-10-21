import logging
import logging.config
import pathlib
from typing import Any, overload

import tomli


DEFAULT_FILE = pathlib.Path(__file__).parent / "logging.toml"


@overload
def load_file(path: str | pathlib.Path, *, allow_not_exist: bool) -> dict[str, Any] | None: ...


@overload
def load_file(path: str | pathlib.Path, *, allow_not_exist: bool = False) -> dict[str, Any]: ...


def load_file(path: str | pathlib.Path, *, allow_not_exist: bool = False) -> dict[str, Any] | None:
    """Load the provided file into toml."""
    try:
        with open(path, "rb") as f:
            return tomli.load(f)
    except FileNotFoundError:
        if allow_not_exist:
            return
        else:
            raise


def configure_logging() -> None:
    """Load logging configuration."""
    default_config = load_file(DEFAULT_FILE)
    user_config = load_file(pathlib.Path.cwd() / "logging.toml", allow_not_exist=True)
    logging.config.dictConfig(default_config)
    if user_config is not None:
        logging.config.dictConfig(user_config)
