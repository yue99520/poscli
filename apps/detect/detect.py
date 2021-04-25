from pydarknet import Detector as Darknet, Image as DarknetImage

from apps.base import DetectedObject


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
