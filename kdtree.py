import numpy as np
from point import Point
from scope import Scope
# import generator
import simple_visualiser

class Node:
    def __init__(self, p, left=None, right=None):
        self.point = Point(p)
        self.left = left
        self.right = right


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
        _construct(points[k:], depth + 1)
    )


def report_subtree(node):
    if node is None:
        return None
    if node.left is None and node.right is None:
        return [node.point]
    result = []
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
            new_scope.common(y_low=node.point.y)

        # print("Node : ", node.point.get_tuple())
        # print("Scope: ", scope.x_low, scope.x_high)
        # print("Actua: ", actual_scope.x_low, actual_scope.x_high)
        # print("New_s: ", new_scope.x_low, new_scope.x_high)
        if scope.contains(new_scope):
            return report_subtree(child)
        elif scope.intersects(new_scope):
            print("Y")
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
    # print("B ",  [p.get_tuple() for p in res])
    return result


def print_tree(node, depth=0):
    if node is None:
        return
    print("depth ", depth, " - ", node.point.get_tuple())
    print_tree(node.left, depth + 1)
    print_tree(node.right, depth + 1)


def search(tree, x_low=-np.inf, x_high=np.inf, y_low=-np.inf, y_high=np.inf):
    scope = Scope(x_low, x_high, y_low, y_high)
    return [p.get_tuple() for p in _search(tree, scope)]


def construct(points):
    k = len(points) // 2
    p = np.array(points, dtype=[('x', np.int), ('y', np.int)])
    return _construct(p)


if __name__ == '__main__':
    points_set = [(0, 10), (-10, -10), (10, 10), (10, 0), (-10, 0), (0, -10)]
    # points_set = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1)]

    kdtree = construct(points_set)
    s = search(kdtree, x_low=-2, x_high=2)
    print(s)

    plot = simple_visualiser.Plot([simple_visualiser.PointsCollection(points_set),
                     simple_visualiser.PointsCollection(s, 'red', marker="x")])
    plot.draw()


    # print_tree(kdtree)
    # nie dziala xD