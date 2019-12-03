from random import randint


def generate_points(n=1000, v=10 ** 9):
    return [(randint(-v, v), randint(-v, v)) for _ in range(n)]
