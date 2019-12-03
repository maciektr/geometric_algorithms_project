import numpy as np


class Scope:
    def __init__(self, xl=-np.inf, xh=np.inf, yl=-np.inf, yh=np.inf):
        self.x_low = xl
        self.x_high = xh
        self.y_low = yl
        self.y_high = yh

    def get_tuple(self):
        return tuple([self.x_low, self.x_high, self.y_low,self.y_high])

    def in_scope(self, point):
        return self.x_low <= point.x <= self.x_high and self.y_low <= point.y <= self.y_high

    def contains(self, other):
        return (self.x_low <= other.x_low
                and self.x_high >= other.x_high
                and self.y_low <= other.y_low
                and self.y_high >= other.y_high
                )

    def intersects(self, other):
        if self.x_low > other.x_high or other.x_low > self.x_high:
            return False

        if self.y_low > other.y_high or other.y_low > self.y_high:
            return False

        return True

    def common(self, x_low=None, x_high=None, y_low=None, y_high=None):
        if x_low is not None:
            self.x_low = max(self.x_low, x_low)
        if x_high is not None:
            self.x_high = min(self.x_high, x_high)
        if y_low is not None:
            self.y_low = max(self.y_low, y_low)
        if y_high is not None:
            self.y_high = min(self.y_high, y_high)

    def copy(self, other):
        self.x_low = other.x_low
        self.x_high = other.x_high
        self.y_low = other.y_low
        self.y_high = other.y_high

class Point:
    def __init__(self, s):
        self.x = s[0]
        self.y = s[1]

    def get_tuple(self):
        return tuple([self.x, self.y])
