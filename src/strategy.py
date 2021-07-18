
from phidias.Types import *
from phidias.Lib import *
from phidias.Main import *
from utilities import *


class blockSlot(Belief): pass
class towerSlot(Belief): pass
class link(Belief): pass
class path(Procedure): pass
class select_min(Procedure): pass
class show_min(Procedure): pass
class selected(SingletonBelief): pass



class droneNode(SingletonBelief): pass
class targetNode(SingletonBelief): pass
class targetIntermediateNode(SingletonBelief): pass
class heldBlock(SingletonBelief): pass
class targetReached(SingletonBelief):pass

class towerColor(Belief): pass


def_vars('Source', 'Target', 'Next', 'Cost', 'P', 'Total', 'CurrentMin', 'CurrentMinCost','Node','drone','pathLength','N','currentTarget')
class main(Agent):
    def main(self):

      generate_and_follow_min_path(Node) / blockSlot(Node) & droneNode(drone) >> [
                                  path(drone,Node),
                                  "N = 0",
                                  "pathLength = len(P)",
                                  +targetReached(drone)
                                  follow_path()
                                  ]
      generate_and_follow_min_path(Node) / towerSlot(Node) & droneNode(drone) >> [
                                  path(drone,Node),
                                  "N = 0",
                                  "pathLength = len(P)",
                                  +targetReached(drone)
                                  follow_path()
                                  ]

      pick() / blockSlot(Node) & droneNode(drone) >> [ 
                                  +targetNode(Node),
                                  generate_and_follow_min_path(Node)
                                  ]

      go(X,Z) >> [ +go_to(X,Z)[{'to': 'robot@127.0.0.1:6566'}] ]

      send_heldBlock(Node) >> [ +heldBlock(Node)[{'to': 'robot@127.0.0.1:6566'}] ]

      send_releaseBlock() >> [ +releaseBlockToTower()[{'to': 'robot@127.0.0.1:6566'}] ]

      go_node(Node)  >> [ +go_to_node(Node)[{'to': 'robot@127.0.0.1:6566'}] ]

      follow_path() / eq(pathLength, N) >> [ show_line("target reached"),
                                              "N = 0"]

      follow_path() / targetReached(Node) >> [ "currentTarget = P[N]",
                        "N = N+1",
                        +targetIntermediateNode(currentTarget),
                        go_node(currentTarget),
                        ]
      
      sense() / heldBlock(X,C) >> [ ]

      next_node() >> []

      sense() >> [ +sense_distance()[{'to': 'robot@127.0.0.1:6566'}],
                     +sense_color()[{'to': 'robot@127.0.0.1:6566'}] ]


      generate() >> [ +generate(6)[{'to': 'robot@127.0.0.1:6566'}] ]
      generate(N) >> [ +generate(N)[{'to': 'robot@127.0.0.1:6566'}] ]

      path(Src, Dest) >> \
        [
            path([], 0, Src, Dest),
            show_min()
        ]

      path(P, Total, Dest, Dest) >> \
        [ 
            "P.append(Dest)", 
            +selected(P, Total)
        ]
      path(P, Total, Src,  Dest)['all'] / link(Src,Next,Cost) >> \
        [
            "P = P.copy()",
            "P.append(Src)",
            "Total = Total + Cost",
            select_min(P, Total, Next, Dest)
        ]

      select_min(P, Total, Next, Dest) / (selected(CurrentMin, CurrentMinCost) & gt(Total, CurrentMinCost)) >> \
        [
        ]
      select_min(P, Total, Next, Dest) >> \
        [
            path(P, Total, Next, Dest)
        ]

      show_min() / selected(CurrentMin, CurrentMinCost)  >> \
        [
            show_line("Minimum Cost Path ", CurrentMin, ", cost ", CurrentMinCost)
        ]
        # TODO 

      +target_got()[{'from': _A}] / targetIntermediateNode(X) & droneNode(drone) >> \
        [
            show_line('Reached Node ', X),
            +targetReached(X),
            "drone = X",
            sense(),
            follow_path()
        ]
      +target_got()[{'from': _A}] / targetNode(X) >> \
        [
            show_line('Reached Node ', X),
            +targetReached(X),
            sense()
        ]

      closeTargetNode(Node,D) << (targetNode(Node) & lt(D,0.035))

      +distance(D)[{'from':_A}] / closeTargetNode(Node,D) >> [ show_line("Block found in slot ", X),
                                                                    +block(X)]

      +color(C)[{'from':_A}] / (targetNode(X) & block(X) & towerColor(Node,C)) >> [ show_line("Color ", C, " sampled in slot", X),
                                                              -block(X),
                                                              +heldBlock(X,C),
                                                              send_heldBlock(X),
                                                              +targetNode(Node),
                                                              go_to_tower(Node)
                                                              ]
      
      go_to_tower(Node) / heldBlock(X,C) >> [ generate_and_follow_min_path(Node), -heldBlock(X,C), send_releaseBlock() ]

      +color(C)[{'from':_A}] >> [ _scan_next() ]
      +color()[{'from':_A}] >> [ _scan_next() ]

      _scan_next() / (targetNode(X)) >> \
        [
            show_line('end')
        ]

      _scan_next() / (targetNode(X) & heldBlock(X,C)) >> \
        [
            show_line('block getting transported')
            go_to_tower
        ]

      _scan_next() / (targetNode(X) & blockSlot(Node)) >> \
        [
            +targetNode(Node),
            go_node(Node)
        ]





ag = main()
ag.start()
nodes, block_slots, tower_slots, edges = readNodesCoordsAndEdges("nodes.txt")
for edge in edges:
  ag.assert_belief(link(edge[0],edge[1],edge[2]))
for block_slot in block_slots:
  ag.assert_belief(blockSlot(block_slot))
#for tower_slot in tower_slots:
#  ag.assert_belief(towerSlot(tower_slot))
#  ag.assert_belief
ag.assert_belief(towerColor("towX","red"))
ag.assert_belief(towerColor("towY","green"))
ag.assert_belief(towerColor("towZ","blue"))
#PHIDIAS.run()
PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())
