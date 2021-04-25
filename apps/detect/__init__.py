import abc
from copy import deepcopy
from random import randint
from threading import Lock
from typing import List, Tuple

from apps.base import DetectedObject
from apps.base.config import Configuration
from apps.base.thread import ApplicationThread
from apps.camera import Camera
from apps.context import SystemContext, DetectThreadInterface
from apps.detect.detect import Detector


class DetectThread(ApplicationThread, DetectThreadInterface, abc.ABC):

    def __init__(self, name: str, context: SystemContext, config: Configuration, camera: Camera):
        super().__init__(name, context, config)
        self._camera = camera
        self._darknet = self.get_detector()

        self._unfiltered_positions_lock = Lock()
        self._unfiltered_positions = list()
        self._unfiltered_positions_id = 0

    def get_unfiltered_positions(self) -> Tuple[List[DetectedObject], int]:
        self._unfiltered_positions_lock.acquire()
        li = deepcopy(self._unfiltered_positions)
        self._unfiltered_positions_lock.release()
        return li, self._unfiltered_positions_id

    def set_unfiltered_positions(self, unfiltered_positions: List[DetectedObject]):
        self._unfiltered_positions_lock.acquire()
        self._unfiltered_positions = unfiltered_positions
        self._unfiltered_positions_id = randint(0, 1000)
        self._unfiltered_positions_lock.release()

    def get_detector(self) -> Detector:
        raise NotImplementedError()

    def run_loop(self) -> None:
        image = self._camera.get_frame()
        positions = self._darknet.detect(image)

        self.set_unfiltered_positions(positions)


class TargetDetectThread(DetectThread):
    def get_detector(self) -> Detector:
        return Detector(
            cfg_path=self.configuration.target.cfg_path,
            weights_path=self.configuration.target.weights_path,
            data_path=self.configuration.target.data_path,
        )


class CoordinateDetectThread(DetectThread):
    def get_detector(self) -> Detector:
        return Detector(
            cfg_path=self.configuration.coordinate.cfg_path,
            weights_path=self.configuration.coordinate.weights_path,
            data_path=self.configuration.coordinate.data_path,
        )
