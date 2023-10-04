"""Top-level package for Style Echo."""
__all__ = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bblack",
    "bred",
    "bgreen",
    "byellow",
    "bblue",
    "bmagenta",
    "bcyan",
    "bwhite",
    "reset",
)
import click

from secho import color
from secho.color import *  # noqa: F403

__all__ = color.__all__ + __all__

def black(msg="", bold=False, underline=False, blink=False, err=False):
    """black."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='black', err=err)


def red(msg="", bold=False, underline=False, blink=False, err=True):
    """red."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='red', err=err)


def green(msg="", bold=False, underline=False, blink=False, err=False):
    """green."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='green', err=err)


def yellow(msg="", bold=False, underline=False, blink=False, err=False):
    """yellow."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='yellow', err=err)


def blue(msg="", bold=False, underline=False, blink=False, err=False):
    """blue."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='blue', err=err)


def magenta(msg="", bold=False, underline=False, blink=False, err=False):
    """magenta."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='magenta', err=err)


def cyan(msg="", bold=False, underline=False, blink=False, err=False):
    """cyan."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='cyan', err=err)


def white(msg="", bold=False, underline=False, blink=False, err=False):
    """white."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='white', err=err)


def bblack(msg="", bold=False, underline=False, blink=False, err=False):
    """bblack."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_black', err=err)


def bred(msg="", bold=False, underline=False, blink=False, err=False):
    """bred."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_red', err=err)


def bgreen(msg="", bold=False, underline=False, blink=False, err=False):
    """bgreen."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_green', err=err)


def byellow(msg="", bold=False, underline=False, blink=False, err=False):
    """byellow."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_yellow', err=err)


def bblue(msg="", bold=False, underline=False, blink=False, err=False):
    """bblue."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_blue', err=err)


def bmagenta(msg="", bold=False, underline=False, blink=False, err=False):
    """bmagenta."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_magenta', err=err)


def bcyan(msg="", bold=False, underline=False, blink=False, err=False):
    """bcyan."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_cyan', err=err)


def bwhite(msg="", bold=False, underline=False, blink=False, err=False):
    """bwhite."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_white', err=err)


def reset(msg="", bold=False, underline=False, blink=False, err=False):
    """reset."""
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='reset', err=err)
