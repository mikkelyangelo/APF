from math import sqrt


class Cell:
    def __init__(self, x, y, end):
        self.x = x
        self.y = y

        self.is_polygon = 0
        self.distance = 0
        self.distances = []
        self.capability = 0
     #   self.print()

        self.evcl_distance = sqrt((x - end[0]) ** 2 + (y - end[1]) ** 2)

    def __repr__(self):
        return str((self.x, self.y))

    def reset(self):
        self.capability = 0
        self.distance = 0
        self.distances = []
