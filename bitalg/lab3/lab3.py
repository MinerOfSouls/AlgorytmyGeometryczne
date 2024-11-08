import matplotlib.pyplot as plt
import numpy as np
import time
from bitalg.tests.test3 import Test

def give_figure():
    E=input("Podaj ilość wierzchołków w wielokącie: ")
    def tellme(s):
        print(s)
        plt.title(s, fontsize=16)
        plt.draw()

    plt.figure()
    plt.xlim(0, 50)
    plt.ylim(0, 50)
    tellme('Proszę nayrsować wielokąt, kliknij aby zacząć')
    plt.waitforbuttonpress()

    pts = []
    tellme('Narysuj wielokąt')
    pts = np.asarray(plt.ginput(E))
    ph = plt.fill(pts[:, 0], pts[:, 1], 'r', lw=2)
    tellme('Czy dobry wielokąt?')
    plt.waitforbuttonpress()
    for p in ph:
        p.remove()
    return pts

def is_y_monotonic(Polygon):
    max_y=max([Polygon[i][1] for i in range(len(Polygon))])
    starti=0;
    for i in range(len(Polygon)):
        if max_y==Polygon[i][1]:
            starti=i
            break
    prev = starti
    loop = starti + 1
    if starti == len(Polygon) - 1:
        prev = starti
        loop = 0
    while loop!=starti:
        if Polygon[prev][0]>Polygon[loop][0] or Polygon[prev][1]>Polygon[loop][1]:
            prev = loop
            if loop==len(Polygon)-1:
                loop=0
            else:
                loop+=1
        else:
            return False
    return True

Test().runtest(1, is_y_monotonic)

input()