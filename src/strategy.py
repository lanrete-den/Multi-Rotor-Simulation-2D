
from phidias.Types import *
from phidias.Lib import *
from phidias.Main import *
from phidias.Agent import *

from utilities import *


class blockSlot(Belief): pass
class slotNotChecked(Belief): pass
class towerSlot(Belief): pass
class link(Belief): pass
class selected(SingletonBelief): pass

class path(Procedure): pass
class select_min(Procedure): pass
class show_min(Procedure): pass
class follow_path(Procedure) : pass
class generate_and_follow_min_path(Procedure) : pass
class pick(Procedure) : pass
class restoreSlots(Procedure) : pass
class go(Procedure) : pass
class send_heldBlock(Procedure) : pass
class send_releaseBlock(Procedure) : pass
class go_node(Procedure) : pass
class sense(Procedure) : pass
class generate(Procedure) : pass
class go_to_tower(Procedure): pass

#belief of server
class go_to_node(Belief): pass
class go_to(Belief): pass
class send_held_block(Belief): pass
class sense_color(Belief): pass
class sense_distance(Belief): pass
class generate_blocks(Belief): pass
class releaseBlockToTower(Belief): pass

#reactor
class target_got(Reactor): pass
class distance(Reactor): pass
class color(Reactor): pass

class droneNode(SingletonBelief): pass
class targetNode(SingletonBelief): pass
class targetIntermediateNode(SingletonBelief): pass
class heldBlock(SingletonBelief): pass
class targetReached(SingletonBelief):pass
class selected_path(SingletonBelief): pass

class towerColor(Belief): pass
class block(Belief): pass

class closeTargetNode(Goal): pass

#testtttttting
class not_navigating(SingletonBelief): pass


class nodeNotInPath(ActiveBelief):
  def evaluate(self, P, Node):
    return (Node() not in P())


