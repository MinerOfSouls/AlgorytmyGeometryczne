import matplotlib.pyplot as plt
import numpy as np
import time
from bitalg.tests.test3 import Test
from bitalg.visualizer.figures.polygon import Polygon
from bitalg.visualizer.main import Visualizer

def draw_polygon_colors(polygon,colors):
    points_start=[]
    points_end=[]
    points_connect=[]
    points_divide=[]
    points_regular=[]
    for i in range(len(polygon)):
        if colors[i]==0:
            points_start.append(polygon[i])
        elif colors[i]==1:
            points_end.append(polygon[i])
        elif colors[i]==2:
            points_connect.append(polygon[i])
        elif colors[i]==3:
            points_divide.append(polygon[i])
        elif colors[i]==4:
            points_regular.append(polygon[i])

    vis = Visualizer()
    colors_start = ['green']
    color_end=['red']
    color_connect=['blue']
    color_divide=['cyan']
    color_regular=['#3B240B']
    vis.add_polygon(polygon, fill=False)
    vis.add_point(points_start, color=colors_start)
    vis.add_point(points_end, color=color_end)
    vis.add_point(points_connect, color=color_connect)
    vis.add_point(points_divide, color=color_divide)
    vis.add_point(points_regular, color=color_regular)
    vis.show()

def draw_polygon(polygon):
    vis = Visualizer()
    points = polygon
    vis.add_polygon(polygon, fill=False)
    vis.show()

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

def orient(a,b,c):
    return (a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0])

def is_y_monotonic(Polygon):
    max_y=max([Polygon[i][1] for i in range(len(Polygon))])
    min_y=min([Polygon[i][1] for i in range(len(Polygon))])
    starti=0;
    endi=0;
    for i in range(len(Polygon)):
        if max_y==Polygon[i][1]:
            starti=i
        if min_y==Polygon[i][1]:
            endi=i
    prev = starti
    loop = starti + 1
    if starti == len(Polygon) - 1:
        prev = starti
        loop = 0
    while loop!=endi:
        if Polygon[prev][1]>Polygon[loop][1]:
            prev = loop
            if loop==len(Polygon)-1:
                loop=0
            else:
                loop+=1
        else:
            return False
    prev = endi
    loop = endi + 1
    if endi == len(Polygon) - 1:
        prev = endi
        loop = 0
    while loop!=starti:
        if Polygon[prev][1]<Polygon[loop][1]:
            prev = loop
            if loop==len(Polygon)-1:
                loop=0
            else:
                loop+=1
        else:
            return False
    return True

def angle_check(a,b,c):
    x1, y1 = a[0] - b[0], a[1] - b[1]
    x2, y2 = c[0] - b[0], c[1] - b[1]
    return x1 * y2 > x2 * y1

def color_vertex(Polygon):
    T = [None for i in range(len(Polygon))]
    for i in range(len(Polygon)):
        prev=Polygon[i-2]
        curr=Polygon[i-1]
        next=Polygon[i]
        if prev[1]<curr[1] and next[1]<curr[1] and not angle_check(prev,curr,next):
            T[i-1]=0
        elif prev[1]>curr[1] and next[1]>curr[1] and not angle_check(prev,curr,next):
            T[i-1]=1
        elif prev[1]<curr[1] and next[1]<curr[1] and angle_check(prev,curr,next):
            T[i-1]=3
        elif prev[1]>curr[1] and next[1]>curr[1] and angle_check(prev,curr,next):
            T[i-1]=2
        else:
            T[i-1]=4
    return T

def are_not_nb(length,a,b):
    if a==0 and b==length-1 or b==0 and a==length-1:
        return False
    elif abs(a-b)!=1:
        return True
    return False

def get_up_nb(index,Polygon):
    if index == 0:
        if Polygon[-1][1]>Polygon[0][1]:
            return len(Polygon)-1
        else:
            return 1
    elif index == len(Polygon)-1:
        if Polygon[0][1]>Polygon[-1][1]:
            return 0
        else:
            return len(Polygon)-2
    else:
        if Polygon[index-1][1]>Polygon[index][1]:
            return index-1
        else: return index+1


