"""
Author: Joseph Gregory
resources: https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/

### Problem
        Suppose we are given a set of boxes, each specified by their height, width, and depth in inches. All
    three side lengths of every box lie strictly between 1 inch and 36 inches. As you should expect, one
    box can be placed inside another if the first box can be rotated so that its height, width, and depth
    are respectively at least one inch smaller smaller than the height, width, and depth of the second
    box. Boxes can be nested recursively. Call a box visible if it is not inside another box. Write code
    that will determine the smallest number of visible boxes.
    Your code should use standard input/output. A test file will start with an integer n (1 ≤ n ≤ 50),
    being the number of boxes. After that will follow n lines of the form l w h (1 ≤ l, w, h ≤ 36), where
    the three integers give the length, width, and height of that box.

Sample Input 1:
4
2 1 3
4 3 5
2 3 4
4 5 6

Sample Input 2:
5
5 5 5
4 4 5
4 5 5
2 3 3
5 6 6
"""
import sys

class Graph:
    
    def __init__(self, graph):
        self.graph = graph 
        self.row = len(graph)
    
    def __repr__(self):
        ret = "\n[\n"
        for i in range(len(self.graph)):
            ret = ret + str(self.graph[i]) + "\n"
        ret += "]\n"
        return ret
        
    
    def BFS(self, s, t, parent):
        visited = [False] * (self.row)
        queue = []

        queue.append(s)
        visited[s] = True
        
        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
            
        return True if visited[t] else False

    def maxFlow(self, source, sink):
        parent = [-1] * (self.row)

        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while( v!= source):
                u = parent[v]
                self.graph[u][v] -= path_flow 
                self.graph[v][u] += path_flow
                v = parent[v]
        return max_flow

def driver():

    #initialize a list of boxes that will contain
    #[ [l,w,h], ... ,[l,w,h]]
    boxes = []
    
    while (sys.stdin):
        #first line of file read
        n = int(sys.stdin.readline().strip())
        for _ in range(n):
            #line read
            in_data = sys.stdin.readline().strip().split() 
            l, w, h = int(in_data[0]), int(in_data[1]), int(in_data[2])
            box = [l,w,h]

            #sort the current box for later comparison
            box.sort()
            boxes.append(box)
            boxes.sort()
        #unconditional way of doing this, but it works
        break

    test_g = Graph(boxes)
    print(test_g)
    
    #2n box nodes + 2 source and sink nodes

    #B nodes
    graph = [[0] * (n+2)] * (n)


    #B' nodes
    _graph = [[0] * (n+2)] * (n)


    for i in range(len(boxes)-1):
        for j in range(len(boxes)-1):

            #box_1.l < box'_1.l AND box_1.w < box'_1.w ...
            if boxes[i][0] < boxes[j][0] and boxes[i][1] < boxes[j][1] and boxes[i][2] < boxes[j][2]:  

                #its a match! set edge
                graph[i+1][j+1] += 1
                _graph[j][i+1] += 1

                #set the sink to 1
                graph[0][-1] = 1
                _graph[0][-1] = 1


    #set source list to 1
    source = [1] * (n+2)

    #source does not have an edge to itself
    source[0] = 0

    #source does not have an edge to sink
    source[-1] = 0

    #sing has 0 output edges
    sink = [0] * (n+2)

    #final graph
    t_graph = [source]

    #add box edges to graph
    for i in range(len(graph)):
        t_graph.append(graph[i])

    #add box' edges to graph
    for j in range(len(_graph)):
        t_graph.append(_graph[j])

    #append sink edges
    t_graph.append(sink)


    #new graph
    g = Graph(t_graph)
    print(g)

    #perform maxflow, get maxflow
    m = g.maxFlow(0,n-1)

    #print
    print(n-m, file=sys.stdout)

if __name__ == "__main__":
    driver()
