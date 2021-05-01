from typing import List

from cv2 import cv2 as cv

from apps.base import DetectedObject
from apps.base.config import Configuration
from apps.camera import Camera
from apps.context import ViewThreadInterface, SystemContext
from apps.view.buffer import ViewBuffer
from apps.view.shape import Rectangle, Point


class ViewThread(ViewThreadInterface):
    def __init__(self, name: str, context: SystemContext, config: Configuration, camera: Camera):
        super().__init__(name, context, config)
        self._camera = camera
        self._window_name = "Poscli View"
        self.logging = context.logging

        # position context
        self.targets = list()
        self.coordinates = list()

    def run_loop(self) -> None:
        frame = self._camera.get_frame()

        targets: List[DetectedObject] = self.context.process_thread.get_targets()
        for target in targets:
            self._attempt_draw_detected_object(frame, target)

        origin, red, blue = self.context.process_thread.get_coordinates()
        self._attempt_draw_detected_object(frame, origin)
        self._attempt_draw_detected_object(frame, red)
        self._attempt_draw_detected_object(frame, blue)

        cv.imshow(self._window_name, frame)
        cv.waitKey(1)

    def _attempt_draw_detected_object(self, frame, detected_object: DetectedObject):
        if detected_object is not None:
            rectangle = self._detected_object_to_rectangle(detected_object)
            rectangle.draw(frame, (0, 255, 255))

    def _detected_object_to_rectangle(self, detected_object: DetectedObject) -> Rectangle:
        return Rectangle(
            name=detected_object.name,
            score=detected_object.confidence,
            point=Point(detected_object.x, detected_object.y),
            width=detected_object.width,
            height=detected_object.height,
        )

    def stopping(self):
        super(ViewThread, self).stopping()
        cv.destroyWindow(self._window_name)