def triangulate_y_monotonic(Polygon, vis):
    addededges = []
    max_y = max([Polygon[i][1] for i in range(len(Polygon))])
    min_y = min([Polygon[i][1] for i in range(len(Polygon))])
    starti = 0;
    endi = 0;
    for i in range(len(Polygon)):
        if max_y == Polygon[i][1]:
            starti = i
        if min_y == Polygon[i][1]:
            endi = i
    left=[]
    right=[]
    if starti<endi:
        left=Polygon[starti:(endi+1)]
        right=Polygon[endi:]
        right.extend(Polygon[:(starti+1)])
    else:
        right = Polygon[endi:(starti + 1)]
        left = Polygon[starti:]
        left.extend(Polygon[:(endi + 1)])
    Polygon_Sorted = sorted(Polygon, key=lambda tup: tup[1],reverse=True)
    Stack = []
    Stack.append(Polygon.index(Polygon_Sorted[0]))
    Stack.append(Polygon.index(Polygon_Sorted[1]))
    for i in range(2,len(Polygon)):
        ind=Polygon.index(Polygon_Sorted[i])
        if ((Polygon_Sorted[i] in right and Polygon[Stack[-1]] in left) or
                (Polygon_Sorted[i] in left and Polygon[Stack[-1]] in right)):
            for point in Stack:
                if are_not_nb(len(Polygon),ind,point):
                    vis.add_line_segment((Polygon[ind], Polygon[point]))
                    addededges.append((ind,point))
            Stack.append(ind)
            Stack = [Stack[-2],Stack[-1]]
        elif Polygon_Sorted[i] in left and Polygon[Stack[-1]] in left:
            added=[]
            for j in range(len(Stack)-1,-1,-1):
                between = []
                for p in Polygon:
                    if Polygon[ind][1] < p[1] < Polygon[Stack[j]][1]:
                        between.append(p)
                tmp = [orient(Polygon[ind], Polygon[Stack[j]], between[k]) for k in range(len(between))]
                if are_not_nb(len(Polygon), ind,Stack[j]) and len(tmp)>0 and min(tmp)>0:
                    vis.add_line_segment((Polygon[ind],Polygon[Stack[j]]))
                    addededges.append((ind,Stack[j]))
                    added.append((ind,Stack[j]))
            toRm=set()
            for edge in added:
                for point in Stack:
                    if (orient(Polygon[edge[0]], Polygon[edge[1]], Polygon[point])>0 and
                            Polygon[edge[0]][1] < Polygon[point][1] < Polygon[edge[1]][1]):
                        toRm.add(point)
            for point in toRm:
                Stack.remove(point)
            Stack.append(ind)
        elif Polygon_Sorted[i] in right and Polygon[Stack[-1]] in right:
            added = []
            for j in range(len(Stack) - 1, -1, -1):
                between=[]
                for p in Polygon:
                    if Polygon[ind][1] < p[1] < Polygon[Stack[j]][1]:
                        between.append(p)
                tmp = [orient(Polygon[ind], Polygon[Stack[j]], between[k]) for k in range(len(between))]
                if are_not_nb(len(Polygon), ind, Stack[j]) and len(tmp)>0 and max(tmp) < 0:
                    vis.add_line_segment((Polygon[ind], Polygon[Stack[j]]))
                    addededges.append((ind,Stack[j]))
                    added.append((ind, Stack[j]))
            toRm = set()
            for edge in added:
                for point in Stack:
                    if (orient(Polygon[edge[0]], Polygon[edge[1]], Polygon[point]) < 0 and
                            Polygon[edge[0]][1] < Polygon[point][1] < Polygon[edge[1]][1]):
                        toRm.add(point)
            for point in toRm:
                Stack.remove(point)
            Stack.append(ind)
    return addededges

def triangulation(Polygon,name):
    vis = Visualizer()
    vis.add_polygon(Polygon, color="orange", fill=False)
    vis.add_point(Polygon, color="blue")
    vis.save(name+"_poly")
    if is_y_monotonic(Polygon):
        added=triangulate_y_monotonic(Polygon,vis)
        vis.save(name+"_triangulated")
        vis.save_gif(name+"_tgif")
        vis.show()
        return added

name=input("Podaj nazwe: ")
poly=give_figure()
tri=triangulation(poly,name)
print(tri)