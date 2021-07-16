import math

def distanceCouple(tuple1,tuple2):
    return math.sqrt((tuple1[0]-tuple2[0])**2 + (tuple1[1]-tuple2[1])**2)

def readNodesCoordsAndEdges(fileName):
    f= open(fileName,"r")
    
    nodes = dict()
    block_slot_nodes = dict()
    tower_slot_nodes = dict()
    edgesTmp = []
    edges = []

    fl =f.readlines()
    for line in fl:
        elems = line.replace("\n","").replace(" ","").split(';')
        coords = elems[1].split(',')
        nodes[elems[0]] = (int(coords[0]), int(coords[1]))
        # Save block slots in a different dictionary with a lower position
        # nodes are in the air, blocks are located on the floor or on a shelf
        if "tow" in elems[0]:
            tower_slot_nodes[elems[0]] = (float(coords[0])/100, float(coords[1])/100)
        if "gen" in elems[0]:
            block_slot_nodes[elems[0]] = (float(coords[0])/100, float(coords[1])/100 + 1)
        adj_list = elems[2].split(',')
        for n in adj_list:
            if(elems[0] and n):
                edgesTmp.append((n, elems[0]))
                edgesTmp.append((elems[0], n))
    for edge in edgesTmp:
        distance = distanceCouple(nodes[edge[0]],nodes[edge[1]])   
        edges.append((edge[0],edge[1],int(math.ceil(distance))))


    return nodes, block_slot_nodes, tower_slot_nodes, edges