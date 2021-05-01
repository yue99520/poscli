import time

from copy import deepcopy
from threading import Lock
from typing import List

from apps.base import DetectedObject
from apps.base.config import Configuration
from apps.camera import Camera
from apps.context import SystemContext, DetectThreadInterface
from apps.detect.coordinate import CoordinateClassifier
from apps.detect.detect import Detector, CoordinateDetector, TargetDetector


class DetectThread(DetectThreadInterface):

    def __init__(self, name: str, context: SystemContext, config: Configuration, camera: Camera):
        super().__init__(name, context, config)
        self._camera = camera
        self._darknet = self.get_detector()
        self.logging = self.context.logging

        self._unfiltered_positions_lock = Lock()
        self._unfiltered_positions = list()
        self._unfiltered_positions_id = 0

        self._positions_queue = list()
        self._last_positions = None

    def get_unfiltered_positions(self) -> List[DetectedObject]:
        return deepcopy(self._unfiltered_positions)

    def set_unfiltered_positions(self, unfiltered_positions: List[DetectedObject]):
        self._unfiltered_positions = unfiltered_positions

    def get_detector(self) -> Detector:
        raise NotImplementedError()

    def run_loop(self) -> None:
        time.sleep(0.2)
        frame = self._camera.get_frame()
        positions = self._darknet.detect(frame)

        for position in positions:
            self._log_detected_object(position)

        self.set_unfiltered_positions(positions)

    def _log_detected_object(self, detected_object: DetectedObject):
        if detected_object is not None and self.configuration.system.show_detections_log:
            self.logging.debug(f"DetectThread: name={str(detected_object.name)} x={str(detected_object.x)} y={str(detected_object.y)}")


class TargetDetectThread(DetectThread):
    def get_detector(self) -> Detector:
        return TargetDetector(
            config=self.configuration,
            cfg=self.configuration.target.cfg_path,
            weights=self.configuration.target.weights_path,
            data=self.configuration.target.data_path,
        )


class CoordinateDetectThread(DetectThread):
    def get_detector(self) -> Detector:
        return CoordinateDetector(
            config=self.configuration,
            cfg=self.configuration.coordinate.cfg_path,
            weights=self.configuration.coordinate.weights_path,
            data=self.configuration.coordinate.data_path,
        )
