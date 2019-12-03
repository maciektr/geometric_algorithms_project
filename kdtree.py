import numpy as np
from point import Point
from scope import Scope
import simple_visualiser


class Node:
    def __init__(self, point = None, line=None, left=None, right=None):
        self.point = Point(point) if point is not None else None
        self.line = line
        self.left = left
        self.right = right


def _construct(points, depth=0):
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
        left = _construct(left_slice, depth + 1),
        right = _construct(right_slice , depth + 1)
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
    # print("Check ", 'left' if child==node.left else 'right' , depth)
    if child is not None:
        new_scope = Scope()
        new_scope.copy(actual_scope)

        if depth % 2 == 0 and node.left == child:
            new_scope.common(x_high=node.line) #.point.x)
        elif depth % 2 == 1 and node.left == child:
            new_scope.common(y_high=node.line) #point.y)
        elif depth % 2 == 0 and node.right == child:
            new_scope.common(x_low=node.line) #point.x)
        else:
            new_scope.common(y_low=node.line) #point.y)

        if scope.contains(new_scope):
            return report_subtree(child)
        elif scope.intersects(new_scope):
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


def print_tree(node, depth=0):
    if node is None:
        return
    print_tree(node.left, depth + 1)
    print_tree(node.right, depth + 1)


def search(tree,actual_scope, x_low=-np.inf, x_high=np.inf, y_low=-np.inf, y_high=np.inf):
    scope = Scope(x_low, x_high, y_low, y_high)
    s = _search(tree, scope, actual_scope)
    return [p.get_tuple() for p in s]


def construct(points):
    k = len(points) // 2
    return _construct(points) , \
           Scope(min(points, key =lambda x:x[0])[0],
                 max(points, key =lambda x:x[0])[0],
                 min(points, key =lambda y:y[1])[1],
                 max(points, key =lambda y:y[1])[1])


if __name__ == '__main__':
    # points_set = [(0, 10), (-10, -10), (10, 10), (10, 0), (-10, 0), (0, -10)]
    # points_set = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1)]
    points_set = [(0, 0), (20, 10), (20, 70), (60, 10), (60, 40), (70, 80), (75, 90), (80, 85), (80, 80), (80, 83)]

    kdtree, act_scope = construct(points_set)
    s = search(kdtree,act_scope, x_low=10, x_high=100, y_low=20, y_high=80)
    print(s)

    plot = simple_visualiser.Plot([simple_visualiser.PointsCollection(points_set),
                                   simple_visualiser.PointsCollection(s, 'red', marker="x")])
    plot.draw()
