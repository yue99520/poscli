from threading import Lock
from cv2 import cv2 as cv
from numpy import ndarray


class CameraNotOpenedException(Exception):
    pass


class Camera:
    def __init__(self, port):
        self._cam = cv.VideoCapture(port)
        self._lock = Lock()

    def get_frame(self) -> ndarray:
        self._lock.acquire()
        if self._cam.isOpened():
            ret, frame = self._cam.read()
        else:
            raise CameraNotOpenedException()
        self._lock.release()
        return frame
