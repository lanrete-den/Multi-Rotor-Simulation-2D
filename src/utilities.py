

def readNodesCoordsAndEdges(fileName):
    f= open("nodes.txt","r")
    
    nodes = dict()
    edges = []

    fl =f.readlines()
    for line in fl:
        elems = line.split(';')
        nodes[elems[0]] = (int(elems[1].split(',')[0]), int(elems[1].split(',')[1]))
        adj_list = elems[2].split(',')
        for n in adj_list:
            edges.append((elems[0], n))
    return nodes, edges