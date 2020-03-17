class Box:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def get_dims(self):
        return self.x1, self.x2, self.y1, self.y2
