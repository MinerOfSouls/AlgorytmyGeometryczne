import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from PIL.ImageChops import difference
from notebook_shim.nbserver import diff_members

sys.path.append('C:/Users/franc/Documents/AlgorytmyGeometryczne')

from bitalg.tests.test1 import Test
from bitalg.visualizer.main import Visualizer
import random as random
import math as math

#punkty zawsze będą generowane identyczne ponieważ generowane są w takiej samej kolejności
#i jest ustalony seed
random.seed(1728893743)
POINT_SIZE=5
SPECTRUM_POINT_SIZE=5

#funkcje do rysowanie
def draw_points(points):
    vis = Visualizer()
    vis.add_point(points, s=POINT_SIZE, color='green')
    vis.show()

def draw_points_and_save(points,filename):
    vis = Visualizer()
    vis.add_point(points, s=POINT_SIZE, color='green')
    vis.show()
    vis.save(filename)

def draw_line(points_left, points_mid, points_right):
    vis = Visualizer()
    vis.add_line(((-1.0, 0.0), (1.0,0.1)), color='red')
    vis.add_point(points_left, s=POINT_SIZE, color=['green'])
    vis.add_point(points_right, s=POINT_SIZE, color=['orange'])
    vis.add_point(points_mid, s=POINT_SIZE, color=['purple'])
    vis.show()

def draw_line_and_save(points_left, points_mid, points_right,filename,line=True):
    vis = Visualizer()
    if line: vis.add_line(((-1.0, 0.0), (1.0,0.1)), color='red')
    vis.add_point(points_left, s=POINT_SIZE, color=['green'])
    vis.add_point(points_mid, s=POINT_SIZE, color=['purple'])
    vis.add_point(points_right, s=POINT_SIZE, color=['orange'])
    vis.show()
    vis.save(filename)

def export_data(array,filename):
    f=open(filename, 'x')
    for i in range(5):
        for j in range(4):
            print(len(array[i][j][0]),len(array[i][j][1]),len(array[i][j][2]),end=" ",file=f)
        print(" ", file=f)
    f.close()

#funkcje generujące linie
def generate_uniform_points(left, right, n = 10 ** 5):
    points=[None for _ in range(n)]
    counter=0
    while counter<n:
        points[counter]=(random.uniform(left,right),random.uniform(left,right))
        counter=counter+1
    return points

def generate_circle_points(O, R, n = 100):
    points=[None for _ in range(n)]
    for i in range(n):
        angle=random.random()*(2*math.pi)
        points[i]=(O[0]+(math.sin(angle)*R),O[1]+(math.cos(angle)*R))
    return points

def generate_collinear_points(a, b, n=100):
    """
    Funkcja generuje równomiernie n współliniowych punktów leżących na prostej ab pomiędzy punktami a i b
    :param a: krotka współrzędnych oznaczająca początek wektora tworzącego prostą
    :param b: krotka współrzędnych oznaczająca koniec wektora tworzącego prostą
    :param n: ilość generowanych punktów
    :return: tablica punktów w postaci krotek współrzędnych
    """
    points=[]
    for i in range(n):
        x=random.uniform(-1000,1000)
        y=(a[1]-b[1])/(a[0]-b[0])*x+(a[1]-(a[1]-b[1])/(a[0]-b[0])*a[0])
        points.append((x,y))
    return points

#a,b - krotki wyznaczające prostą, c - punkt do sprawdzenia

def mat_det_3x3(a, b, c):
    return a[0] * b[1] + a[1] * c[0] + b[0] * c[1] - b[1] * c[0] - c[1] * a[0] - a[1] * b[0]
def mat_det_3x3_lib(a, b, c):
    matrix=[[a[0],a[1],1],
            [b[0],b[1],1],
            [c[0],c[1],1]]
    return np.linalg.det(matrix)
def mat_det_2x2(a, b, c):
    return (a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0])
def mat_det_2x2_lib(a, b, c):
    matrix=[[a[0]-c[0],a[1]-c[1]],
            [b[0]-c[0],b[1]-c[1]]]
    return np.linalg.det(matrix)

#a,b - wektry linni, points - tabela punktów, mat_det_func - funkcja licząca wyznacznik, eps - dokładność
def categorize_points(points, a, b, mat_det_func, eps):
    left,mid,right=[],[],[]
    for p in points:
        close=mat_det_func(a,b,p)
        if close>eps:
            left.append(p)
        elif close<-eps:
            right.append(p)
        else:
            mid.append(p)
    return (left,mid,right)

def check_points_many(points,a,b,det_funcs, eps, checked_points):
    for i in range(len(eps)):
        for j in range(len(det_funcs)):
            left,mid,right=categorize_points(points,a,b,det_funcs[j],eps[i])
            checked_points[i][j]=[left,mid,right]

def diff_cheker(pointsA,pointsB):
    A=set(pointsA[1])
    B=set(pointsB[1])
    A=A-B
    B=B-A
    returna=[]
    for i in A:
        returna.append(i)
    retunb=[]
    for j in B:
        retunb.append(j)
    return (returna,retunb)

def draw_diff(A,B):
    vis = Visualizer()
    vis.add_point(A, s=POINT_SIZE, color=['blue'])
    vis.add_point(B, s=POINT_SIZE, color=['red'])
    vis.show()

def draw_diff_and_save(A,B,filename,line=True, size=5):
    vis=Visualizer()
    if line: vis.add_line(((-1.0, 0.0), (1.0, 0.1)), color='green')
    vis.add_point(A,s=size,color=['blue'])
    vis.add_point(B,s=size,color=['red'])
    vis.show()
    vis.save(filename)

