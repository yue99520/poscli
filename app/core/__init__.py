# import config as default_config
# import logging
# from app.core import SystemContext
# from app.core.state import SystemContext, SystemState
# from app.core.vendor.entity import CoordinatePosition, TargetPosition
# from app.util.log import logger_init
#
#
# class System:
#     def __init__(self, config=default_config):
#         logger_init(log_level=config.log_level)
#         self.config = config
#         self.context = self._make_context()
#
#     def _make_context(self):
#         camera = Camera(port=self.config.camera_port)
#         return SystemContext(
#             camera=camera,
#             system_state=SystemState(),
#             coordinate=CoordinatePosition(),
#             target=TargetPosition(),
#         )
