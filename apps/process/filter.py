import abc
from typing import List, Tuple, Union

from apps.base import DetectedObject


class RawPositionsFilterer(abc.ABC):
    def filter(self, raw_positions: List[DetectedObject]) -> Tuple[List[DetectedObject], Union[DetectedObject, None]]:
        raise NotImplementedError()


class RedCoordinateFilter(RawPositionsFilterer):
    def filter(self, raw_positions: List[DetectedObject]) -> Tuple[List[DetectedObject], Union[DetectedObject, None]]:
        return raw_positions, None


class BlueCoordinateFilter(RawPositionsFilterer):
    def filter(self, raw_positions: List[DetectedObject]) -> Tuple[List[DetectedObject], Union[DetectedObject, None]]:
        pass


class OriginCoordinateFilter(RawPositionsFilterer):
    def filter(self, raw_positions: List[DetectedObject]) -> Tuple[List[DetectedObject], Union[DetectedObject, None]]:
        pass


class TargetFilter(RawPositionsFilterer):
    def filter(self, raw_positions: List[DetectedObject]) -> Tuple[List[DetectedObject], Union[DetectedObject, None]]:
        pass