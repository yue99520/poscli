import numpy as np

from numpy import ndarray

from apps.base import DetectedObject

np.seterr(divide='ignore', invalid='ignore')


class CoordinateClassifier:
    NONE = 0,
    ORIGIN = 1,
    RED = 2,
    BLUE = 3,

    def classify(self, frame, detected_object: DetectedObject):
        cut = self.cut_frame(frame, detected_object)
        color = self.average_color(cut)
        if self.is_red(color):
            return self.RED
        elif self.is_blue(color):
            return self.BLUE
        elif self.is_grey(color):
            return self.ORIGIN
        else:
            return self.NONE

    def cut_frame(self, frame: ndarray, detected_object: DetectedObject):
        return frame[int(detected_object.y - detected_object.height / 2 + 3): int(detected_object.y + detected_object.height / 2 - 3), int(detected_object.x - detected_object.width / 2 + 3): int(detected_object.x + detected_object.width / 2 - 3)]

    def average_color(self, frame: ndarray):
        return frame.mean(axis=0).mean(axis=0)

    def is_red(self, avg_color):
        return avg_color[2] / avg_color[0] >= 1.5 and avg_color[2] / avg_color[1] >= 1.5

    def is_grey(self, avg_color):
        return 0.8 <= avg_color[0] / avg_color[1] <= 1.2 and 0.8 <= avg_color[1] / avg_color[2] <= 1.2

    def is_blue(self, avg_color):
        return avg_color[0] / avg_color[1] >= 1.5 and avg_color[0] / avg_color[2] >= 1.5
