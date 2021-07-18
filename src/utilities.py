import math


def pixel_to_meter(x,z,window_width,window_height,dronepos):
    x_meter = (window_width/2 - dronepos[0] -x)
    z_meter = (window_height - dronepos[1] -z)
    return x_meter, z_meter 


def distanceCouple(tuple1,tuple2):
    return math.sqrt((tuple1[0]-tuple2[0])**2 + (tuple1[1]-tuple2[1])**2)

def rotate_point(cx, cy, px , py, angle):
     return math.cos(angle) * (px - cx) - math.sin(angle) * (py - cy) + cx, math.sin(angle) * (px - cx) + math.cos(angle) * (py - cy) + cy

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