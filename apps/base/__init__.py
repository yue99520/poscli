class DetectedObject:
    def __init__(self, name, x, y, width, height, confidence):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence


class ProcessedObject:
    def __init__(self, name, red, blue, width, height, confidence):
        self.name = name
        self.red = red
        self.blue = blue
        self.width = width
        self.height = height
        self.confidence = confidence


class FilteredPositions:
    def __init__(self, origin, red, blue, target):
        self.origin = origin
        self.red = red
        self.blue = blue
        self.target = target