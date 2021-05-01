from typing import List, Tuple

from apps.base.config import Configuration
from apps.arm.bot import Arm
from apps.base import ProcessedObject
from apps.context import ArmThreadInterface, SystemContext


class ArmThread(ArmThreadInterface):
    def __init__(self, name: str, context: SystemContext, config: Configuration):
        super().__init__(name, context, config)
        self.arm = Arm(self.configuration, reset=config.arm.reset)
        self.logging = context.logging

    def run_loop(self) -> None:
        processed_objects: List[ProcessedObject] = self.context.process_thread.get_processed_targets()
        if len(processed_objects) == 0:
            return
        processed_object = processed_objects[0]
        x, y = self.get_arm_xy(processed_object)
        self._log_arm_position(x, y)
        self.arm.move_object(x, y, wait=True)

    def get_arm_xy(self, processed_object: ProcessedObject) -> Tuple[int, int]:
        return processed_object.blue * 10, processed_object.red * 10

    def _log_arm_position(self, x: int, y: int):
        if self.configuration.system.show_processed_log:
            self.logging.debug(f"ArmThread: x={str(x)} y={str(y)}")
