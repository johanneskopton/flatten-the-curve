from box import Box


class Obstacle(Box):
    def __init__(self, x1, x2, y1, y2):
        super().__init__(x1, x2, y1, y2)
