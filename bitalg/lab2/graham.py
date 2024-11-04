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

def sorter(Q,startpoint):
    swaps = True
    while swaps:
        swaps = False
        for i in range(1,len(Q)):
            if orient(startpoint,Q[i],Q[i-1])>0:
                Q[i-1], Q[i] = Q[i], Q[i-1]
                swaps=True
    building=[]
    building.append(Q[0])
    b=0
    for i in range(1,len(Q)):
        if orient(startpoint,building[b],Q[i])==0:
            if ((Q[i][0]**2) + (Q[i][1]**2))>((building[b][0]**2)+(building[b][1]**2)):
                building[b]=Q[i]
        else:
            building.append(Q[i])
            b+=1
    return building

def better_sorter(Q,startpoint):
    comparisonpoint = startpoint
    def mycmp(a,b):
        nonlocal comparisonpoint
        if orient(comparisonpoint,b,a)>0:
            return 1
        return -1
    Q.sort(key=cmp_to_key(mycmp))
    building = []
    building.append(Q[0])
    b = 0
    for i in range(1, len(Q)):
        if orient(startpoint, building[b], Q[i]) == 0:
            if ((((Q[i][0] - startpoint[0]) ** 2) + ((Q[i][1] - startpoint[1]) ** 2)) >
                    (((building[b][0] - startpoint[0]) ** 2) + ((building[b][1] - startpoint[1]) ** 2))):
                building[b] = Q[i]
        else:
            building.append(Q[i])
            b += 1
    return building


def sidetest(Stack,sorted,i):
    if len(Stack)<2:
        return False
    return orient(Stack[len(Stack)-2],sorted[i],Stack[len(Stack)-1])>=0

def graham_algorithm(Q):
    if len(Q)<4:
        return Q
    mini = 0
    for i in range(len(Q)):
        if Q[i][1]<Q[mini][1]:
            mini = i
        elif Q[i][1]==Q[mini][1] and Q[i][0]<Q[mini][0]:
            mini = i
    startpoint = (Q[mini][0],Q[mini][1])
    Q.pop(mini)
    sorted=better_sorter(Q,startpoint)
    if len(sorted)<2:
        tmp=[startpoint]
        tmp.extend(sorted)
        return tmp
    Stack=[]
    Stack.append(startpoint)
    Stack.append(sorted[0])
    Stack.append(sorted[1])
    i=2
    while i<len(sorted):
        while sidetest(Stack,sorted, i):
            Stack.pop()
        Stack.append(sorted[i])
        i +=1
    return Stack

def graham_algorithm_draw(Q):
    vis=Visualizer()
    vis.add_point(Q)
    if len(Q)<4:
        return Q
    mini = 0
    for i in range(len(Q)):
        if Q[i][1]<Q[mini][1]:
            mini = i
        elif Q[i][1]==Q[mini][1] and Q[i][0]<Q[mini][0]:
            mini = i
    startpoint = (Q[mini][0],Q[mini][1])
    Q.pop(mini)
    sorted=better_sorter(Q,startpoint)
    if len(sorted)<2:
        tmp=[startpoint]
        tmp.extend(sorted)
        return tmp
    vis.add_point(startpoint,color="orange")
    vis.add_point(sorted,color="orange")
    Stack=[]
    Stack.append(startpoint)
    Stack.append(sorted[0])
    Stack.append(sorted[1])
    visstack=[]
    tmp=vis.add_line_segment((startpoint,sorted[0]))
    visstack.append(tmp)
    tmp=vis.add_line_segment((sorted[0],sorted[1]))
    visstack.append(tmp)
    i=2
    while i<len(sorted):
        while sidetest(Stack,sorted, i):
            Stack.pop()
            vis.remove_figure(visstack.pop())
        Stack.append(sorted[i])
        tmp=vis.add_line_segment((Stack[len(Stack)-2],Stack[len(Stack)-1]))
        visstack.append(tmp)
        i +=1
    vis.show()
    return Stack

Test().runtest(1, graham_algorithm_draw)