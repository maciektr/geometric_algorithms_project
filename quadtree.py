from enum import Enum


class Child(Enum):
    NE = 0
    NW = 1
    SE = 2
    SW = 3
    # SW = 2
    # SE = 3


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


# TODO Test Node
class Node:
    def __init__(self, n=100, w=0, s=0, e=100, par=None, type=-1):
        self.parent = par
        self.north = n
        self.west = w
        self.east = e
        self.south = s
        self.midx = (self.east+self.west)/2
        self.midy = (self.north+self.south)/2
        self.kids = [None for i in range(4)]
        self.point = None
        self.type = type
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


def create_kids(node, points):
    if len(points) < 2:
        node.point = points[0]
    if len(points) < 1:
        return

    ne = Node(node.north, node.midx, node.midy, node.east, par=node, type=Child.NE.value)
    nw = Node(node.north, node.west, node.midy, node.midx, par=node, type=Child.NW.value)
    sw = Node(node.midy, node.west, node.south, node.midx, par=node, type=Child.SW.value)
    se = Node(node.midy, node.midx, node.south, node.east, par=node, type=Child.SE.value)

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


# TODO Test QuadTree init and neighbours
class QuadTree:
    def __init__(self, points, n=100, w=0, s=0, e=100):
        self.root = Node(n, w, s, e, None)
        create_kids(self.root, points)

    def south_neighbour(self, node):
        if node == self.root:
            return None
        if node.type in {Child.NE.value, Child.NW.value}:
            ancestor = node.parent.get_kid(node.type+2)
            while ancestor.kidscount != 0:
                ancestor = ancestor.get_kid(node.type)
            return ancestor

        ancestor = self.south_neighbour(node.parent)
        if ancestor is None or ancestor.kidscount == 0:
            return ancestor
        while ancestor.kidscount != 0:
            ancestor = ancestor.get_kid(node.type-2)

        # if node.type == Child.SE.value:
        #     while ancestor.kidscount != 0:
        #         ancestor = ancestor.get_kid(Child.NE.value)
        #     return ancestor
        # while ancestor.kidscount != 0:
        #     ancestor = ancestor.get_kid(Child.NW.value)

    def west_neighbour(self, node):
        if node == self.root:
            return None
        if node.type in {Child.NE.value, Child.SE.value}:
            ancestor = node.parent.get_kid(node.type+1)
            while ancestor.kidscount != 0:
                ancestor = ancestor.get_kid(node.type)
            return ancestor

        ancestor = self.west_neighbour(node.parent)
        if ancestor is None or ancestor.kidscount == 0:
            return ancestor
        while ancestor.kidscount != 0:
            ancestor = ancestor.get_kid(node.type-1)


def get_points(_=0):
    if _==0:
        return [Point(0, 0), Point(20, 10), Point(20, 70), Point(60, 10), Point(60, 40), Point(70, 80), Point(75, 90),
                Point(80, 85), Point(80, 80), Point(80, 83)]
    else:
        return []


pkts = get_points(0)
for pkt in pkts:
    print(pkt)

# TODO Find points in range -> start upperright and go down from each left neighbour until out of range

