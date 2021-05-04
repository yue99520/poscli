import time
from typing import List, Tuple, Dict

from apps.base.config import Configuration
from apps.arm.bot import Arm
from apps.base import ProcessedObject
from apps.context import ArmThreadInterface, SystemContext


class ArmThread(ArmThreadInterface):
    def __init__(self, name: str, context: SystemContext, config: Configuration):
        super().__init__(name, context, config)
        self.arm = Arm(self.configuration, reset=config.arm.reset)
        self.logging = context.logging
        self.accumulation_goal = config.arm.accumulation_goal
        self.processed_objects_accumulation: Dict[ProcessedObject, int] = dict()

    def run_loop(self) -> None:
        processed_objects: List[ProcessedObject] = self.context.process_thread.get_processed_targets()
        if len(processed_objects) == 0:
            return

        optional_processed_object = self._add_processed_objects(processed_objects)
        if optional_processed_object is not None:
            name, x, y = self.get_arm_xy(optional_processed_object)
            self._log_arm_position(x, y)
            self.arm.move_object(name, x, y, wait=True)

    def get_arm_xy(self, processed_object: ProcessedObject) -> Tuple[str, int, int]:
        return processed_object.name, processed_object.blue * 10, processed_object.red * 10

    def _add_processed_objects(self, processed_objects: List[ProcessedObject]):
        for processed_object in processed_objects:
            is_exist = False
            for po, count in self.processed_objects_accumulation.items():
                if processed_object.name == po.name:
                    is_exist = True
                    if int(processed_object.red) == int(po.red) and int(processed_object.blue) == int(po.blue):
                        self.processed_objects_accumulation[po] += 1
                        if self.processed_objects_accumulation[po] > self.accumulation_goal:
                            self.processed_objects_accumulation.clear()
                            return po
            if not is_exist:
                self.processed_objects_accumulation[processed_object] = 1
        return None

    def _log_arm_position(self, x: int, y: int):
        if self.configuration.system.show_processed_log:
            self.logging.debug(f"ArmThread: x={str(x)} y={str(y)}")
