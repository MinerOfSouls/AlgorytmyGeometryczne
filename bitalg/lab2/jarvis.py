from turtledemo.penrose import start

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from functools import cmp_to_key
from PIL.ImageChops import difference
from matplotlib.pyplot import inferno
from notebook_shim.nbserver import diff_members
import random as random
import math as math

sys.path.append('C:/Users/franc/Documents/AlgorytmyGeometryczne')
from bitalg.tests.test2 import Test
from bitalg.visualizer.main import Visualizer

def generate_circle_points(O, R, n=100):
    """
    Funkcja generuje jednostajnie n punktów na okręgu o środku O i promieniu R
    :param O: krotka współrzędnych x, y określająca środek okręgu
    :param R: promień okręgu
    :param n: ilość generowanych punktów
    :return: tablica punktów w postaci krotek współrzędnych
    """
    points=[None for _ in range(n)]
    for i in range(n):
        angle=random.random()*(2*math.pi)
        points[i]=(O[0]+(math.sin(angle)*R),O[1]+(math.cos(angle)*R))
    return points


def generate_rectangle_points(a=(-10, -10), b=(10, -10), c=(10, 10), d=(-10, 10), n=100):
    '''
    Funkcja generuje n punktów na obwodzie prostokąta
    o wierzchołkach w punktach a, b, c i d
    :param a: lewy-dolny wierzchołek prostokąta
    :param b: prawy-dolny wierzchołek prostokąta
    :param c: prawy-górny wierzchołek prostokąta
    :param d: lewy-górny wierzchołek prostokąta
    :param n: ilość generowanych punktów
    :return: tablica punktów w postaci krotek współrzędnych
    '''
    points = []
    for i in range(n):
        side = random.randint(0, 4)
        if side == 0:
            points.append((random.uniform(a[0], b[0]), -10))
        elif side == 1:
            points.append((10, random.uniform(b[1], c[1])))
        elif side == 2:
            points.append((random.uniform(d[0], c[0]), 10))
        elif side == 3:
            points.append((-10, random.uniform(a[1], d[1])))

    return points


def orient(a,b,c):
    return (a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0])
def distance(a,b):
    return ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)

#np.arctan2(A[1]-B[1],A[0]-B[0])
def angle_sorter(Q,startpoint):
    def mycmp(a, b):
        nonlocal startpoint
        if orient(startpoint, b, a) > 0:
            return 1
        elif orient(startpoint, b, a) == 0:
            return 0
        return -1

    Q.sort(key=cmp_to_key(mycmp))
    result = Q[0]
    i = 1
    to_remove = []
    while i < len(Q) and orient(startpoint, result, Q[i]) == 0:
        if distance(Q[i],startpoint)>distance(result,startpoint):
            result = Q[i]
        else:
            to_remove.append(Q[i])
        i += 1
    for point in to_remove:
        Q.remove(point)
    return result

def jarvis_algorithm(Q):
    if len(Q) < 4:
        return Q
    mini = 0
    for i in range(len(Q)):
        if Q[i][1] < Q[mini][1]:
            mini = i
        elif Q[i][1] == Q[mini][1] and Q[i][0] < Q[mini][0]:
            mini = i
    startpoint = (Q[mini][0], Q[mini][1])
    nextpoint = angle_sorter(Q, startpoint)
    hull = [startpoint]
    while nextpoint != startpoint:
        hull.append(nextpoint)
        Q.remove(nextpoint)
        nextpoint = angle_sorter(Q, nextpoint)
    return hull

def jarvis_algorithm_draw(Q):
    if len(Q)<4:
        return Q
    mini = 0
    for i in range(len(Q)):
        if Q[i][1]<Q[mini][1]:
            mini = i
        elif Q[i][1]==Q[mini][1] and Q[i][0]<Q[mini][0]:
            mini = i
    vis=Visualizer()
    vis.add_point(Q)
    visstack=[]
    startpoint = (Q[mini][0],Q[mini][1])
    nextpoint=angle_sorter(Q,startpoint)
    hull=[startpoint]
    visstack.append(vis.add_line_segment((startpoint,nextpoint),color="orange"))
    while nextpoint!=startpoint:
        hull.append(nextpoint)
        Q.remove(nextpoint)
        nextpoint=angle_sorter(Q,nextpoint)
        visstack.append(vis.add_line_segment((hull[len(hull)-1],nextpoint),color="orange"))

    return (hull,vis)

a,b=jarvis_algorithm_draw(generate_rectangle_points())
print(a,b)