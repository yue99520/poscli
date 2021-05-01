# pydobot version 1.1.0
from pydobot.dobot import Dobot
from serial.tools import list_ports

from apps.base.config import Configuration


class Arm:
    def __init__(self, config: Configuration, reset: bool):
        self.bot = Dobot(list_ports.comports()[1].device)
        self._vertical_fix = config.arm.vertical_off_set
        self._horizontal_fix = config.arm.horizontal_off_set
        self._destination_x = config.arm.destination_x
        self._destination_y = config.arm.destination_y
        self._destination_z = config.arm.destination_z
        if reset:
            self.reset()

    def reset(self):
        self.bot.wait_for_cmd(self.bot.home())

    def move_object(self, x, y, wait=True):
        self.bot.move_to(x + self._vertical_fix, y + self._horizontal_fix, 20)
        self.bot.suck(True)
        self.bot.move_to(x + self._vertical_fix, y + self._horizontal_fix, -50)
        self.bot.move_to(x + self._vertical_fix, y + self._horizontal_fix, 20)
        self.bot.move_to(self._destination_x, self._destination_y, self._destination_z + 70)
        self.bot.move_to(self._destination_x, self._destination_y, self._destination_z)
        self.bot.suck(False)
        self.bot.move_to(self._destination_x, self._destination_y, self._destination_z + 70)
        cmd_id = self.bot.move_to(120, 0, 0)
        if wait:
            self.bot.wait_for_cmd(cmd_id)
