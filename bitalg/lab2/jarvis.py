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
def orient(a,b,c):
    return (a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0])

def better_sorter(Q,startpoint):
    comparisonpoint = startpoint
    def mycmp(a,b):
        nonlocal comparisonpoint
        if orient(comparisonpoint,b,a)>0:
            return 1
        return -1
    Q.sort(key=cmp_to_key(mycmp))
    result=Q[0]
    i=1
    while i<len(Q) and orient(startpoint, result, Q[i]) == 0:
        if ((((Q[i][0] - startpoint[0])** 2) + ((Q[i][1] - startpoint[1]) ** 2)) >
                (((result[0] - startpoint[0]) ** 2) + ((result[1] - startpoint[0]) ** 2))):
            result = Q[i]
        i+=1
    return result

def jarvis_algorithm(Q):
    if len(Q)<4:
        return Q
    mini = 0
    for i in range(len(Q)):
        if Q[i][1]<Q[mini][1]:
            mini = i
        elif Q[i][1]==Q[mini][1] and Q[i][0]<Q[mini][0]:
            mini = i
    startpoint = (Q[mini][0],Q[mini][1])
    nextpoint=better_sorter(Q,startpoint)
    hull=[startpoint]
    while nextpoint!=startpoint:
        hull.append(nextpoint)
        nextpoint=better_sorter(Q,nextpoint)
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
    nextpoint=better_sorter(Q,startpoint)
    hull=[startpoint]
    visstack.append(vis.add_line_segment((startpoint,nextpoint),color="orange"))
    while nextpoint!=startpoint:
        hull.append(nextpoint)
        nextpoint=better_sorter(Q,nextpoint)
        visstack.append(vis.add_line_segment((hull[len(hull)-1],nextpoint),color="orange"))
    vis.show()
    return hull

Test().runtest(2, jarvis_algorithm_draw)