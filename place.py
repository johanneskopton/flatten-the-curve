from box import Box


class Place(Box):
    def __init__(self, x1, x2, y1, y2, place_type, i):
        self.id = i
        self.others = None
        self.place_type = place_type
        super().__init__(x1, x2, y1, y2)

    def pass_others(self, others):
        self.others = others
