import abc
from typing import List, Tuple, Union

from apps.base import DetectedObject
from apps.base.config import Configuration


class RawPositionsFilterer(abc.ABC):
    def __init__(self, config: Configuration):
        self.config = config

    def filter(self, raw_positions_stack: List[List[DetectedObject]]) -> Union[DetectedObject, None]:
        raise NotImplementedError()


class CoordinateFilter(RawPositionsFilterer):
    def __init__(self, config: Configuration, coord_name):
        super().__init__(config)
        self._name = coord_name

    def filter(self, raw_positions_stack: List[List[DetectedObject]]) -> Union[DetectedObject, None]:

        if len(raw_positions_stack) == 0:
            return raw_positions_stack, None

        best = None
        for position in raw_positions_stack:
            if position.name != self._name:
                continue
            if best is None or position.confidence >= best.confidence:
                best = position
        return raw_positions_stack, best


class RedCoordinateFilter(CoordinateFilter):
    def __init__(self, config: Configuration):
        super().__init__(config, config.coordinate.red_name)


class BlueCoordinateFilter(CoordinateFilter):
    def __init__(self, config: Configuration):
        super().__init__(config, config.coordinate.blue_name)


class OriginCoordinateFilter(CoordinateFilter):
    def __init__(self, config: Configuration):
        super().__init__(config, config.coordinate.origin_name)


class TargetFilter(RawPositionsFilterer):
    def filter(self, raw_positions_stack: List[List[DetectedObject]]) -> Union[DetectedObject, None]:
        if len(raw_positions_stack) == 0:
            return raw_positions_stack, None

        best = raw_positions_stack[0]
        for position in raw_positions_stack:
            if position.width >= best.width and position.height >= best.height:
                best = position

        if best.x <= 10 or best.y <= 10:
            # by case 處理辨識模型瑕疵
            best = None
        return raw_positions_stack, best
