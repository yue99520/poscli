from typing import Union

from pydarknet import Detector as Darknet, Image as DarknetImage

from apps.base import DetectedObject
from apps.base.config import Configuration
from apps.detect import CoordinateClassifier


class Detector(Darknet):
    def __init__(self, config: Configuration, **kwargs):
        self.config = config
        self.cfg_path = kwargs.get("cfg_path")
        self.weights_path = kwargs.get("weights_path")
        self.data_path = kwargs.get("data_path")
        super().__init__(
            bytes(self.cfg_path, encoding="utf-8"),
            bytes(self.weights_path, encoding="utf-8"),
            0,
            bytes(self.data_path, encoding="utf-8")
        )

    def detect(self, frame):
        results = super().detect(DarknetImage(frame))
        unfiltered_positions = []
        for cat, score, bounds in results:
            x, y, w, h = bounds
            position = self.create_detected_object(
                frame=frame,
                name=cat.decode("utf-8"),
                x=x,
                y=y,
                width=w,
                height=h,
                confidence=score,
            )
            if position is not None:
                unfiltered_positions.append(position)
        return unfiltered_positions

    def create_detected_object(self, frame, name, x, y, width, height, confidence) -> Union[DetectedObject, None]:
        return DetectedObject(
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            confidence=confidence,
        )


class TargetDetector(Detector):
    def __init__(self, config: Configuration, **kwargs):
        super(TargetDetector, self).__init__(config, **kwargs)
        self.threshold = config.target.confident_threshold

    def create_detected_object(self, frame, name, x, y, width, height, confidence) -> Union[DetectedObject, None]:
        position = super().create_detected_object(frame, name, x, y, width, height, confidence)
        if position.confidence < self.threshold:
            return None
        return position


class CoordinateDetector(Detector):
    def __init__(self, config: Configuration, **kwargs):
        super().__init__(config, **kwargs)
        self.threshold = config.coordinate.confident_threshold

        self._coordinate_classifier = CoordinateClassifier()

        self.origin_name = config.coordinate.origin_name,
        self.red_name = config.coordinate.red_name,
        self.blue_name = config.coordinate.blue_name,

    def create_detected_object(self, frame, name, x, y, width, height, confidence) -> Union[DetectedObject, None]:
        position = super().create_detected_object(frame, name, x, y, width, height, confidence)
        if position.confidence < self.threshold:
            return None

        coord_type = self._coordinate_classifier.classify(frame, position)
        if coord_type == CoordinateClassifier.ORIGIN:
            position.name = self.origin_name
        elif coord_type == CoordinateClassifier.RED:
            position.name = self.red_name
        elif coord_type == CoordinateClassifier.BLUE:
            position.name = self.blue_name
        else:
            return None
        return position
