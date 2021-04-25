from cv2 import cv2 as cv


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Shape:
    def __init__(self, name):
        self.name = name


class Rectangle(Shape):
    def __init__(self, name, point: Point, width: int, height: int):
        super().__init__(name)
        self.pt1 = (int(point.x - width / 2), int(point.y - height / 2))
        self.pt2 = (int(point.x + width / 2), int(point.y + height / 2))

    def draw(self, frame, color):
        cv.rectangle(frame, self.pt1, self.pt2, color)
        cv.putText(frame, self.name, self.pt2, cv.FONT_HERSHEY_DUPLEX, 1, color=color)
