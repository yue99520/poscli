from threading import Thread
from pydarknet import Detector as YoloDetector
from pydarknet import Image as YoloImage
from app.core.vendor import Camera, CoordinatePosition, TargetPosition, DetectedObject


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


class TargetDetectThread(Detector):
    def __init__(self, cfg_path, weights_path, data_path,
                 camera: Camera, target_context: TargetPosition):
        super(TargetDetectThread, self).__init__(name="TargetDetectorThread")
        self._weights_path = weights_path
        self._cfg_path = cfg_path
        self._data_path = data_path
        self._camera = camera
        self._target_context = target_context
        self._yolo = YoloDetector(bytes(cfg_path, encoding="utf-8"),
                                  bytes(weights_path, encoding="utf-8"),
                                  0,
                                  bytes(data_path, encoding="utf-8"))

    def run(self) -> None:
        image = self._camera.get_frame()
        results = self._yolo.detect(YoloImage(image))
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


class CoordinateDetectThread(Detector):

    def __init__(self, camera: Camera, coordinate_context: CoordinatePosition):
        super(CoordinateDetectThread, self).__init__(name="CoordinateDetectorThread")
        self.camera = camera
        self._coordinate_context = coordinate_context

    def run(self) -> None:
        pass
