import logging

from apps.base import config
from apps.base.config import Configuration
from apps.cli import CommandController
from apps.log import logger_init
from apps.camera import Camera
from apps.context import SystemContext
from apps.detect import TargetDetectThread, CoordinateDetectThread
from apps.process import ProcessThread
from apps.view import ViewThread


class Application:
    def __init__(self, cfg=None):
        self.configuration = Configuration.from_ini(cfg)
        self.system_context = SystemContext()
        self.camera = Camera(self.configuration.camera.vertical_camera_port)

        self.system_context.target_detect_thread = TargetDetectThread(
            name="TargetDetectThread",
            context=self.system_context,
            config=self.configuration,
            camera=self.camera,
        )

        self.system_context.coordinate_detect_thread = CoordinateDetectThread(
            name="CoordinateDetectThread",
            context=self.system_context,
            config=self.configuration,
            camera=self.camera,
        )

        self.system_context.process_thread = ProcessThread(
            name="ProcessThread",
            context=self.system_context,
            config=self.configuration,
        )

        self.system_context.view_thread = ViewThread(
            name="ViewThread",
            context=self.system_context,
            config=self.configuration,
            camera=self.camera,
        )

    def run(self):
        self.system_context.coordinate_detect_thread.start()
        self.system_context.target_detect_thread.start()
        self.system_context.process_thread.start()
        self.system_context.view_thread.start()

        controller = CommandController(self.configuration, self.system_context)
        controller.run()
