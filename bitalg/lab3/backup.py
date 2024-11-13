def triangulate_y_monotonic(Polygon, vis):
    max_y = max([Polygon[i][1] for i in range(len(Polygon))])
    min_y = min([Polygon[i][1] for i in range(len(Polygon))])
    starti = 0;
    endi = 0;
    for i in range(len(Polygon)):
        if max_y == Polygon[i][1]:
            starti = i
        if min_y == Polygon[i][1]:
            endi = i
    print(endi)
    left=[]
    right=[]
    if starti<endi:
        left=Polygon[starti:(endi+1)]
        right=Polygon[endi:]
        right.extend(Polygon[:(starti+1)])
    else:
        left = Polygon[endi:(starti + 1)]
        right = Polygon[starti:]
        right.extend(Polygon[:(endi + 1)])
    Polygon_Sorted = sorted(Polygon, key=lambda tup: tup[1],reverse=True)
    Stack = []
    Stack.append(Polygon.index(Polygon_Sorted[0]))
    Stack.append(Polygon.index(Polygon_Sorted[1]))
    polygon_graphed=[set() for _ in range(len(Polygon))]
    for i in range(1,len(Polygon)-1):
        polygon_graphed[i-1].add(i)
        polygon_graphed[i].add(i-1)
    polygon_graphed[0].add(len(Polygon)-1)
    polygon_graphed[-1].add(0)
    for i in range(2,len(Polygon)):
        ind=Polygon.index(Polygon_Sorted[i])
        if ((Polygon_Sorted[i] in right and Polygon[Stack[-1]] in left) or
                (Polygon_Sorted[i] in left and Polygon[Stack[-1]] in right)):
            for point in Stack:
                if are_not_nb(len(Polygon),ind,point):
                    vis.add_line_segment((Polygon[ind], Polygon[point]))
                    polygon_graphed[point].add(ind)
                    polygon_graphed[ind].add(point)
            Stack.append(ind)
            Stack = [Stack[-2],Stack[-1]]
        else:
            ToRm=set()
            is_left=Polygon_Sorted[i] in left
            is_right=Polygon_Sorted[i] in right
            for j in range(len(Stack)-1,-1,-1):
                if (are_not_nb(len(Polygon),ind,Stack[j]) and
                ( (is_left and Polygon[Stack[j]] in left and orient(Polygon[ind],Polygon[ind-1],Polygon[Stack[j]])<0) or
                (is_right and Polygon[Stack[j]] in right and orient(Polygon[ind],Polygon[ind-1],Polygon[Stack[j]])>0 and Stack[j] is not starti))):
                    vis.add_line_segment((Polygon[ind],Polygon[Stack[j]]))
                    polygon_graphed[Stack[j]].add(ind)
                    polygon_graphed[ind].add(Stack[j])
                    for p in Stack:
                        if ((is_left and orient(Polygon[ind],Polygon[p],Polygon[Stack[j]])<0) or
                            (is_right and orient(Polygon[ind],Polygon[p],Polygon[Stack[j]])>0)):
                            ToRm.add(p)
                elif (are_not_nb(len(Polygon),ind,Stack[j]) and
                      ((Polygon_Sorted[i] in right and Polygon[Stack[-1]] in left) or
                       (Polygon_Sorted[i] in left and Polygon[Stack[-1]] in right))):
                    vis.add_line_segment((Polygon[ind], Polygon[Stack[j]]))
                    polygon_graphed[Stack[j]].add(ind)
                    polygon_graphed[ind].add(Stack[j])
            for p in ToRm:
                Stack.remove(p)
            Stack.append(ind)
    return polygon_graphed