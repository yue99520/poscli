from typing import List, Tuple

from apps.base import DetectedObject, ProcessedObject, FilteredPositions


class DetectThreadInterface:
    def get_unfiltered_positions(self) -> Tuple[List[DetectedObject], int]: ...


class ProcessThreadInterface:
    def get_processed_target(self) -> Tuple[ProcessedObject, int]: ...
    def get_filtered_positions(self) -> Tuple[FilteredPositions, int]: ...


class ArmThreadInterface:
    pass


class ViewThreadInterface:
    pass


class SystemContext:
    def __init__(self,
                 coordinate_detect_thread: DetectThreadInterface,
                 target_detect_thread: DetectThreadInterface,
                 process_thread: ProcessThreadInterface,
                 arm_thread: ArmThreadInterface,
                 view_thread: ViewThreadInterface):

        self.coordinate_detect_thread = coordinate_detect_thread
        self.target_detect_thread = target_detect_thread
        self.process_thread = process_thread
        self.arm_thread = arm_thread
        self.view_thread = view_thread
