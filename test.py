#########################################
#      Algorytmy Grafowe 2019/2020      #
#    Integracyjne testy automatyczne    #
#          Stanislaw Denkowski          #
#          Maciej Tratnowiecki          #
#########################################

# Import wykorzystywanych modulow
import generator
import kdtree
import quadtree
from random import randint

if __name__=='__main__':
    test = generator.generate_points(100)
    kd = kdtree.Kdtree(test)
    quad = quadtree.QuadTree(test)

    v = 1000
    while True:
        xl = randint(-v,v)
        xh = randint(-v,v)
        yl = randint(-v,v)
        yh = randint(-v,v)

        s1 = kd.find(xl,xh,yl,yh)
        s2 = quad.find(xl,xh,yl,yh)

        if set(s1) != set(s2):
            print("ERROR!")
            print(test)
            break
        print("OK")