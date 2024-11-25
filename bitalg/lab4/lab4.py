import random
import heapq
import numpy as np
import pandas as pd
from bitalg.tests.test4 import Test
from bitalg.visualizer.main import Visualizer

def compute_key(x,start,end):
    if x == start[0]:
        return start[1]
    elif x == end[0]:
        return end[1]
    return ((end[1] - start[1]) / (end[0] - start[0])) * (x - start[0]) + start[1]

class TreeNode:
    def __init__(self,given_start, given_end):
        self.start=given_start
        self.end=given_end
        self.height=1
        self.right=None
        self.left=None
    def key(self,x):
        if x == self.start[0]:
            return self.start[1]
        elif x == self.end[0]:
            return self.end[1]
        return ((self.end[1]-self.start[1])/(self.end[0]-self.start[0]))*(x-self.start[0])+self.start[1]

class AVLTree:
    def __init__(self):
        self.root = None
        self.x=0

    def height(self,node):
        if not node:
            return 0
        return node.height

    def balance(self,node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_left(self, a):
        b = a.right
        c = b.left

        b.left = a
        a.right = c

        a.height = 1 + max(self.height(a.left), self.height(a.left))
        b.height = 1 + max(self.height(b.left), self.height(b.left))

        return b

    def rotate_right(self, a):
        b = a.left
        c = b.right

        b.right = a
        a.left = c

        a.height = 1 + max(self.height(a.left), self.height(a.left))
        b.height = 1 + max(self.height(b.left), self.height(b.left))

        return b

    def min_key_node(self, node):
        curr = node
        while curr.left:
            curr=curr.left
        return curr

    def max_key_node(self, node):
        curr = node
        while curr.right:
            curr = curr.right
        return curr

    def insert_node(self, root ,given_node):
        if not root:
            return given_node
        elif given_node.key(self.x) < root.key(self.x):
            root.left = self.insert_node(root.left, given_node)
        else:
            root.right = self.insert_node(root.right, given_node)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        #tree rotations

        if balance > 1 and given_node.key(self.x) < root.left.key(self.x):
            return self.rotate_right(root)
        if balance < -1 and given_node.key(self.x) > root.right.key(self.x):
            return self.rotate_left(root)
        if balance > 1 and given_node.key(self.x) > root.left.key(self.x):
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and given_node.key(self.x) < root.right.key(self.x):
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def delete(self, root, key):
        if not root:
            return root

        if key < root.key(self.x):
            root.left = self.delete(root.left, key)
        elif key > root.key(self.x):
            root.right = self.delete(root.left, key)
        else:
            if not root.left:
                tmp = root.right
                root = None
                return tmp
            elif not root.right:
                tmp = root.left
                root = None
                return tmp

            tmp = self.min_key_node(root.right)
            root.start = tmp.start
            root.end = tmp.end
            root.right = self.delete(root.right, tmp.key(self.x))

        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        if balance > 1 and self.balance(root.left) >= 0:
            return self.rotate_right(root)
        elif balance < -1 and self.balance(root.right) <= 0:
            return self.rotate_left(root)
        elif balance > 1 and self.balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        elif balance < -1 and self.balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def find_key(self, root, key):
        if not root or root.key(self.x) == key:
            return root
        if root.key(self.x) < key:
            return self.find_key(root.right, key)
        else:
            return self.find_key(root.left, key)

    def find_parent(self, root, key):
        if not root:
            return root
        if root.left and root.left.key(self.x) == key:
            return root
        elif root.right and root.right.key(self.x) == key:
            return root
        elif root.key(self.x) < key:
            return self.find_parent(root.right, key)
        elif root.key(self.x) > key:
            return self.find_parent(root.left, key)
        else:
            return None

    def insert_line_segment(self,start,end):
        self.root=self.insert_node(self.root,TreeNode(start,end))

    def delete_key(self,key):
        self.root=self.delete(self.root,key)

    def search_key(self,key):
        return self.find_key(self.root,key)

    def swap(self, nodeA, nodeB):
        nodeA.start, nodeA.end, nodeB.start, nodeB.end = nodeB.start, nodeB.end, nodeA.start, nodeA.end

    def get_all(self,root, array):
        if root:
            self.get_all(root.left, array)
            array.append(root)
            self.get_all(root.right, array)

    def slow_search(self, key):
        nodes = []
        self.get_all(self.root, nodes)
        for node in nodes:
            if node.key(self.x) == key:
                return node
        return None

    def get_neighbours(self, key):
        node = self.search_key(key)
        if not node:
            return []
        left_nb = None
        right_nb = None
        if node.right:
            left_nb = self.min_key_node(node.right)
        if node.left:
            right_nb = self.max_key_node(node.left)
        parent = self.find_parent(self.root,key)
        build = [left_nb, right_nb, parent]
        build = [x for x in build if x is not None]
        if len(build)==3:
            build.pop(2)
        ret = []
        for node in build:
            ret.append((node.start,node.end))
        return ret

    def swap_and_get_neighbours(self, lineA, lineB):
        nb = {}
        keyA = compute_key(self.x,lineA[0],lineA[1])
        keyB = compute_key(self.x, lineB[0], lineB[1])
        nodeA = self.search_key(keyA)
        nodeB = self.search_key(keyB)
        if not nodeA:
            nodeA = self.slow_search(keyA)
        if not nodeB:
            nodeB = self.slow_search(keyB)
        self.swap(nodeA,nodeB)
        nb[lineA] = self.get_neighbours(keyA)
        nb[lineB] = self.get_neighbours(keyB)
        return nb


def generate_uniform_sections(max_x, max_y, n):
    count=0
    build=[]
    start_end_set=set()
    while count<n:
        start_x, start_y = random.uniform(0,max_x), random.uniform(0,max_y)
        end_x, end_y = random.uniform(start_x,max_x), random.uniform(0,max_y)
        if start_x==end_x: continue
        if start_x in start_end_set: continue
        if end_x in start_end_set: continue
        start_end_set.add(start_x)
        start_end_set.add(end_x)
        build.append(((start_x,start_y),(end_x,end_y)))
        count+=1
    return build

def are_intersecting(segment_a, segment_b):
    A, B = segment_a
    C, D = segment_b
    if ((A[0]-B[0])*(C[1]-D[1])-(A[1]-B[1])*(C[0]-D[0])) == 0: return False
    t = ((A[0]-C[0])*(C[1]-D[1])-(A[1]-C[1])*(C[0]-D[0]))/((A[0]-B[0])*(C[1]-D[1])-(A[1]-B[1])*(C[0]-D[0]))
    u = -((A[0]-B[0])*(A[1]-C[1])-(A[1]-B[1])*(A[0]-C[0]))/((A[0]-B[0])*(C[1]-D[1])-(A[1]-B[1])*(C[0]-D[0]))
    if 0 <= t <= 1 and 0 <= u <= 1:
        return A[0]+t*(B[0]-A[0]),A[1]+t*(B[1]-A[1])
    else: return False

def is_intersection(segments):
    Queue=[]
    Tree=AVLTree()
    for section in segments:
        Queue.append((section[0][0],1,segments.index(section)))
        Queue.append((section[1][0],2,segments.index(section)))
    heapq.heapify(Queue)
    while len(Queue)>0:
        index = heapq.heappop(Queue)
        Tree.x=index[0]
        if index[1] == 1:
            line = (segments[index[2]][0],segments[index[2]][1])
            Tree.insert_line_segment(line[0],line[1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x,line[0],line[1]))
            for nb in neighbours:
                if are_intersecting(line,nb):
                    return True
        elif index[1] == 2:
            line = (segments[index[2]][0], segments[index[2]][1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x, line[0], line[1]))
            Tree.delete_key(compute_key(Tree.x, line[0], line[1]))
            if len(neighbours)==2:
                if are_intersecting(neighbours[0],neighbours[1]):
                    return True
    return False

def is_intersection_VIS(segments, vis):
    vis.add_line_segment(segments)
    Queue=[]
    Tree=AVLTree()
    for section in segments:
        Queue.append((section[0][0],1,segments.index(section)))
        Queue.append((section[1][0],2,segments.index(section)))
    heapq.heapify(Queue)
    prev = vis.add_line(((0,0),(0,1)))
    while len(Queue)>0:
        index = heapq.heappop(Queue)
        vis.remove_figure(prev)
        prev = vis.add_line(((index[0],0),(index[0],1)))
        Tree.x=index[0]
        if index[1] == 1:
            line = (segments[index[2]][0],segments[index[2]][1])
            Tree.insert_line_segment(line[0],line[1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x,line[0],line[1]))
            for nb in neighbours:
                if are_intersecting(line,nb):
                    return True
        elif index[1] == 2:
            line = (segments[index[2]][0], segments[index[2]][1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x, line[0], line[1]))
            Tree.delete_key(compute_key(Tree.x, line[0], line[1]))
            if len(neighbours)==2:
                if are_intersecting(neighbours[0],neighbours[1]):
                    return True
    return False

def find_intersections(segments):
    intersections = []
    Queue = []
    Tree = AVLTree()
    for section in segments:
        Queue.append((section[0][0], 1, segments.index(section)))
        Queue.append((section[1][0], 2, segments.index(section)))
    heapq.heapify(Queue)
    while len(Queue) > 0:
        index = heapq.heappop(Queue)
        Tree.x = index[0]
        if index[1] == 1:
            line = (segments[index[2]][0], segments[index[2]][1])
            Tree.insert_line_segment(line[0], line[1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x, line[0], line[1]))
            for nb in neighbours:
                point = are_intersecting(line, nb)
                if point:
                    heapq.heappush(Queue, (point[0], 3, (point, line, nb)))
                    intersections.append((point, segments.index(line), segments.index(nb)))

        elif index[1] == 2:
            line = (segments[index[2]][0], segments[index[2]][1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x, line[0], line[1]))
            Tree.delete_key(compute_key(Tree.x, line[0], line[1]))
            if len(neighbours) == 2:
                point = are_intersecting(neighbours[0], neighbours[1])
                if point and (point[0], 3, (point, neighbours[0], neighbours[1])) not in Queue:
                    heapq.heappush(Queue, (point[0], 3, (point, neighbours[0], neighbours[1])))
                    intersections.append((point, segments.index(neighbours[0]), segments.index(neighbours[1])))

        elif index[1] == 3:
            neighbours = Tree.swap_and_get_neighbours(index[2][1], index[2][2])
            for nb1 in neighbours[index[2][1]]:
                point = are_intersecting(index[2][1], nb1)
                if point and point[0] > Tree.x and (point[0], 3, (point, index[2][1], nb1)) not in Queue:
                    heapq.heappush(Queue, (point[0], 3, (point, index[2][1], nb1)))
                    intersections.append((point, segments.index(index[2][1]), segments.index(nb1)))
            for nb2 in neighbours[index[2][2]]:
                point = are_intersecting(index[2][2], nb2)
                if point and point[0] > Tree.x and (point[0], 3, (point, index[2][2], nb2)) not in Queue:
                    heapq.heappush(Queue, (point[0], 3, (point, index[2][2], nb2)))
                    intersections.append((point, segments.index(index[2][2]), segments.index(nb2)))
    return intersections

def find_intersections_VIS(segments, vis):
    vis=Visualizer()
    vis.add_line_segment(segments)
    intersections = []
    Queue = []
    Tree = AVLTree()
    for section in segments:
        Queue.append((section[0][0], 1, segments.index(section)))
        Queue.append((section[1][0], 2, segments.index(section)))
    heapq.heapify(Queue)
    prev = vis.add_line(((0,0),(0,1)))
    while len(Queue) > 0:
        index = heapq.heappop(Queue)
        Tree.x = index[0]
        vis.remove_figure(prev)
        prev = vis.add_line(((index[0], 0), (index[0], 1)))
        if index[1] == 1:
            line = (segments[index[2]][0], segments[index[2]][1])
            Tree.insert_line_segment(line[0], line[1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x, line[0], line[1]))
            for nb in neighbours:
                point = are_intersecting(line, nb)
                if point:
                    heapq.heappush(Queue, (point[0], 3, (point, line, nb)))
                    intersections.append((point, segments.index(line), segments.index(nb)))

        elif index[1] == 2:
            line = (segments[index[2]][0], segments[index[2]][1])
            neighbours = Tree.get_neighbours(compute_key(Tree.x, line[0], line[1]))
            Tree.delete_key(compute_key(Tree.x, line[0], line[1]))
            if len(neighbours) == 2:
                point = are_intersecting(neighbours[0], neighbours[1])
                if point and (point[0], 3, (point, neighbours[0], neighbours[1])) not in Queue:
                    heapq.heappush(Queue, (point[0], 3, (point, neighbours[0], neighbours[1])))
                    intersections.append((point, segments.index(neighbours[0]), segments.index(neighbours[1])))

        elif index[1] == 3:
            neighbours = Tree.swap_and_get_neighbours(index[2][1], index[2][2])
            for nb1 in neighbours[index[2][1]]:
                point = are_intersecting(index[2][1], nb1)
                if point and point[0] > Tree.x and (point[0], 3, (point, index[2][1], nb1)) not in Queue:
                    heapq.heappush(Queue, (point[0], 3, (point, index[2][1], nb1)))
                    intersections.append((point, segments.index(index[2][1]), segments.index(nb1)))
            for nb2 in neighbours[index[2][2]]:
                point = are_intersecting(index[2][2], nb2)
                if point and point[0] > Tree.x and (point[0], 3, (point, index[2][2], nb2)) not in Queue:
                    heapq.heappush(Queue, (point[0], 3, (point, index[2][2], nb2)))
                    intersections.append((point, segments.index(index[2][2]), segments.index(nb2)))
    return intersections

#Test().runtest(1, generate_uniform_sections)
#Test().runtest(2, is_intersection)
#Test().runtest(3, find_intersections)