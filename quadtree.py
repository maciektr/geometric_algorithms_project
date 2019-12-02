from enum import Enum
import numpy as np

class Child(Enum):
    NE = 0
    NW = 1
    SE = 2
    SW = 3


class Point:
    nr = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nr = Point.nr
        Point.nr += 1

    def __str__(self):
        return str(self.nr) + ':' + ' (' + str(self.x) + ', ' + str(self.y) + ')'

    def in_range(self, lowerleft, upperright):
        return lowerleft.x <= self.x <= upperright.x and lowerleft.y <= self.y <= upperright.y

    def get_tuple(self):
        return tuple([self.x,   self.y])


class Node:
    def __init__(self, n=100, w=0, s=0, e=100, par=None, typ=-1):
        self.parent = par
        self.north = n
        self.west = w
        self.east = e
        self.south = s
        self.midx = (self.east+self.west)/2
        self.midy = (self.north+self.south)/2
        self.kids = [None for i in range(4)]
        self.point = None
        self.type = typ
        self.kidscount = 0

    def add_kid(self, nr, other):
        if type(nr) != int:
            nr = nr.value
        self.kids[nr] = other
        self.kidscount += 1

    def get_kid(self, nr):
        if type(nr) != int:
            nr = nr.value
        return self.kids[nr]

    def __str__(self):
        return 'N: ' + str(self.north) + ' W: ' + str(self.west) + ' S: ' + str(self.south) + ' E: ' + str(self.east) + \
               ' Kids: ' + str(self.kidscount) + ' Point:' + str(self.point)


def create_kids(node, points):
    if 0 < len(points) < 2:
        node.point = points[0]
    if len(points) < 2:
        return

    ne = Node(node.north, node.midx, node.midy, node.east, par=node, typ=Child.NE.value)
    nw = Node(node.north, node.west, node.midy, node.midx, par=node, typ=Child.NW.value)
    sw = Node(node.midy, node.west, node.south, node.midx, par=node, typ=Child.SW.value)
    se = Node(node.midy, node.midx, node.south, node.east, par=node, typ=Child.SE.value)

    node.add_kid(Child.NE.value, ne)
    node.add_kid(Child.NW.value, nw)
    node.add_kid(Child.SW.value, sw)
    node.add_kid(Child.SE.value, se)

    tabne = [point for point in points if point.x>node.midx and point.y>node.midy]
    tabnw = [point for point in points if point.x<=node.midx and point.y>node.midy]
    tabsw = [point for point in points if point.x<=node.midx and point.y<=node.midy]
    tabse = [point for point in points if point.x>node.midx and point.y<=node.midy]

    create_kids(ne, tabne)
    create_kids(nw, tabnw)
    create_kids(sw, tabsw)
    create_kids(se, tabse)


class QuadTree:
    def __init__(self, points, n=100, w=0, s=0, e=100):
        self.root = Node(n, w, s, e, None)
        create_kids(self.root, points)

    def _find_points(self, lowerleft, upperright, solution, tree=None):
        if tree is None:
            tree = self.root
        if lowerleft.x > tree.east or lowerleft.y > tree.north or upperright.x < tree.west or upperright.y < tree.south:
            return
        if tree.kidscount==0:
            if tree.point is not None and tree.point.in_range(lowerleft, upperright):
                solution.add(tree.point)
            return
        for kid in tree.kids:
            self._find_points(lowerleft, upperright, solution, kid)

    def find_points(self, lowerleft, upperright):
        solution = set([])
        self._find_points(lowerleft,upperright,solution)
        return solution

    def find(self, x_low = -np.inf, x_high=np.inf, y_low=-np.inf, y_high=np.inf):
        lowerleft = Point(x_low, y_low)
        upperright = Point(x_high, y_high)
        p = self.find_points(lowerleft, upperright)
        # print(p)
        return list(map(Point.get_tuple, p))


def druk(quad, depth=0):
    if quad is None:
        return
    print(depth, ': N=', quad.north, ' W=', quad.west, ' S=', quad.south, ' E=', quad.east, ' Type=', quad.type,
          ' Kids=', quad.kidscount, end='')
    if quad.point is not None:
        print(' Point=', quad.point)
    else:
        print()
    for i in quad.kids:
        druk(i, depth+1)


def get_points(_=0):
    if _==0:
        return [Point(0, 0), Point(20, 10), Point(20, 70), Point(60, 10), Point(60, 40), Point(70, 80), Point(75, 90),
                Point(80, 85), Point(80, 80), Point(80, 83)]
    else:
        return []


if __name__=='__main__':
    pkts = get_points(0)
    for pkt in pkts:
        print(pkt)

    quad = QuadTree(pkts)
    #druk(quad.root)


    lowerleft = Point(0, 0)
    upperright = Point(100, 100)

    solution = set([])
    quad.find_points(lowerleft, upperright, solution)

    print('Solution:')
    for point in solution:
        print(point)
    print(len(solution))

# TODO Better input
# TODO Visualization

