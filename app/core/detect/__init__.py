from app.core.detect.detector import TargetDetectThread, CoordinateDetectThread
from app.core.detect.positioner import RealPositionProcessThread
from app.core.vendor import SystemContext


class DetectionService:

    def __init__(self, system_context: SystemContext):
        self.system_context = system_context
        self.target_detect_thread = TargetDetectThread(
            cfg_path=None,
            weights_path=None,
            data_path=None,
            camera=self.system_context.camera,
            target_context=self.system_context.target,
        )
        self.coordinate_detect_thread = CoordinateDetectThread(
            camera=self.system_context.camera,
            coordinate_context=self.system_context.coordinate,
        )
        self.real_position_thread = RealPositionProcessThread(
            real_axis_len=self.system_context.config,
            real_position=self.system_context.real_position,
            target_context=self.system_context.target,
            coordinate_context=self.system_context.coordinate,
        )

    def start(self):
        self.coordinate_detect_thread.start()
        self.target_detect_thread.start()
        self.real_position_thread.start()

    def exit(self):
        if self.real_position_thread.is_alive():
            self.target_detect_thread.exit()

        if self.target_detect_thread.is_alive():
            self.target_detect_thread.exit()

        if self.coordinate_detect_thread.is_alive():
            self.coordinate_detect_thread.exit()
