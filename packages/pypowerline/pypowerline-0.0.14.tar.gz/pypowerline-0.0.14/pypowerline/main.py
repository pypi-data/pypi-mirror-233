"""
main
"""
import os
from typing import Dict, Any
from pytconf import register_endpoint, register_main, config_arg_parse_and_launch

from termcolor import cprint
from pypowerline.utils import execute_python_file

from pypowerline.static import DESCRIPTION, APP_NAME, VERSION_STR


symbols = {
    "detached": "\u2693",
    "ahead": "\u2B06",
    "behind": "\u2B07",
    "staged": "\u2714",
    "changed": "\u270E",
    "new": "?",
    "conflicted": "\u273C",
    "stash": "\u2398",
    "git": "\uE0A0",
    "hg": "\u263F",
    "bzr": "\u2B61\u20DF",
    "fossil": "\u2332",
    "svn": "\u2446",
    "separator": "\u25B6",
    "separator_b": "\uE0B0",
    "separator_thin": "\u276F",
    "separator_thin_b": "\uE0B1",
    "lock": "\uE0A2",
    "folder": "\U0001F5C1",
    "virtual_env": "\U0001F40D",
    "battery": "\U0001F50C",
    "ellipsis": "\u2026",
    "bat": "\u26A1",
    "up": "\u2191",
}


@register_endpoint(
    configs=[],
    description="print a prompt for bash",
)
def bash() -> None:
    py_file = os.path.expanduser("~/.config/pypowerline/segments.py")
    vals: Dict[str, Any] = {}
    try:
        execute_python_file(py_file, vals=vals)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(e)
        print("cannot execute segments > ", end="")
        return
    if "segments" not in vals:
        print("segments not defined > ", end="")
        return
    segments = vals["segments"]
    for segment in segments:
        segment.setup()
        print(segment.get_text(), end="")


@register_endpoint(
    configs=[],
    description="do some test printing on the terminal (development purposes)",
)
def test() -> None:
    cwd = os.getcwd()
    symbol = symbols["separator_b"]
    print(f"{cwd} > ", end="")
    cprint("cwd", "black", "on_light_magenta", end="")
    cprint("cwd", "black", "on_light_grey", end="")
    cprint("cwd", "black", "on_grey", end="")
    cprint("cwd", "black", "on_blue", end="")
    cprint("cwd", "black", "on_light_blue", end="")
    cprint("cwd", "white", "on_cyan", end="")
    cprint("cwd", "white", "on_green", end="")
    cprint(f"{symbol}", "light_cyan", "on_black", end="")
    print()


@register_endpoint(
    configs=[],
    description="do tmux",
)
def tmux() -> None:
    cwd = os.getcwd()
    print(f"{cwd} > ", end="")
    cprint(f"{cwd}", "red", "on_light_magenta", end="")


@register_endpoint(
    configs=[],
    description="print special symbols (used for development)",
)
def dump_symbols() -> None:
    for k, v in symbols.items():
        print(k, v)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
