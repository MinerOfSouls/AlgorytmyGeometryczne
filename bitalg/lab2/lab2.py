import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from functools import cmp_to_key
from PIL.ImageChops import difference
from matplotlib.pyplot import inferno
from notebook_shim.nbserver import diff_members
sys.path.append('C:/Users/franc/Documents/AlgorytmyGeometryczne')
from bitalg.tests.test2 import Test
from bitalg.visualizer.main import Visualizer
import random as random
import math as math

def owncmp(a,b):
    if a[0]<b[0]:
        return -1
    if a[0]==b[0]:
        if b[1]>a[1]:
            return 1
        else:
            return -1
    return 1

def angle_bettwen(A,B):
    if A==B: return -1
    return np.arctan2(A[1]-B[1],A[0]-B[0])

def special_unique(list):
    building=[]
    building.append(list[0])
    for i in range(1, len(list)):
        if list[i][0] != list[i-1][0]:
            building.append(list[i])
    return building

def orient(a,b,c):
    return (a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0])

def pointcheck(Stack,sortedpoints,i,stacklen):
    if stacklen<1:
        return False
    return orient((sortedpoints[i][2], sortedpoints[i][3]),Stack[stacklen - 2], Stack[stacklen - 1]) > 0

def graham_algorithm(Q):
    if len(Q)<4:
        return Q
    Stack=[]
    mini=(math.inf,math.inf)
    for i in Q:
        if i[1]<mini[1]:
            mini=(i[0],i[1])
    for i in Q:
        if i[1]==mini[1] and i[0]<mini[0]:
            mini=i
    sortedpoints=[]
    for point in Q:
        sortedpoints.append((angle_bettwen(point,mini),(point[0]-mini[0])**2 + (point[1]-mini[1])**2,point[0],point[1]))
    sortedpoints.sort(key=cmp_to_key(owncmp))
    sortedpoints=special_unique(sortedpoints)
    if len(sortedpoints)<4:
        hull = []
        for point in sortedpoints:
            hull.append((point[2], point[3]))
        return hull
    Stack.append(sortedpoints[0])
    Stack.append(sortedpoints[1])
    Stack.append(sortedpoints[2])
    stacklen=len(Stack)
    i=3
    while i<len(sortedpoints):
        while pointcheck(Stack,sortedpoints, i, stacklen):
            Stack.pop()
            stacklen-=1
        else:
            Stack.append(sortedpoints[i])
            stacklen+=1
            i += 1
    hull=[]
    for point in Stack:
        hull.append((point[2],point[3]))
    return hull

Test().runtest(1, graham_algorithm)

