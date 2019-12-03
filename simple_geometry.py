#########################################
#      Algorytmy Grafowe 2019/2020      #
#           Klasy pomocnicze            #
#          Stanislaw Denkowski          #
#          Maciej Tratnowiecki          #
#########################################

# Import wykorzystywanych modulow
import numpy as np


# Klasa przechowujaca obszar prostokatny w pamieci
class Scope:
    # Konstruktor klasy
    def __init__(self, xl=-np.inf, xh=np.inf, yl=-np.inf, yh=np.inf):
        self.x_low = xl
        self.x_high = xh
        self.y_low = yl
        self.y_high = yh

    # Funkcja zwracajaca reprezentacje instancji klasy w formie lancucha znakow
    def __str__(self):
        return '('+str(self.x_low)+', '+str(self.x_high)+', '+str(self.y_low)+', '+str(self.y_high)+')'

    # Funkcja przyjmujaca przedzial jako pare krotek
    def from_tuple(self, lowerleft, upperright):
        self.x_low = lowerleft.x
        self.x_high = upperright.x
        self.y_low = lowerleft.y
        self.y_high = upperright.y
        return self

    # Funkcja sprawdzajaca czy punkt podany jako argument nalezy do przechowywanego przedzialu
    def in_scope(self, point):
        return self.x_low <= point.x <= self.x_high and self.y_low <= point.y <= self.y_high

    # Funkcja sprawdzajaca, czy dwa obszary sie w sobie zawieraja
    def contains(self, other):
        return (self.x_low <= other.x_low
                and self.x_high >= other.x_high
                and self.y_low <= other.y_low
                and self.y_high >= other.y_high
                )

    # Funkcja sprawdzajaca czy dwa obszary sie przecinaja
    def intersects(self, other):
        if self.x_low > other.x_high or other.x_low > self.x_high:
            return False

        if self.y_low > other.y_high or other.y_low > self.y_high:
            return False

        return True

    # Funkcja realizujaca operacje przeciecia obszaru z polplaszczyzna
    def common(self, x_low=None, x_high=None, y_low=None, y_high=None):
        if x_low is not None:
            self.x_low = max(self.x_low, x_low)
        if x_high is not None:
            self.x_high = min(self.x_high, x_high)
        if y_low is not None:
            self.y_low = max(self.y_low, y_low)
        if y_high is not None:
            self.y_high = min(self.y_high, y_high)

    # Funkcja kopiujaca zawartosc innej instancji klasy
    def copy(self, other):
        self.x_low = other.x_low
        self.x_high = other.x_high
        self.y_low = other.y_low
        self.y_high = other.y_high


# Klasa przechowujaca punkt na dwuwymiarowej plaszczyznie euklidesowej w pamieci
class Point:
    def __init__(self, s):
        self.x = s[0]
        self.y = s[1]

    # Funkcja zwracajaca punkt w postaci dwuelementowej krotki
    def get_tuple(self):
        return tuple([self.x, self.y])

    # Funkcja zwracajaca reprezentacje instancji klasy w formie lancucha znakow
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
