import math

def distanceCouple(tuple1,tuple2):
    return math.sqrt((tuple1[0]-tuple2[0])^2 + (tuple1[1]-tuple2[1])^2)

def readNodesCoordsAndEdges(fileName):
    f= open(fileName,"r")
    
    nodes = dict()
    edgesTmp = []
    edges = []

    fl =f.readlines()
    for line in fl:
        elems = line.split(';')
        nodes[elems[0]] = (int(elems[1].split(',')[0]), int(elems[1].split(',')[1]))
        adj_list = elems[2].split(',')
        for n in adj_list:
            edgesTmp.append((n, elems[0]))
            edgesTmp.append((elems[0], n))
    for edge in edgesTmp:
        distance = distanceCouple(nodes[edge[0]],nodes[edge[1]])   
        edges.append((edge[0],edge[1],distance))

    return nodes, edges