from abc import ABC, abstractmethod

import os
import os.path

from pypowerline.symbols import Symbol


class Segment(ABC):
    def __init__(self, show_icon: bool = True):
        self.show_icon = show_icon

    @abstractmethod
    def get_text(self) -> str:
        """ return the text of the segment """

    def get_icon(self) -> Symbol:
        """ return the special character of the segment """
        return Symbol.NONE

    # def get_color(self) -> str:
    #     """ return the color of the segment """
    # def get_background_color(self) -> str:
    #     """ return the background color of the segment """


class SegmentCwd(Segment):
    def __init__(
            self,
            color: str = "green",
            last_only: bool = False,
            home_as_tilde: bool = True,
            show_icon: bool = True,
    ):
        super().__init__(show_icon=show_icon)
        self.color = color
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

    def get_icon(self) -> Symbol:
        return Symbol.FOLDER


class SegmentForward(Segment):
    def __init__(self):
        super().__init__(show_icon=False)

    def get_text(self):
        return " > "
