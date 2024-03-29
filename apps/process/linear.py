import math
from typing import Tuple


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def find_distance(self, point):
        square_of_x_diff = math.pow(self.x - point.x, 2)
        square_of_y_diff = math.pow(self.y - point.y, 2)
        return math.sqrt(square_of_x_diff + square_of_y_diff)


class Equation:
    """
    數學方程式物件
    """
    @staticmethod
    def by_two_points(point1: Point, point2: Point):
        """
        方程式模型： y = ax + b
        """
        a = (point2.y - point1.y) / (point2.x - point1.x)
        b = point1.y - a * point1.x
        return Equation(round(a, 4), round(b, 4))

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_normal_equation(self, pass_point: Point):
        """
        取得過 pass_point 的法向量方程式
        """
        normal_a = -1 / self.a
        normal_b = pass_point.y - normal_a * pass_point.x
        return Equation(round(normal_a, 4), round(normal_b, 4))

    def intersection_of(self, equation) -> Point:
        """
        聯立方程式求解
        """
        x = (-self.b + equation.b) / (self.a - equation.a)
        y = self.a * x + self.b
        return Point(x, y)


class RealPositionProcessor:
    """
    計算定位虛擬座標點，產生真實座標。
    """
    def __init__(self, real_red_axis_len, real_blue_axis_len):
        """
        傳入真實軸線長度數值，供虛擬座標點轉換。
        """
        self._real_red_axis_len = real_red_axis_len
        self._real_blue_axis_len = real_blue_axis_len

    def find_position(
            self,
            origin: Point,
            red: Point,
            blue: Point,
            target: Point,
            ) -> Tuple[float, float]:

        red_axis_ratio = self._get_real_len_ratio(self._real_red_axis_len, origin, red)
        blue_axis_ratio = self._get_real_len_ratio(self._real_blue_axis_len, origin, blue)

        real_red_distance = self._real_value_on_axis(origin, red, target, red_axis_ratio)
        real_blue_distance = self._real_value_on_axis(origin, blue, target, blue_axis_ratio)

        return real_red_distance, real_blue_distance

    def _get_real_len_ratio(self, real_len, origin, axis):
        return real_len / origin.find_distance(axis)

    def _real_value_on_axis(self, origin: Point, axis: Point, target: Point, ratio: float):
        """
        求 target 在 axis 軸上到原點的距離。

        過程：
            1. 求原點到 axis 點方程式
            2. 求軸線方程式過 target 點的法線方程式
            3. 求法線方程式與軸線方程式的交點（投影點）
            4. 求投影點到 origin 的距離（單位 pixels）
            5. 做 pixels 與真實長度的轉換
        """
        axis_equation = Equation.by_two_points(origin, axis)
        normal_of_axis_equation = axis_equation.get_normal_equation(target)
        projection_of_target = normal_of_axis_equation.intersection_of(axis_equation)

        # todo 這裡做了修改，原本是求投影點到 target 的距離，改成到 origin 的距離，應該會讓方法給的數值變正確，但意思是其他地方就要做x, y的轉換。
        pixel_distance = projection_of_target.find_distance(origin)

        real_distance = pixel_distance * ratio
        return real_distance
