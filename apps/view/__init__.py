import abc

from cv2 import cv2 as cv

from apps.base import DetectedObject
from apps.base.config import Configuration
from apps.base.thread import ApplicationThread
from apps.camera import Camera
from apps.context import ViewThreadInterface, SystemContext
from apps.view.shape import Rectangle, Point


class ViewThread(ViewThreadInterface):
    def __init__(self, name: str, context: SystemContext, config: Configuration, camera: Camera):
        super().__init__(name, context, config)
        self._camera = camera
        self._window_name = "Poscli View"

    def run_loop(self) -> None:
        frame = self._camera.get_frame()

        positions, data_id = self.context.process_thread.get_filtered_positions()

        target = positions.target
        self._attempt_draw_detected_object(frame, target)

        origin = positions.origin
        self._attempt_draw_detected_object(frame, origin)

        red = positions.red
        self._attempt_draw_detected_object(frame, red)

        blue = positions.blue
        self._attempt_draw_detected_object(frame, blue)

        cv.imshow(self._window_name, frame)
        # cv.waitKey(1)

    def _attempt_draw_detected_object(self, frame, detected_object: DetectedObject):
        if detected_object is not None:
            rectangle = self._detected_object_to_rectangle(detected_object)
            rectangle.draw(frame, (0, 255, 255))

    def _detected_object_to_rectangle(self, detected_object: DetectedObject) -> Rectangle:
        return Rectangle(
            name=detected_object.name,
            point=Point(detected_object.x, detected_object.y),
            width=detected_object.width,
            height=detected_object.height,
        )

    def stopping(self):
        super(ViewThread, self).stopping()
        cv.destroyWindow(self._window_name)
