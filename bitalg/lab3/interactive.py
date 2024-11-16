
import matplotlib.pyplot as plt
import numpy as np
import time


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

A=[]

for i in range(10):
    tmp = give_figure()
    A.append(tmp.tolist())

print(A)