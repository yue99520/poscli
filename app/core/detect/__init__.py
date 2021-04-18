from app.core.detect.detector import TargetDetector, CoordinateDetector
from app.core.detect.positioner import TargetPositioner
from app.core.vendor import SystemContext


class DetectionService:

    def __init__(self, system_context: SystemContext):
        self.system_context = system_context
        self.target_detector = TargetDetector(
            camera=self.system_context.camera,
            target_context=self.system_context.target,
        )
        self.coordinate_detector = CoordinateDetector(
            camera=self.system_context.camera,
            coordinate_context=self.system_context.coordinate,
        )
        self.target_positioner = TargetPositioner(
            real_axis_len=self.system_context.config,
            real_position=self.system_context.real_position,
            target_context=self.system_context.target,
            coordinate_context=self.system_context.coordinate,
        )

    def start(self):
        self.coordinate_detector.start()
        self.target_detector.start()
        self.target_positioner.start()

    def exit(self):
        if self.target_positioner.is_alive():
            self.target_detector.exit()

        if self.target_detector.is_alive():
            self.target_detector.exit()

        if self.coordinate_detector.is_alive():
            self.coordinate_detector.exit()
