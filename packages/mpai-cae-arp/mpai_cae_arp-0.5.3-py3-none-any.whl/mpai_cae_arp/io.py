"""
.. deprecated:: 0.2.0.

    Use rich library instead.

This module contains functions to print and format text in the console.

"""
import warnings
from collections.abc import Iterable
from enum import Enum

from typing_extensions import deprecated

warnings.warn(
    "the mpai_cae_arp.io module is deprecated",
    DeprecationWarning,
    stacklevel=2,
)

END = "\033[0m"


@deprecated("Use rich library instead")
class Style(Enum):
    """Styles for console output."""

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


@deprecated("Use rich library instead")
class Color(Enum):
    """Colors for console output."""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARK_CYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


@deprecated("Use rich library instead")
def prettify(
    text: str,
    color: Color | None = None,
    styles: Iterable[Style] | None = None,
) -> str:
    """Format a string with some styles.

    Parameters
    ----------
    text : str
        string to format
    color : Color, optional
        color to use
    styles : list[Style], optional
        styles to use

    Returns
    -------
    str
        formatted string

    """
    prepend = ""

    if color:
        prepend += color.value
    if styles:
        for style in styles:
            prepend += style.value

    return prepend + text + END


@deprecated("Use rich library instead")
def pprint(
    text: str,
    color: Color | None = None,
    styles: list[Style] | None = None,
) -> None:
    """Format a string with some styles and prints it.

    Parameters
    ----------
    text : str
        string to format
    color : Color, optional
        color to use
    styles : list[Style], optional
        styles to use

    """
    print(prettify(text, color, styles))
