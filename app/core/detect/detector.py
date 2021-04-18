from threading import Thread

from app.core.vendor import Camera, CoordinatePosition, TargetPosition


class Detector(Thread):
    def __init__(self, name: str):
        super(Detector, self).__init__(name=name)
        self._exit = False
        self._exited = False

    def start(self) -> None:
        self._exit = False
        self._exited = False
        super(Detector, self).start()

    def exit(self):
        self._exit = True
        while True:
            if self._exited is True:
                break


class TargetDetector(Detector):
    def __init__(self, camera: Camera, target_context: TargetPosition):
        super(TargetDetector, self).__init__(name="TargetDetectorThread")
        self._camera = camera
        self._target_context = target_context

    def run(self) -> None:
        pass


class CoordinateDetector(Detector):

    def __init__(self, camera: Camera, coordinate_context: CoordinatePosition):
        super(CoordinateDetector, self).__init__(name="CoordinateDetectorThread")
        self.camera = camera
        self._coordinate_context = coordinate_context

    def run(self) -> None:
        pass
