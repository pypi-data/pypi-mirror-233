"""Logging Related Functions."""
import logging

import click
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

from . import typer as typer_helpers

LOGGER = logging.getLogger(__name__)


def set_logging(verbose: bool = False) -> None:
    """Set the Logging Config according to passed arguments.

    parameters
    ----------
    verbose : bool
        wether to Log debug Messages
    """
    if verbose:
        install_rich_traceback(suppress=[click, typer_helpers])
        logging.basicConfig(
            level=logging.DEBUG,
            format="{name}: {message}",
            style="{",
            handlers=[
                RichHandler(
                    level=logging.DEBUG,
                    show_path=True,
                    rich_tracebacks=True,
                    tracebacks_show_locals=True,
                )
            ],
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="{message}",
            style="{",
            handlers=[RichHandler(level=logging.INFO, show_path=False, rich_tracebacks=False)],
            datefmt="%Y-%m-%d %H:%M:%S",
        )
