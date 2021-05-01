from cv2 import cv2 as cv


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Shape:
    def __init__(self, name):
        self.name = name


class Rectangle(Shape):
    def __init__(self, name, score: float, point: Point, width: int, height: int):
        super().__init__(name)
        self.pt1 = (int(point.x - width / 2), int(point.y - height / 2))
        self.pt2 = (int(point.x + width / 2), int(point.y + height / 2))
        self.score = score

    def draw(self, frame, color):
        cv.rectangle(frame, self.pt1, self.pt2, color)
        txt = f"{self.name} sc: {str(self.score)}"
        cv.putText(frame, txt, self.pt2, cv.FONT_HERSHEY_DUPLEX, 0.5, color=color)
