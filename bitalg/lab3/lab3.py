from operator import truediv

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

def draw_polygon_colors_and_save(polygon,colors,filename):
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
    vis.save(filename)
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
                for p in left:
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
                for p in right:
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

def triangulation(Polygon,id=0):
    vis = Visualizer()
    vis.add_polygon(Polygon, color="orange", fill=False)
    vis.add_point(Polygon, color="blue")
    vis.save(str(id)+"_poly")
    draw_polygon_colors_and_save(Polygon,color_vertex(Polygon),str(id)+"_categorised")
    if is_y_monotonic(Polygon):
        added=triangulate_y_monotonic(Polygon,vis)
        vis.save(str(id)+"_triangulated")
        vis.save_gif(str(id)+"_tgif")
        vis.show()
        return added


#Test().runtest(1, is_y_monotonic)
#Test().runtest(2, color_vertex)
#Test().runtest(3,triangulation)

polys = [[[16.263440860215056, 38.31168831168831], [7.862903225806452, 30.555555555555554], [16.061827956989248, 24.33261183261183], [30.98118279569893, 24.51298701298701], [36.29032258064517, 31.908369408369406], [30.91397849462366, 38.85281385281385]],
         [[24.66397849462366, 45.707070707070706], [16.330645161290324, 43.72294372294372], [11.357526881720432, 38.94300144300144], [8.66935483870968, 33.44155844155844], [8.266129032258064, 28.93217893217893], [8.736559139784948, 25.144300144300143], [10.618279569892476, 21.536796536796533], [14.516129032258068, 17.748917748917748], [20.631720430107528, 14.68253968253968], [26.34408602150538, 14.953102453102453], [31.250000000000004, 17.929292929292927], [34.61021505376344, 23.97186147186147], [34.543010752688176, 30.194805194805188], [33.53494623655915, 36.507936507936506], [31.787634408602155, 41.46825396825397]],
         [[16.801075268817208, 47.51082251082251], [16.733870967741936, 43.27200577200577], [27.55376344086022, 40.115440115440116], [17.06989247311828, 35.42568542568542], [27.755376344086027, 31.998556998556996], [17.74193548387097, 26.767676767676765], [27.486559139784948, 23.79148629148629], [17.607526881720432, 18.740981240981238], [36.155913978494624, 23.16017316017316], [26.612903225806452, 27.48917748917749], [37.16397849462366, 35.24531024531024], [25.000000000000004, 35.51587301587301], [37.432795698924735, 42.73088023088023]],
         [[24.39516129032258, 46.60894660894661], [8.803763440860216, 41.91919191919192], [24.19354838709678, 37.04906204906205], [8.333333333333336, 34.794372294372295], [23.655913978494628, 30.916305916305912], [8.938172043010752, 25.59523809523809], [23.319892473118284, 24.873737373737374], [9.475806451612904, 19.1017316017316], [22.98387096774194, 18.831168831168828], [25.067204301075275, 14.68253968253968], [28.56182795698925, 11.886724386724385], [42.67473118279571, 32.08874458874459]],
         [[24.327956989247316, 41.73881673881674], [12.5, 28.300865800865797], [24.66397849462366, 14.141414141414138], [36.155913978494624, 29.38311688311688]],
         [[24.73118279569893, 42.82106782106782], [13.508064516129032, 37.22943722943723], [18.010752688172044, 22.438672438672437], [30.577956989247316, 22.889610389610386], [34.74462365591398, 36.32756132756133]],
         [[25.806451612903228, 46.60894660894661], [7.997311827956988, 3.3189033189033195], [23.924731182795703, 23.520923520923517], [40.72580645161291, 27.75974025974026], [26.478494623655916, 31.36724386724386], [42.80913978494624, 34.07287157287157], [27.55376344086022, 37.95093795093795], [43.682795698924735, 40.656565656565654], [28.225806451612907, 43.72294372294372], [43.01075268817205, 49.314574314574315]],
         [[36.491935483870975, 47.42063492063492], [33.064516129032256, 41.73881673881674], [28.629032258064523, 36.32756132756133], [22.916666666666668, 31.998556998556996], [17.607526881720432, 29.56349206349206], [11.021505376344088, 27.308802308802303], [39.852150537634415, 2.507215007215007]],
         [[25.940860215053764, 47.781385281385276], [11.827956989247312, 41.82900432900433], [25.470430107526884, 38.31168831168831], [12.5, 33.17099567099567], [25.537634408602155, 28.300865800865797], [39.65053763440861, 32.81024531024531], [30.24193548387097, 36.417748917748916], [30.1747311827957, 40.386002886002885], [40.38978494623656, 44.35425685425685], [30.040322580645164, 46.51875901875902]],
         [[24.798387096774196, 46.60894660894661], [4.56989247311828, 39.75468975468976], [18.750000000000004, 36.688311688311686], [5.981182795698926, 29.83405483405483], [18.21236559139785, 25.68542568542568], [5.981182795698926, 19.01154401154401], [18.346774193548388, 15.58441558441558], [18.27956989247312, 11.255411255411254], [29.569892473118284, 11.616161616161616], [29.435483870967747, 16.396103896103895], [41.801075268817215, 21.085858585858585], [29.70430107526882, 27.038239538239534], [42.876344086021504, 35.33549783549783], [29.637096774193555, 38.13131313131313], [42.54032258064517, 45.25613275613276]]]

for i in range(len(polys)):
    triangulation(polys[i],i+1)
