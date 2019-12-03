from enum import Enum
import numpy as np


class Child(Enum):  # enumeracja, dla łatwiejszego zarządzania synami node'a
    NE = 0
    NW = 1
    SE = 2
    SW = 3


class Point:  # Klasa, dla łatwiejszego zarządzania punktami
    def __init__(self, x, y):  # Inicjalizacja punktów
        self.x = x
        self.y = y

    def __str__(self):  # Wypisywanie w sensowny sposób
        return ':' + ' (' + str(self.x) + ', ' + str(self.y) + ')'

    def in_range(self, lowerleft, upperright):  # sprawdzenie czy punkt znajduje się w zadanym obszarze
        return lowerleft.x <= self.x <= upperright.x and lowerleft.y <= self.y <= upperright.y

    def get_tuple(self):  # zwracanie punkty w formacie przyjmowanym przez wizualizację
        return tuple([self.x,   self.y])


class Node:  # Klasa, dla łatwiejszego zarządzania konkretnymi node'ami qudatree
    # Dla każdego node'a pamiętamy obszar jaki on obejmuje, wartości ułatwiające podział noda na 4 dzieci
    # Lista dzieci i licznik pamiętający ich liczbę dla łatwiejszego zarządzania
    # Punkt, jeżeli jesteśmy w liściu  i akurat jakiś Point znajduje się w naszym obszarze
    def __init__(self, n=100, w=0, s=0, e=100, par=None, typ=-1):  # Inicjalizacja node'a
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

    def add_kid(self, nr, other):  # Metoda dodająca konkretne dziecko danemu node'owi i zwiększające licznik dzieci
        if type(nr) != int:
            nr = nr.value
        self.kids[nr] = other
        self.kidscount += 1

    def get_kid(self, nr):  # Metoda zwracająca konkretne dziecko danego node'a
        if type(nr) != int:
            nr = nr.value
        return self.kids[nr]

    def __str__(self):  # Wypisywania w sensowny sposób
        return 'N: ' + str(self.north) + ' W: ' + str(self.west) + ' S: ' + str(self.south) + ' E: ' + str(self.east) + \
               ' Kids: ' + str(self.kidscount) + ' Point:' + str(self.point)


def create_kids(node, points):  # Funkcja, konieczna przy inicjalizacji quadtree, dzieląca punkty i tworząca node'y
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


def _get_lines(node, sol):  # Funkcja konieczna przy wizualizacji, aby wyświetlić obszary obejmowane przez liście
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


class QuadTree:  # Klasa, dla łatiwejszego zarządzania quadtree
    def __init__(self, pkts):  # Inicjalizacja quadtree, stworzenie drzewa i pamiętanie root'a
        points = [Point(x[0], x[1]) for x in pkts]
        _, n = max(pkts, key=lambda x: x[1])
        _, s = min(pkts, key=lambda x: x[1])
        e, _ = max(pkts, key=lambda x: x[0])
        w, _ = min(pkts, key=lambda x: x[0])
        self.root = Node(n, w, s, e, None)
        create_kids(self.root, points)

    def _find_points(self, lowerleft, upperright, solution, tree=None):  # Funkcja wewnętrzna zwracająca listę pkt
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

    def find(self, x_low=-np.inf, x_high=np.inf, y_low=-np.inf, y_high=np.inf):  # Funkcja zewnętrzna, zwracająca listę
        lowerleft = Point(x_low, y_low)                                          # punktów w będących w zadanym obszarze
        upperright = Point(x_high, y_high)
        solution = set([])
        self._find_points(lowerleft, upperright, solution)
        # print(p)
        return list(map(Point.get_tuple, solution))

    def get_lines(self):  # Funkcja zwracająca linie potrzebne do wizualizacji
        sol = []
        _get_lines(self.root, sol)
        return sol

    def get_lines(self):  # Funkcja zwracająca linie potrzebne do wizualizacji
        sol = []
        _get_lines(self.root, sol)
        return sol


def druk(quad, depth=0):  # Funkcja przydatna przy debugowaniu, drukująca całe quadtree w miarę czytelny sposób
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


def get_points(_=0):  # Funkcja służąca do uzyskiwania punktów - wykorzystywana przy testowaniu
    if _==0:
        # return [Point(0, 0), Point(20, 10), Point(20, 70), Point(60, 10), Point(60, 40), Point(70, 80), Point(75, 90),
        #         Point(80, 85), Point(80, 80), Point(80, 83)]
        return [(0, 0), (20, 10), (20, 70), (60, 10), (60, 40), (70, 80), (75, 90), (80, 85), (80, 80), (80, 83)]
    else:
        return []


if __name__=='__main__':
    pkts = get_points(0)
    for pkt in pkts:
        print(pkt)

    quad = QuadTree(pkts)
    #druk(quad.root)

    solution = quad.find(0, 100, 0, 100)
    print('Solution:')
    for point in solution:
        print(point)
    print(len(solution))

    lines = quad.get_lines()

    #print('Lines:')
    #for line in lines:
    #    print(line)

# TODO Better input
# TODO Visualization

