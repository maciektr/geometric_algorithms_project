import numpy as np
from point import Point


class Node:
    def __init__(self, p, l=None, r=None):
        # self.point = (p[0], p[1])
        self.point = Point(p)
        self.left = l
        self.right = r


def _construct(points, depth=0):
    if len(points) < 1:
        return None
    if len(points) == 1:
        return Node(points[0])
    k = len(points) // 2
    np.partition(points, k, order='x' if depth % 2 == 0 else 'y')
    return Node(
        points[k],
        _construct(points[:k], depth + 1),
        _construct(points[k + 1:], depth + 1)
    )


def construct(points):
    k = len(points) // 2
    p = np.array(points, dtype=[('x', np.int), ('y', np.int)])
    return _construct(p)


def choose(var, val, fun):
    if val is not None:
        return fun(var, val)
    return var


class Scope:
    def __init__(self, xl=np.inf, xh=np.inf, yl=np.inf, yh=np.inf):
        self.x_low = xl
        self.x_high = xh
        self.y_low = yl
        self.y_high = yh

    def in_scope(self, point):
        return self.x_low <= point.x <= self.x_high and self.y_low <= point.y <= self.y_high

    def contains(self, other):
        return (self.x_low <= other.x_low
                and self.x_high >= other.x_high
                and self.y_low <= other.y_low
                and self.y_high >= other.y_high
                )

    def intersects(self, other):
        return ((self.x_low <= other.x_low <= self.x_high
                 or self.x_low <= other.x_high <= self.x_high)
                and (self.y_low <= other.y_low <= self.y_high
                     or self.y_low <= other.y_high <= self.y_high))

    def common(self, x_low=None, x_high=None, y_low=None, y_high=None):
        self.x_low = choose(self.x_low, x_low, max)
        self.y_low = choose(self.y_low, y_low, max)
        self.x_high = choose(self.x_high, x_high, min)
        self.y_high = choose(self.y_high, y_high, min)

    def copy(self, other):
        self.x_low = other.x_low
        self.x_high = other.x_high
        self.y_low = other.y_low
        self.y_high = other.y_high


def report_subtree(node):
    if node is None:
        return None
    result = [node.point]
    res = report_subtree(node.left)
    if res is not None:
        result += res
    res = report_subtree(node.right)
    if res is not None:
        result += res
    return result


def check_child(node, child, actual_scope, depth, scope):
    if child is not None:
        new_scope = Scope()
        new_scope.copy(actual_scope)
        if depth % 2 == 0 and node.left == child:
            new_scope.common(x_high=node.point.x)
        elif depth % 2 == 1 and node.left == child:
            new_scope.common(y_high=node.point.y)
        elif depth % 2 == 0 and node.right == child:
            new_scope.common(x_low=node.point.x)
        else:
            new_scope.common(y_low=node.point.x)

        if actual_scope.contains(new_scope):
            return report_subtree(child)
        elif actual_scope.intersects(new_scope):
            return _search(child, scope, new_scope, depth + 1)
        return None


def _search(node, scope, actual_scope=Scope(), depth=0):
    if node is None:
        return None
    if node.left is None and node.right is None:
        return None if not scope.in_scope(node.point) else [node.point]

    result = []
    res = check_child(node, node.left, actual_scope, depth, scope)
    if res is not None:
        result += res
    res = check_child(node, node.right, actual_scope, depth, scope)
    if res is not None:
        result += res
    return result


def search(tree, x_low, x_high, y_low, y_high):
    scope = Scope(x_low, x_high, y_low, y_high)
    res = [tree.point.get_tuple()] if scope.in_scope(tree.point) else []
    return res + [p.get_tuple() for p in _search(tree, scope)]


def print_tree(node, depth=0):
    if node is None:
        return
    print("depth ", depth, " - ", node.point.get_tuple())
    print_tree(node.left, depth+1)
    print_tree(node.right, depth+1)


if __name__ == '__main__':
    points_set = [(0, 10), (-10, -10), (10, 10), (10, 0), (-10, 0), (0, -10)]
    # tree = construct(list(map(Point.point_from_tuple, points_set)))
    # points_set = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1)]
    kdtree = construct(points_set)
    print(points_set)
    print(len(points_set))
    s = search(kdtree, -np.inf, np.inf, -np.inf, np.inf)
    print(s)
    print(len(s))

    # t = report_subtree(kdtree)
    # print([(p.x, p.y) for p in t])
    # print(len(t))
    # print_tree(kdtree)
