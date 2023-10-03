from abc import ABC, abstractmethod
from typing import Optional

import os
import os.path

from pypowerline.symbols import Symbol
from pypowerline.colors import Color


class Segment(ABC):
    def __init__(
            self,
            color: Optional[Color] = None,
            background: Optional[Color] = None,
            icon: Optional[Symbol] = None,
            separator: Optional[Symbol] = Symbol.SEPARATOR,
            reverse_sep: bool = True,
    ):
        self.color = color
        self.background = background
        self.icon = icon
        self.separator = separator
        self.reverse_sep = reverse_sep

    @abstractmethod
    def get_text(self) -> str:
        """ return the text of the segment """


class SegmentCwd(Segment):
    def __init__(
            self,
            color: Optional[Color] = None,
            background: Optional[Color] = None,
            icon: Optional[Symbol] = Symbol.FOLDER,
            separator: Optional[Symbol] = Symbol.SEPARATOR_B,
            reverse_sep: bool = True,
            last_only: bool = False,
            home_as_tilde: bool = True,
    ):
        super().__init__(
            color=color,
            background=background,
            icon=icon,
            separator=separator,
            reverse_sep=reverse_sep,
        )
        self.last_only = last_only
        self.home_as_tilde = home_as_tilde
        self.home_directory = os.path.expanduser("~")

    def get_text(self) -> str:
        cwd = os.getcwd()
        if self.home_as_tilde and cwd.startswith(self.home_directory):
            cwd = "~" + cwd[len(self.home_directory):]
        if self.last_only:
            return os.path.basename(cwd)
        return cwd


class SegmentForward(Segment):
    def __init__(self):
        super().__init__()

    def get_text(self):
        return " > "


class SegmentSpace(Segment):
    def __init__(self):
        super().__init__(separator=None)

    def get_text(self):
        return " "
