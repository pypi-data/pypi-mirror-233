from abc import ABC, abstractmethod

import os
import os.path


class Segment(ABC):
    def __init__(self):
        pass

    def setup(self):
        pass

    @abstractmethod
    def get_text(self):
        """ return the text of the segment """
    def get_color(self):
        """ return the color of the segment """
    def get_background_color(self):
        """ return the background color of the segment """
    def get_icon(self):
        """ return the special character of the segment """


class SegmentCwd(Segment):
    def __init__(self, color="green", last_only=False, home_as_tilde=True):
        self.color = color
        self.last_only = last_only
        self.home_as_tilde = home_as_tilde
        self.home_directory = os.path.expanduser("~")

    def get_text(self):
        cwd = os.getcwd()
        if cwd.startswith(self.home_directory):
            cwd = "~/" + cwd[len(self.home_directory):]
        if self.last_only:
            return os.path.basename(cwd)
        return cwd


class SegmentForward(Segment):
    def get_text(self):
        return " > "
