from abc import ABC, abstractmethod

import os
import os.path


class Segment(ABC):
    def __init__(self):
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
    def __init__(self):
        self.color = None
        self.last_only = True

    def get_text(self):
        cwd = os.getcwd()
        if self.last_only:
            return os.path.basename(cwd)
        return os.getcwd()

    def get_color(self):
        return self.color

    def get_background_color(self):
        return "black"

    def get_icon(self):
        return None


class SegmentForward(Segment):
    def get_text(self):
        return " > "
