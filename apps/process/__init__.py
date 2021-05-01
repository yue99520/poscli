from copy import deepcopy
from typing import List, Tuple, Optional

from apps.base import DetectedObject, ProcessedObject, FilteredPositions
from apps.base.config import Configuration

from apps.context import SystemContext, ProcessThreadInterface
from apps.process.filter import DetectionCleaner
from apps.process.linear import RealPositionProcessor, Point


class ProcessThread(ProcessThreadInterface):
    """
    1. 將 unfiltered_positions 過濾成虛擬座標位置與虛擬目標位置
    2. 計算虛擬座標位置與虛擬目標位置的相對位置，並轉為目標與機械手臂相對位置
    3. 輸出目標位置
    """
    def __init__(self, name: str, context: SystemContext, config: Configuration):
        super().__init__(name, context, config)
        self._processor = RealPositionProcessor(
            real_red_axis_len=self.configuration.coordinate.real_origin_to_red_length,
            real_blue_axis_len=self.configuration.coordinate.real_origin_to_blue_length,
        )
        self._filter = DetectionCleaner(self.configuration)
        self.logging = self.context.logging
        self._processed_targets = list()
        self._origin = None
        self._red = None
        self._blue = None
        self._targets = list()

    def run_loop(self) -> None:
        # get source
        targets: List[DetectedObject] = self.context.target_detect_thread.get_unfiltered_positions()
        detections: List[DetectedObject] = self.context.coordinate_detect_thread.get_unfiltered_positions()

        # filter
        bests = self._filter.de_dup(targets, detections)
        origin, red, blue, targets = self._filter.reg_detections(bests)

        self._origin = origin
        self._red = red
        self._blue = blue
        self._targets = targets

        # process
        processed_targets = list()
        if origin is not None and red is not None and blue is not None:
            for target in targets:
                processed_target = self._process_target(origin, red, blue, target)
                processed_targets.append(processed_target)
                self._log_processed_object(processed_target)

        self._processed_targets = processed_targets

    def _log_processed_object(self, processed_target: ProcessedObject):
        if processed_target is not None and self.configuration.system.show_processed_log:
            self.logging.debug(f"ProcessThread: name={str(processed_target.name)} red={str(processed_target.red)} blue={str(processed_target.blue)}")

    def get_processed_targets(self) -> List[ProcessedObject]:
        return deepcopy(self._processed_targets)

    def get_coordinates(self) -> Tuple[Optional[DetectedObject], Optional[DetectedObject], Optional[DetectedObject]]:
        return deepcopy(self._origin), deepcopy(self._red), deepcopy(self._blue)

    def get_targets(self) -> List[DetectedObject]:
        return deepcopy(self._targets)

    def _process_target(self, raw_origin, raw_red, raw_blue, raw_target) -> ProcessedObject:
        origin = Point(raw_origin.x, raw_origin.y)
        red = Point(raw_red.x, raw_red.y)
        blue = Point(raw_blue.x, raw_blue.y)
        target = Point(raw_target.x, raw_target.y)

        red_dis, blue_dis = self._processor.find_position(
            origin=origin,
            red=red,
            blue=blue,
            target=target,
        )

        return ProcessedObject(
            name=raw_target.name,
            red=red_dis,
            blue=blue_dis,
            width=raw_target.width,
            height=raw_target.height,
            confidence=raw_target.confidence,
        )

    def get_merge_depth(self) -> int:
        raise NotImplementedError()
