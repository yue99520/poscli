import logging

import numpy as np

from apps.arm import ArmThread
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
        logger_init(self.configuration.system.log_level)
        logging.debug("start")
        self.system_context.logging = logging

        self.camera = Camera(self.configuration.camera.vertical_camera_port)

        logging.debug("target thread init")
        self.system_context.target_detect_thread = TargetDetectThread(
            name="TargetDetectThread",
            context=self.system_context,
            config=self.configuration,
            camera=self.camera,
        )

        logging.debug("coordinate thread init")
        self.system_context.coordinate_detect_thread = CoordinateDetectThread(
            name="CoordinateDetectThread",
            context=self.system_context,
            config=self.configuration,
            camera=self.camera,
        )

        logging.debug("process thread init")
        self.system_context.process_thread = ProcessThread(
            name="ProcessThread",
            context=self.system_context,
            config=self.configuration,
        )

        logging.debug("arm thread init")
        self.system_context.arm_thread = ArmThread(
            name="ArmThread",
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
        logging.debug("coordinate thread start")
        self.system_context.coordinate_detect_thread.start()
        logging.debug("target thread start")
        self.system_context.target_detect_thread.start()
        logging.debug("process thread start")
        self.system_context.process_thread.start()
        logging.debug("arm thread start")
        self.system_context.arm_thread.start()

        self.system_context.view_thread.run()

        # controller = CommandController(self.configuration, self.system_context)
        # controller.run()
