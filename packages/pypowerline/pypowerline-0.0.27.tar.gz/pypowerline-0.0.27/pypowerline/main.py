"""
main
"""
import os
from typing import Dict, Any, List
from pytconf import register_endpoint, register_main, config_arg_parse_and_launch

from termcolor import cprint, RESET
from pypowerline.utils import execute_python_file
from pypowerline.segments import Segment

from pypowerline.symbols import Symbol
from pypowerline.static import DESCRIPTION, APP_NAME, VERSION_STR


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
    segments: List[Segment] = vals["segments"]
    for segment in segments:
        text = ""
        if segment.icon is not None:
            # TODO: why the two spaces here? Is it because it's unicode?
            text += segment.icon.value + "  "
        text += segment.get_text()
        if segment.separator is not None:
            text += segment.separator.value
        if segment.color is not None:
            if segment.background is not None:
                attrs: List[str] = []
                if segment.reverse_sep:
                    attrs += "reverse"
                text += RESET
                cprint(
                    text,
                    segment.color.value,
                    "on_" + segment.background.value,
                    attrs=attrs,
                    end="",
                )
            else:
                cprint(text, segment.color.value, end="")
        else:
            print(text, end="")


@register_endpoint(
    configs=[],
    description="do some test printing on the terminal (development purposes)",
)
def test() -> None:
    cwd = os.getcwd()
    symbol = Symbol.SEPARATOR_B.value
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
    for symbol in Symbol:
        print(symbol, symbol.value)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
