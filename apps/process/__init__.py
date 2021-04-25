import abc
from copy import deepcopy
from random import randint
from threading import Lock
from time import sleep
from typing import List, Tuple

from apps.base import DetectedObject, ProcessedObject, FilteredPositions
from apps.base.config import Configuration
from apps.base.thread import ApplicationThread

from apps.context import SystemContext, ProcessThreadInterface

from apps.process.filter import RawPositionsFilterer, RedCoordinateFilter, BlueCoordinateFilter, OriginCoordinateFilter, TargetFilter
from apps.process.linear import RealPositionProcessor, Point


class AbstractProcessThread(ApplicationThread, ProcessThreadInterface, abc.ABC):
    """
    1. 將 unfiltered_positions 過濾成虛擬座標位置與虛擬目標位置
    2. 計算虛擬座標位置與虛擬目標位置的相對位置，並轉為目標與機械手臂相對位置
    3. 輸出目標位置
    """
    def __init__(self, name: str, context: SystemContext, config: Configuration):
        super().__init__(name, context, config)
        self._processed_target_lock = Lock()
        self._processed_target_id = 0
        self._processed_target = None

        self._filtered_positions_lock = Lock()
        self._filtered_positions_id = 0
        self._filtered_positions = None

        self._origin_filter = self.get_origin_filter()
        self._red_filter = self.get_red_filter()
        self._blue_filter = self.get_blue_filter()
        self._target_filter = self.get_blue_filter()

        self._processor = self.get_processor()

        self._current_coord_data_id = -1
        self._current_target_data_id = -1

    def run_loop(self) -> None:
        raw_targets = self._get_target_unfiltered_positions()
        raw_coordinates = self._get_coordinate_unfiltered_positions()

        filtered_positions = self._filter_positions(raw_targets, raw_coordinates)
        self.set_filtered_positions(filtered_positions)

        processed_target = self._process_target(
            raw_origin=filtered_positions.origin,
            raw_red=filtered_positions.red,
            raw_blue=filtered_positions.blue,
            raw_target=filtered_positions.target,
        )
        self.set_processed_target(processed_target)

    def _get_coordinate_unfiltered_positions(self) -> List[DetectedObject]:
        while True:
            positions, data_id = self.context.coordinate_detect_thread.get_unfiltered_positions()
            if self._current_coord_data_id != data_id and len(positions) > 0:
                self._current_coord_data_id = data_id
                return positions
            else:
                sleep(0.2)

    def _get_target_unfiltered_positions(self) -> List[DetectedObject]:
        while True:
            positions, data_id = self.context.target_detect_thread.get_unfiltered_positions()
            if self._current_target_data_id != data_id and len(positions) > 0:
                self._current_target_data_id = data_id
                return positions
            else:
                sleep(0.2)
    
    def _filter_positions(self, raw_targets: List[DetectedObject], raw_coordinates: List[DetectedObject]) -> FilteredPositions:
        raw_coordinates, filtered_raw_origin = self._origin_filter.filter(raw_coordinates)
        raw_coordinates, filtered_raw_red = self._red_filter.filter(raw_coordinates)
        raw_coordinates, filtered_raw_blue = self._blue_filter.filter(raw_coordinates)
        raw_targets, filtered_raw_target = self._target_filter.filter(raw_targets)
        
        return FilteredPositions(
            origin=filtered_raw_origin,
            red=filtered_raw_red,
            blue=filtered_raw_blue,
            target=filtered_raw_target,
        )

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

    def get_processed_target(self) -> Tuple[ProcessedObject, int]:
        self._processed_target_lock.acquire()
        target = deepcopy(self._processed_target)
        self._processed_target_lock.release()
        return target, self._processed_target_id

    def set_processed_target(self, target: ProcessedObject):
        self._processed_target_lock.acquire()
        self._processed_target = target
        self._processed_target_id = randint(0, 1000)
        self._processed_target_lock.release()

    def get_filtered_positions(self) -> Tuple[FilteredPositions, int]:
        self._filtered_positions_lock.acquire()
        positions = deepcopy(self._filtered_positions)
        self._filtered_positions_lock.release()
        return positions, self._filtered_positions_id

    def set_filtered_positions(self, filtered_positions: FilteredPositions):
        self._filtered_positions_lock.acquire()
        self._filtered_positions = filtered_positions
        self._filtered_positions_id = randint(0, 1000)
        self._filtered_positions_lock.release()

    def get_processor(self) -> RealPositionProcessor:
        raise NotImplementedError()

    def get_origin_filter(self) -> RawPositionsFilterer:
        raise NotImplementedError()

    def get_red_filter(self) -> RawPositionsFilterer:
        raise NotImplementedError()

    def get_blue_filter(self) -> RawPositionsFilterer:
        raise NotImplementedError()

    def get_target_filter(self) -> RawPositionsFilterer:
        raise NotImplementedError()


class ProcessThread(AbstractProcessThread):
    def __init__(self, name: str, context: SystemContext, config: Configuration):
        super().__init__(name, context, config)

    def get_processor(self):
        return RealPositionProcessor(
            real_red_axis_len=self.configuration.coordinate.real_origin_to_red_length,
            real_blue_axis_len=self.configuration.coordinate.real_origin_to_blue_length,
        )

    def get_origin_filter(self):
        return OriginCoordinateFilter()

    def get_red_filter(self):
        return RedCoordinateFilter()

    def get_blue_filter(self):
        return BlueCoordinateFilter()

    def get_target_filter(self):
        return TargetFilter()


