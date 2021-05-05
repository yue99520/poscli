# pydobot version 1.1.0
import time

from pydobot.dobot import Dobot
from serial.tools import list_ports

from apps.base.config import Configuration


class Arm:
    destinations = {
        "BlueBox": {
            "red": -140,
            "blue": 100,
            "height": 20,
            "current_height_base": -67,
        },
        "RedBox": {
            "red": -140,
            "blue": 270,
            "height": 20,
            "current_height_base": -67,
        },
        "Mentholatum": {
            "red": -140,
            "blue": 300,
            "height": 20,
            "current_height_base": -67,
        },
        "HerbalCandyBox": {
            "red": 0,
            "blue": 270,
            "height": 25,
            "current_height_base": -67,
        },
    }

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

    def move_object(self, name, blue, red, wait=True):
        des_dict = Arm.destinations[name]
        base_height = -66

        height = des_dict["height"]
        des_blue = des_dict['blue']
        des_red = des_dict['red']
        current_height_base = des_dict['current_height_base']

        # self._move_object(blue, red, des_height, self._destination_x, self._destination_y, self._destination_z, wait)
        self._move_object(blue, red, base_height + height, des_blue, des_red, current_height_base + height, wait)
        # des_dict['current_height_base'] += height

    def _move_object(self, blue, red, height, d_blue, d_red, d_height, wait=True):
        self.bot.move_to(blue + self._blue_axis_base, red + self._red_axis_base, 20)
        self.bot.suck(True)
        self.bot.move_to(blue + self._blue_axis_base, red + self._red_axis_base, height)
        self.bot.move_to(blue + self._blue_axis_base, red + self._red_axis_base, 20)
        self.bot.move_to(d_blue, d_red, d_height + 70)
        self.bot.move_to(d_blue, d_red, d_height)
        self.bot.suck(False)
        self.bot.move_to(d_blue, d_red, d_height + 70)
        cmd_id = self.bot.move_to(120, 0, 0)
        if wait:
            self.bot.wait_for_cmd(cmd_id)