def_vars('Src', 'Dest', 'Next', 'Cost', 'P', 'Total', 'CurrentMin', 'CurrentMinCost','Node','drone','pathLength','N','currentTarget','X','Z','C','_A','D')
class main(Agent):
    def main(self):



      generate_and_follow_min_path(Node,P,N,pathLength) / (blockSlot(Node) & droneNode(drone)) >> [
                                  show_line(Node," generazione ",P," e seguo path ", N,pathLength),
                                  path(drone,Node,P),
                                  "N = 1",
                                  #"pathLength = len(P)",
                                  +targetReached(drone),
                                  follow_path(drone)
                                  ]
      generate_and_follow_min_path(Node,P,N,pathLength) / (towerColor(Node,C) & droneNode(drone)) >> [
                                  show_line(Node," generazione ",P," e seguo path  per tower ", N,pathLength),
                                  path(drone,Node,P),
                                  "N = 1",
                                  #"pathLength = len(P)",
                                  +targetReached(drone),
                                  follow_path(drone)
                                  ]
      pick() / (blockSlot(Node) & slotNotChecked(Node)) >> [
        pick(Node)
      ]
      pick() >> [
        show_line("Finished scanning all slots"), 
        restoreSlots()
      ]

      #pick() >> [pick("genG")]

      pick(Node) / (slotNotChecked(Node) & blockSlot(Node) & droneNode(drone) & not_navigating(C)) >> [ 
                                  show_line("picking"),
                                  +targetNode(Node),
                                  -not_navigating(C),
                                  generate_and_follow_min_path(Node,[],0,0),
                                  pick()
                                  ]

      
      #pick(Node) >> [ show_line("Finished scanning all slots"), restoreSlots() ]
      
      #pick(Node) >> [ show_line(" not campo, not stanco") ]

      restoreSlots()['all'] / blockSlot(Node) >> [ +slotNotChecked(Node) ]

      go(X,Z) >> [ +go_to(X,Z)[{'to': 'robot@127.0.0.1:6566'}] ]

      send_heldBlock(Node) >> [ +send_held_block(Node)[{'to': 'robot@127.0.0.1:6566'}] ]

      send_releaseBlock() >> [ +releaseBlockToTower()[{'to': 'robot@127.0.0.1:6566'}] ]

      go_node(Node)  >> [ show_line("sending the go node request"),
                          +go_to_node(Node)[{'to': 'robot@127.0.0.1:6566'}] ]

      follow_path(currentTarget) / (selected_path(P,pathLength,N) & eq(pathLength, N)) >> [ 
                                              show_line("target reached"),
                                              "N = 1"
                                              ]

      follow_path(currentTarget) / (targetReached(Node) & selected_path(P,pathLength,N) ) >> [ 
                        show_line("current node reached ",Node, "with index ", N),
                        "currentTarget = P[N]",
                        "N = N+1",
                        +selected_path(P,pathLength,N),
                        +targetIntermediateNode(currentTarget),
                        -targetReached(Node),
                        show_line("current target ",currentTarget, "next index ", N),
                        go_node(currentTarget)
                        ]
      follow_path(currentTarget) >> []
      
      sense() / heldBlock(X,C) >> [ ]


      sense() >> [ 
        show_line("sto sensando"),
        +sense_distance()[{'to': 'robot@127.0.0.1:6566'}],
                     +sense_color()[{'to': 'robot@127.0.0.1:6566'}] ]


      generate() >> [ 
        show_line("generazione 6 blocchi"),
        +generate_blocks(6)[{'to': 'robot@127.0.0.1:6566'}] ]
      generate(N) / gt(N,6) >> [ show_line("cannot generate more than 6 blocks") ]
      generate(N) >> [
        show_line("generazione ",N," blocchi"), 
        +generate_blocks(N)[{'to': 'robot@127.0.0.1:6566'}] ]


      path(Src, Dest,P) >> \
        [
            path(P, 0, Src, Dest),
            show_min(P)
        ]

      path(P, Total, Dest, Dest) >> \
        [ 
            "P.append(Dest)", 
            +selected(P, Total)
        ]

      path(P, Total, Src,  Dest)['all'] / (link(Src,Next,Cost) & nodeNotInPath(P,Next))  >> \
        [
            #show_line(P," path , ",Next," next"),
            "P = P.copy()",
            "P.append(Src)",
            "Total = Total + Cost",
            select_min(P, Total, Next, Dest)
        ]

      select_min(P, Total, Next, Dest) / (selected(CurrentMin, CurrentMinCost) & gt(Total, CurrentMinCost)) >> \
        [
          #show_line("path cut")
        ]
      select_min(P, Total, Next, Dest) >> \
        [
            path(P, Total, Next, Dest)
        ]

      show_min(P) / selected(CurrentMin, CurrentMinCost)  >> \
        [
            show_line("Minimum Cost Path ", CurrentMin, ", cost ", CurrentMinCost),
            "pathLength = len(CurrentMin)",
            +selected_path(CurrentMin,pathLength,1),
            -selected(CurrentMin,CurrentMinCost),
            show_line("Lunghezza array: ", pathLength)
        ] 

      +target_got()[{'from': _A}] / (targetIntermediateNode(Node) & targetNode(Node) & slotNotChecked(X) ) >> \
        [
            show_line('Reached Node ', Node),
            +targetReached(Node),
            -slotNotChecked(Node),
            +not_navigating("1"),
            sense()
        ]

      +target_got()[{'from': _A}] / (targetIntermediateNode(X) & droneNode(drone)) >> \
        [
            show_line('Reached Node intermediate ', X),
            +targetReached(X),
            +droneNode(X),
            sense(),
            -slotNotChecked(X),
            follow_path(X)
        ]
      

      closeTargetNode(Node,D) << (targetNode(Node) & lt(D,1.5))

      +distance(D)[{'from':_A}] / closeTargetNode(Node,D) >> [ 
                                                                    show_line("Block found in slot ", X),
                                                                    +block(Node)]

      +color(C)[{'from':_A}] / ( block(X) & towerColor(Node,C)) >> [ 
                                                              show_line("Color ", C, " sampled in slot", X),
                                                              -block(X),
                                                              +heldBlock(X,C),
                                                              -slotNotChecked(X),
                                                              send_heldBlock(X),
                                                              +targetNode(Node),
                                                              go_to_tower(Node)
                                                              ]
      
      go_to_tower(Node) / heldBlock(X,C) >> [ generate_and_follow_min_path(Node,[],0,0), -heldBlock(X,C), send_releaseBlock(), +not_navigating("1") ]





ag = main()
ag.start()
nodes, block_slots, tower_slots, edges = readNodesCoordsAndEdges("nodes.txt")
for edge in edges:
  ag.assert_belief(link(edge[0],edge[1],edge[2]))
for block_slot in block_slots:
  ag.assert_belief(blockSlot(block_slot))
  ag.assert_belief(slotNotChecked(block_slot))

ag.assert_belief(droneNode("Start"))
ag.assert_belief(not_navigating("1"))
#for tower_slot in tower_slots:
#  ag.assert_belief(towerSlot(tower_slot))
#  ag.assert_belief
ag.assert_belief(towerColor("tow_red","red"))
ag.assert_belief(towerColor("tow_green","green"))
ag.assert_belief(towerColor("tow_blue","blue"))
#PHIDIAS.run()
PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())
