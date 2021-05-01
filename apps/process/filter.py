from typing import List, Tuple, Optional

from apps.base import DetectedObject
from apps.base.config import Configuration


class DetectionCleaner:
    def __init__(self, config: Configuration):
        self.origin_name: str = config.coordinate.origin_name
        self.red_name: str = config.coordinate.red_name
        self.blue_name: str = config.coordinate.blue_name

    def de_dup(self, targets, coordinates) -> List[DetectedObject]:
        grouped_target_list = self._group_by_name(targets)
        grouped_coordinate_list = self._group_by_name(coordinates)

        best = list()
        best += self._find_best_detections(grouped_target_list)
        best += self._find_best_detections(grouped_coordinate_list)

        return best

    def reg_detections(self, detections: List[DetectedObject]) -> Tuple[Optional[DetectedObject], Optional[DetectedObject], Optional[DetectedObject], List[DetectedObject]]:
        origin = None
        red = None
        blue = None
        targets = list()
        for detection in detections:
            if detection.name == self.origin_name:
                origin = detection
            elif detection.name == self.red_name:
                red = detection
            elif detection.name == self.blue_name:
                blue = detection
            else:
                targets.append(detection)
        return origin, red, blue, targets

    def _group_by_name(self, detections: List[DetectedObject]):
        results: List[List[DetectedObject]] = list()
        for detection in detections:
            is_exist = False
            for dup_detections in results:
                if dup_detections[0].name == detection.name:
                    dup_detections.append(detection)
                    is_exist = True
            if not is_exist:
                dup_detections = list()
                dup_detections.append(detection)
                results.append(dup_detections)
        return results

    def _find_best_detections(self, detections_list: List[List[DetectedObject]]) -> List[DetectedObject]:
        best_detections = list()
        for detections in detections_list:
            best = self._find_best_detection(detections)
            if best is not None:
                best_detections.append(best)
        return best_detections

    def _find_best_detection(self, detections: List[DetectedObject]) -> Optional[DetectedObject]:
        best = None
        for detection in detections:
            if detection.x <= 10 or detection.y <= 10:
                continue

            if best is None or detection.confidence >= best.confidence:
                best = detection
                continue
        return best