def draw_spectrum_and_save(points,method,filename,howmany=3):
    colors=["#ffaaaa","#ff807a","#ff5347","#ff0000"]
    PointSet=[set(points[i][method][1]) for i in range(howmany+1)]
    for i in range(1,howmany):
        PointSet[i]-=PointSet[i-1]
    table=[[] for i in range(howmany)]
    for i in range(howmany):
        for item in PointSet[i]:
            table[i].append(item)
    vis=Visualizer()
    for i in range(howmany):
        vis.add_point(points[i][method][1],s=SPECTRUM_POINT_SIZE,color=colors[i],alpha=0.2)
    vis.show()
    vis.save(filename)



#stałe do linni
a = (-1.0, 0.0)
b = (1.0, 0.1)

print("Generating points")
points1=generate_uniform_points(-1000,1000,10 ** 5)
points2=generate_uniform_points(-10 ** 14, 10 ** 14, 10 ** 5)
points_circle=generate_circle_points((0,0),100,1000)
points_line=generate_collinear_points(a,b,1000)

#wartości dokładności sprawdzania punktów
eps=[0, 10 ** -14, 10 ** -12, 10 ** -10, 10 ** -8]
det_funcs=[mat_det_2x2,mat_det_2x2_lib,mat_det_3x3,mat_det_3x3_lib]

#tabele zawierające wartości punktów sprawdzonych dla rórych dokładności i funkcji
checked_points1=[[None for _ in range(4)] for __ in range(5)]
checked_points2=[[None for _ in range(4)] for __ in range(5)]
checked_points_circle=[[None for _ in range(4)] for __ in range(5)]
checked_points_line=[[None for _ in range(4)] for __ in range(5)]

print("checking points")

check_points_many(points1,a,b,det_funcs,eps,checked_points1)
check_points_many(points2,a,b,det_funcs,eps,checked_points2)
check_points_many(points_circle,a,b,det_funcs,eps,checked_points_circle)
check_points_many(points_line,a,b,det_funcs,eps,checked_points_line)

print("exporting data")
export_data(checked_points1,"points1.txt")
export_data(checked_points2,"points2.txt")
export_data(checked_points_circle,"points_circle.txt")
export_data(checked_points_line,"points_line.txt")

print("drawing points")

#uncategorised points
draw_points_and_save(points1,"points1_uncategorised")
draw_points_and_save(points2,"points2_uncategorised")
draw_points_and_save(points_circle,"points_circle_uncategorised")
draw_points_and_save(points_line,"points_line_uncategorised")

draw_line_and_save(checked_points1[0][0][0],checked_points1[0][0][1],checked_points1[0][0][2],"points1_categorised")

draw_line_and_save(checked_points_circle[0][0][0],checked_points_circle[0][0][1],checked_points_circle[0][0][2],"points_circle_categorised")

draw_line_and_save(checked_points2[0][0][0],checked_points2[0][0][1],checked_points2[0][0][2],"points2_categorised")

f = open("points2diffs.txt","x")
A1,B1=diff_cheker(checked_points2[0][0],checked_points2[0][1])
print(A1,B1,file=f)
draw_diff_and_save(A1,B1,"points2_diff_2x2handlib",True,30)
A2,B2=diff_cheker(checked_points2[0][0],checked_points2[0][3])
print(A2,B2,file=f)
draw_diff_and_save(A2,B2,"points2_dif_2x2hand_3x3hand",True,30)
f.close()

draw_line_and_save(checked_points_line[0][0][0],checked_points_line[0][0][1],checked_points_line[0][0][2],"points_line_2x2hand_eps0",False)
draw_line_and_save(checked_points_line[0][2][0],checked_points_line[0][2][1],checked_points_line[0][2][2],"points_line_3x3hand_eps0",False)
draw_line_and_save(checked_points_line[1][2][0],checked_points_line[1][2][1],checked_points_line[1][2][2],"points_line_3x3hand_eps-14",False)

draw_spectrum_and_save(checked_points_line,0,"line_spectrum_2x2hand_depth4")
draw_spectrum_and_save(checked_points_line,1,"line_spectrum_2x2lib_depth4")
draw_spectrum_and_save(checked_points_line,2,"line_spctrum_3x3hand_depth2",1)
draw_spectrum_and_save(checked_points_line,3,"line_spctrum_3x3lib_depth3",2)

A3,B3=diff_cheker(checked_points_line[0][0],checked_points_line[0][2])
draw_diff_and_save(A3,B3,"points_line_diff_2x2hand_3x3hand_eps0",False)
A4,B4=diff_cheker(checked_points_line[0][1],checked_points_line[0][3])
draw_diff_and_save(A4,B4,"points_line_diff_2x2lib_3x3lib_eps0",False)
A5,B5=diff_cheker(checked_points_line[1][0],checked_points_line[1][2])
draw_diff_and_save(A5,B5,"points_line_diff_2x2hand_3x3hand_eps-14",False)
A6,B6=diff_cheker(checked_points_line[1][2],checked_points_line[1][3])
draw_diff_and_save(A6,B6,"points_line_diff_3x3hand_3x3lib_eps-14",False)
A7,B7=diff_cheker(checked_points_line[1][0],checked_points_line[1][1])
draw_diff_and_save(A7,B7,"points_line_diff_2x2hand_2x2lib_eps-14",False)



















