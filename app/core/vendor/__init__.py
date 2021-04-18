import abc
from app.core.vendor.entity import *
from app.core.vendor.resource import *
from app.core.vendor.system import *


class SystemContext:
    def __init__(self,
                 config,
                 camera: Camera,
                 system_state: SystemState,
                 coordinate: CoordinatePosition,
                 target: TargetPosition,
                 real_position: TargetPosition,
                 ):
        self.config = config
        self.camera = camera
        self.system_state = system_state
        self.coordinate = coordinate
        self.target = target
        self.real_position = real_position


class Service(abc.ABC):
    """
        一個服務單位
    """
    def pause(self):
        pass

    def resume(self):
        pass

    def start(self):
        pass

    def execute(self, *args, **kwargs):
        pass