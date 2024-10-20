import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from PIL.ImageChops import difference
from matplotlib.pyplot import inferno
from notebook_shim.nbserver import diff_members

sys.path.append('C:/Users/franc/Documents/AlgorytmyGeometryczne')

from bitalg.tests.test1 import Test
from bitalg.visualizer.main import Visualizer
import random as random
import math as math

def angle_bettwen(A,B):
    if A==B: return 0
    angle1=np.arctan2(A[1],A[0])
    angle2=np.arctan2(B[1],B[0])
    return np.rad2deg((angle1-angle2)%(2*np.pi))

def special_unique(list):
    building=[]
    building.append(list[0])
    for i in range(1, len(list)):
        if list[i][0] != list[i-1][0]:
            building.append(list[i])
    return building

def orient(a,b,c):
    return (a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0])

def graham_algorithm(Q):
    Stack=[]
    mini=math.inf
    for i in Q:
        if i[1]<mini[1]:
            mini=i
    for i in Q:
        if i[1]==mini[1] and i[0]<mini[0]:
            mini=i
    sortedpoints=[]
    for point in Q:
        sortedpoints.append((angle_bettwen(point,mini),math.sqrt((point[0]-mini[0])**2 + (point[1]-mini[1])**2 ),point[0],point[1]))
    sortedpoints=sortedpoints[1:]
    sortedpoints.sort(key=lambda tup: tup[1],reverse=True)
    sortedpoints.sort()
    sortedpoints=special_unique(sortedpoints)
    Stack.append(mini)
    Stack.append(sortedpoints[1])
    Stack.append(sortedpoints[2])
    stacklen=len(Stack)
    i=3
    while i<len(sortedpoints):
        while orient((sortedpoints[i][2],sortedpoints[i][3]),Stack[stacklen-1],Stack[stacklen-2]) > 0:
            Stack.pop()
        else:
            Stack.append((sortedpoints[i][2], sortedpoints[i][3]))
            i += 1
    return Stack

