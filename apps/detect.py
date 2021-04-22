import abc
from copy import deepcopy
from threading import Lock
from typing import List

from pydarknet import Detector as Darknet
from pydarknet import Image as DarknetImage

from apps.base.config import Configuration
from apps.base.thread import ApplicationThread
from apps.camera import Camera
from apps.context import SystemContext


class DetectedObject:
    def __init__(self, name, x, y, width, height, confidence):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence


class CoordinatePosition:
    def __init__(self):
        self._lock = Lock()
        self._origin = None
        self._red = None
        self._blue = None

    def get_origin(self) -> DetectedObject:
        self._lock.acquire()
        position = deepcopy(self._origin)
        self._lock.release()
        return position

    def get_red(self) -> DetectedObject:
        self._lock.acquire()
        position = deepcopy(self._red)
        self._lock.release()
        return position

    def get_blue(self) -> DetectedObject:
        self._lock.acquire()
        position = deepcopy(self._blue)
        self._lock.release()
        return position

    def set_origin(self, position: DetectedObject):
        self._lock.acquire()
        self._origin = position
        self._lock.release()

    def set_red(self, position: DetectedObject):
        self._lock.acquire()
        self._red = position
        self._lock.release()

    def set_blue(self, position: DetectedObject):
        self._lock.acquire()
        self._blue = position
        self._lock.release()


class TargetPosition:
    def __init__(self):
        self._target = None
        self._lock = Lock()

    def get_target(self) -> DetectedObject:
        self._lock.acquire()
        position = deepcopy(self._target)
        self._lock.release()
        return position

    def set_target(self, position: DetectedObject):
        self._lock.acquire()
        self._target = position
        self._lock.release()


class Detector(Darknet):
    def __init__(self, **kwargs):
        self.cfg_path = kwargs.get("cfg_path")
        self.weights_path = kwargs.get("weights_path")
        self.data_path = kwargs.get("data_path")
        super().__init__(
            bytes(self.cfg_path, encoding="utf-8"),
            bytes(self.weights_path, encoding="utf-8"),
            0,
            bytes(self.data_path, encoding="utf-8")
        )

    def detect(self, image):
        results = super().detect(DarknetImage(image))
        unfiltered_positions = []
        for cat, score, bounds in results:
            x, y, w, h = bounds
            position = DetectedObject(
                name=cat.decode("utf-8"),
                x=x,
                y=y,
                width=w,
                height=h,
                confidence=score,
            )
            unfiltered_positions.append(position)
        return unfiltered_positions


class DetectThread(ApplicationThread, abc.ABC):

    def __init__(self, name: str, context: SystemContext, config: Configuration, camera: Camera):
        super().__init__(name, context, config)
        self._camera = camera
        self._darknet = self.get_detector()

        self._unfiltered_positions_lock = Lock()
        self._unfiltered_positions = list()

    def get_unfiltered_positions(self) -> List[DetectedObject]:
        self._unfiltered_positions_lock.acquire()
        li = deepcopy(self._unfiltered_positions)
        self._unfiltered_positions_lock.release()
        return li

    def set_unfiltered_positions(self, unfiltered_positions: List[DetectedObject]):
        self._unfiltered_positions_lock.acquire()
        self._unfiltered_positions = unfiltered_positions
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
