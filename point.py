class Point:
    def __init__(self, s):
        self.x = s[0]
        self.y = s[1]

    def get_tuple(self):
        return tuple([self.x, self.y])
