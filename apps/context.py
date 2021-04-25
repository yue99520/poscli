from typing import List, Tuple

from apps.base import DetectedObject, ProcessedObject, FilteredPositions
from apps.base.thread import ApplicationThread


class DetectThreadInterface(ApplicationThread):
    def get_unfiltered_positions(self) -> Tuple[List[DetectedObject], int]: ...


class ProcessThreadInterface(ApplicationThread):
    def get_processed_target(self) -> Tuple[ProcessedObject, int]: ...
    def get_filtered_positions(self) -> Tuple[FilteredPositions, int]: ...


class ArmThreadInterface(ApplicationThread):
    pass


class ViewThreadInterface(ApplicationThread):
    pass


class SystemContext:
    def __init__(self,
                 coordinate_detect_thread: DetectThreadInterface = None,
                 target_detect_thread: DetectThreadInterface = None,
                 process_thread: ProcessThreadInterface = None,
                 arm_thread: ArmThreadInterface = None,
                 view_thread: ViewThreadInterface = None):

        self.coordinate_detect_thread = coordinate_detect_thread
        self.target_detect_thread = target_detect_thread
        self.process_thread = process_thread
        self.arm_thread = arm_thread
        self.view_thread = view_thread

    def stop_all(self):
        self.coordinate_detect_thread.stop(wait=True)
        self.target_detect_thread.stop(wait=True)
        self.process_thread.stop(wait=True)
        self.arm_thread.stop(wait=True)
        self.view_thread.stop(wait=True)
