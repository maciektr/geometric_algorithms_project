#########################################
#      Algorytmy Grafowe 2019/2020      #
#               QuadTree                #
#          Stanislaw Denkowski          #
#          Maciej Tratnowiecki          #
#########################################

# Import wykorzystywanych modulow
from enum import Enum
import numpy as np
from simple_geometry import *


# Typ wyliczeniowy ulatwiajacy zarzadzanie poddrzewami w wezle drzewa
class Child(Enum):
    NE = 0
    NW = 1
    SE = 2
    SW = 3


# Klasa reprezentujaca wezel w QuadTree
class Node:
    # Konstruktor klasy
    # Kazdy wezel przechowuje:
    #   * Obszar, jaki reprezentuje
    #   * Wartosci ulatwiające podzial wezla na 4 poddrzewa
    #   * Lista poddrzew
    #   * Licznik poddrzew
    #   * Punkt, jesli wezel jest liscie  i akurat istnieje punkt znajdujacy sie w przechowywanym obszarze
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

    # Metoda dodajaca poddrzewo do wezla
    def add_kid(self, nr, other):
        if type(nr) != int:
            nr = nr.value
        self.kids[nr] = other
        self.kidscount += 1

    # Metoda zwracajaca poddrzewo o zadanym indeksie
    def get_kid(self, nr):
        if type(nr) != int:
            nr = nr.value
        return self.kids[nr]

    # Funkcja zwracajaca reprezentacje instancji klasy w formie lancucha znakow
    def __str__(self):
        return 'N: ' + str(self.north) + ' W: ' + str(self.west) + ' S: ' + str(self.south) + ' E: ' + str(self.east) + \
               ' Kids: ' + str(self.kidscount) + ' Point:' + str(self.point)


# Funkcja wykorzystywana przy inicjalizacji QuadTree
# Dzieli punkty i tworzy wezly
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


# Funkcja konieczna przy wizualizacji, aby wyświetlić obszary obejmowane przez liście
def _get_lines(node, sol):
    if node.kidscount!=0:
        _get_lines(node.get_kid(Child.NE.value), sol)
        _get_lines(node.get_kid(Child.NW.value), sol)
        _get_lines(node.get_kid(Child.SE.value), sol)
        _get_lines(node.get_kid(Child.SW.value), sol)
    else:
        sol += [[(node.east, node.north), (node.west, node.north)]]
        sol += [[(node.west, node.north), (node.west, node.south)]]
        sol += [[(node.west, node.south), (node.east, node.south)]]
        sol += [[(node.east, node.south), (node.east, node.north)]]


# Klasa enkapsulujaca implementacje QuadTree
class QuadTree:
    # Konstruktor klasy
    # Instancja przechowuje korzen drzewa
    def __init__(self, pkts):
        points = [Point(x) for x in pkts]
        _, n = max(pkts, key=lambda x: x[1])
        _, s = min(pkts, key=lambda x: x[1])
        e, _ = max(pkts, key=lambda x: x[0])
        w, _ = min(pkts, key=lambda x: x[0])
        self.root = Node(n, w, s, e, None)
        create_kids(self.root, points)

    # Funkcja pomocnicza realizujaca przeszukiwanie obszaru
    def _find_points(self, lowerleft, upperright, solution, tree=None):
        if tree is None:
            tree = self.root
        if lowerleft.x > tree.east or lowerleft.y > tree.north or upperright.x < tree.west or upperright.y < tree.south:
            return
        if tree.kidscount==0:
            if tree.point is not None and Scope().from_tuple(lowerleft,upperright).in_scope(tree.point):
                solution.add(tree.point)
            return
        for kid in tree.kids:
            self._find_points(lowerleft, upperright, solution, kid)

    # Funkcja implementujaca algorytm przeszukania QuadTree
    def find(self, x_low=-np.inf, x_high=np.inf, y_low=-np.inf, y_high=np.inf):
        lowerleft = Point((x_low, y_low))
        upperright = Point((x_high, y_high))
        solution = set([])
        self._find_points(lowerleft, upperright, solution)
        # print(p)
        return list(map(Point.get_tuple, solution))

    # Funkcja pomocnicza wykorzystywana przy wizualizacji
    def get_lines(self):
        sol = []
        _get_lines(self.root, sol)
        return sol


# Funkcja wypisujaca tekstowa reprezentacje stanu QuadTree
# Nie jest wykorzystywana w implementacji drzewa
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


# Ponizszy kod nie jest wykorzystywany w implementacji drzewa
if __name__=='__main__':
    pkts = [(0, 0), (20, 10), (20, 70), (60, 10), (60, 40), (70, 80), (75, 90), (80, 85), (80, 80), (80, 83)]
    for pkt in pkts:
        print(pkt)

    quad = QuadTree(pkts)
    solution = quad.find(0, 100, 0, 100)
    print('Solution:')
    for point in solution:
        print(point)
    print(len(solution))
    lines = quad.get_lines()
