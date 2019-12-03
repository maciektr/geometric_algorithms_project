#########################################
#      Algorytmy Grafowe 2019/2020      #
#         Dwuwmiarowe KD-drzewa         #
#          Stanislaw Denkowski          #
#          Maciej Tratnowiecki          #
#########################################

# Import wykorzystywanych modulow
import numpy as np
from simple_geometry import *


# Klasa reprezentujaca wezel w KD-drzewie
class Node:
    # Konstruktor klasy
    def __init__(self, point=None, line=None, left=None, right=None):
        self.point = Point(point) if point is not None else None
        self.line = line
        self.left = left
        self.right = right

    # Funkcja wypisujaca rekurencyjnie, w kolejnosci preorder wszystkie wezly drzewa
    def report_subtree(self):
        if self is None:
            return None
        if self.left is None and self.right is None:
            return [self.point]
        result = []
        res = self.left.report_subtree()
        if res is not None:
            result += res
        res = self.right.report_subtree()
        if res is not None:
            result += res
        return result

    # Funkcja realizujaca rekurencyjny algorytm przeszukania KD-drzewa na poziomie wezla
    def _search(self, scope, actual_scope=Scope(), depth=0):
        if self is None:
            return None
        if self.left is None and self.right is None:
            return None if not scope.in_scope(self.point) else [self.point]

        result = []
        res = self.check_child(self.left, actual_scope, depth, scope)
        if res is not None:
            result += res
        res = self.check_child(self.right, actual_scope, depth, scope)
        if res is not None:
            result += res
        return result

    # Funkcja pomocnicza powyzszej, uruchamiana dla obu poddrzew wezla
    def check_child(self, child, actual_scope, depth, scope):
        if child is not None:
            new_scope = Scope()
            new_scope.copy(actual_scope)

            if depth % 2 == 0 and self.left == child:
                new_scope.common(x_high=self.line)
            elif depth % 2 == 1 and node.left == child:
                new_scope.common(y_high=self.line)
            elif depth % 2 == 0 and node.right == child:
                new_scope.common(x_low=self.line)
            else:
                new_scope.common(y_low=self.line)

            if scope.contains(new_scope):
                return child.report_subtree()
            elif scope.intersects(new_scope):
                return child._search(scope, new_scope, depth + 1)
            return None


# Klasa enkapsulujaca implementacje kd-drzewa
# Przechowuje wezel drzewa oraz obszar do ktorego naleza przechowywane punkty
class Kdtree:
    # Konstruktor,
    # oblicza przedzial w jakim zawarte sa punkty przechowywane w drzewie,
    # wywoluje rekurencyjna funkcje pomocnicza konstruujaca drzewo
    def __init__(self, points):
        self.scope = Scope(min(points, key=lambda x: x[0])[0],
              max(points, key=lambda x: x[0])[0],
              min(points, key=lambda y: y[1])[1],
              max(points, key=lambda y: y[1])[1])
        self.root = self._construct(points)

    # Wspomniana pomocnicza powyzszej, realizuje konstrukcje drzewa zwracajac wezel - korzen drzewa
    def _construct(self, points, depth=0):
        if len(points) < 1:
            return None
        if len(points) == 1:
            return Node(points[0])
        k = len(points) // 2
        indice = depth % 2
        m = int(np.median([i[indice] for i in points]))
        left_slice  = list(filter(lambda x: x[indice] <= m, points))
        right_slice = list(filter(lambda x: x[indice] > m, points))
        return Node(
            line = m,
            left = self._construct(left_slice, depth + 1),
            right = self._construct(right_slice , depth + 1)
        )

    # Funkcja implementujaca algorytm przeszukania kd-drzewa, odwolujaca sie do metod z wezla
    def find(self,  x_low=-np.inf, x_high=np.inf, y_low=-np.inf, y_high=np.inf):
        scope = Scope(x_low, x_high, y_low, y_high)
        res = self.root._search(scope, self.scope)
        return [p.get_tuple() for p in res]


# Ponizszy kod nie jest wykorzystywany w implementacji kd-drzewa
if __name__ == '__main__':
    # points_set = [(0, 10), (-10, -10), (10, 10), (10, 0), (-10, 0), (0, -10)]
    # points_set = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1)]
    points_set = [(0, 0), (20, 10), (20, 70), (60, 10), (60, 40), (70, 80), (75, 90), (80, 85), (80, 80), (80, 83)]

    kdtree = Kdtree(points_set)
    s = kdtree.find(x_low=10, x_high=100, y_low=20, y_high=80)
    print(s)

    # plot = simple_visualiser.Plot([simple_visualiser.PointsCollection(points_set),
    #                                simple_visualiser.PointsCollection(s, 'red', marker="x")])
    # plot.draw()
