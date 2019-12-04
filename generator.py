#########################################
#      Algorytmy Grafowe 2019/2020      #
#      Generator danych testowych       #
#          Stanislaw Denkowski          #
#          Maciej Tratnowiecki          #
#########################################

# Import wykorzystywanych modulow
from random import randint


# Funkcja zwracajaca losowy zbior punktow o zadanych parametrach
def generate_points(n=1000, v=10 ** 9):
    return [(randint(-v, v), randint(-v, v)) for _ in range(n)]


def test_case_1():
    return [(0, 0), (20, 10), (20, 70), (60, 10), (60, 40), (70, 80), (75, 90), (80, 85), (80, 80), (80, 83)]


def test_case_2():
    return [(0, 10), (-10, -10), (10, 10), (10, 0), (-10, 0), (0, -10)]