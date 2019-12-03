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
