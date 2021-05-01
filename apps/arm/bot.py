# pydobot version 1.1.0
from pydobot.dobot import Dobot
from serial.tools import list_ports

from apps.base.config import Configuration


class Arm:
    def __init__(self, config: Configuration, reset: bool):
        self.bot = Dobot(list_ports.comports()[1].device)
        self._red_axis_base = config.arm.red_base
        self._blue_axis_base = config.arm.blue_base
        self._destination_x = config.arm.destination_x
        self._destination_y = config.arm.destination_y
        self._destination_z = config.arm.destination_z
        if reset:
            self.reset()

    def reset(self):
        self.bot.wait_for_cmd(self.bot.home())

    def move_object(self, red, blue, wait=True):
        self.bot.move_to(red + self._red_axis_base, blue + self._blue_axis_base, 20)
        self.bot.suck(True)
        self.bot.move_to(red + self._red_axis_base, blue + self._blue_axis_base, -46)
        self.bot.move_to(red + self._red_axis_base, blue + self._blue_axis_base, 20)
        self.bot.move_to(self._destination_x, self._destination_y, self._destination_z + 70)
        self.bot.move_to(self._destination_x, self._destination_y, self._destination_z)
        self.bot.suck(False)
        self.bot.move_to(self._destination_x, self._destination_y, self._destination_z + 70)
        cmd_id = self.bot.move_to(120, 0, 0)
        if wait:
            self.bot.wait_for_cmd(cmd_id)
