from copy import deepcopy
from threading import Lock


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
