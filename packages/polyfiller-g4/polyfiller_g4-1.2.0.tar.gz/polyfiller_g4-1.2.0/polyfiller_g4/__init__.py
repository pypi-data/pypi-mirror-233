import cv2
import numpy
from utilspy_g4 import add_ext
from functools import singledispatchmethod


class PolyFiller:

    def __init__(self, ext: str = 'fill', color=0):
        """
        :param ext: Added ext
        :param color: Fill color
        """

        self._ext = ext
        self._color = color
        self._polygons = []

    def add_polygon(self, polygon: list) -> None:
        """
        Add polygon to polygon list

        :param polygon: Added polygon
        :rtype: None
        :return: None
        """

        self._polygons.append(polygon)

    @singledispatchmethod
    def fill(self, frame_path) -> None:
        raise NotImplementedError(f"Cannot format value of type {type(frame_path)}")

    @fill.register
    def _(self, frame_path: str) -> None:
        """

        :param frame_path:
        :return: None
        """

        frame = cv2.imread(frame_path)
        frame = self.fill(frame)
        cv2.imwrite(add_ext(frame_path, self._ext), frame)

    @fill.register
    def _(self, frame: numpy.ndarray) -> numpy.ndarray:
        """

        :param frame:
        :return: None
        """

        for row in self._polygons:
            polygon = numpy.array([row], dtype=numpy.int32)
            cv2.fillPoly(frame, polygon, self._color)

        return frame
