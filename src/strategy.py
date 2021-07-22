
from phidias.Types import *
from phidias.Lib import *
from phidias.Main import *
from phidias.Agent import *

from utilities import *

# ------- World information ------- #

# Graph nodes where there are potentially blocks
class blockSlot(Belief): pass
class block(SingletonBelief): pass

# Current held block (if present)
class heldBlock(SingletonBelief): pass

# Information about towers: node (position), color, current number of blocks
class towerColor(Belief): pass

# Graph links
class link(Belief): pass

# ------- Navigation ------- #

# Min path generation beliefs
class selected(SingletonBelief): pass
class path(Procedure): pass
class select_min(Procedure): pass
class show_min(Procedure): pass

# ActiveBelief to prevent cyclic paths
class nodeNotInPath(ActiveBelief):
  def evaluate(self, P, Node):
    return (Node() not in P())

# Graph navigation beliefs
class droneNode(SingletonBelief): pass
class targetNode(SingletonBelief): pass
class targetIntermediateNode(SingletonBelief): pass
class targetReached(SingletonBelief):pass
class selected_path(SingletonBelief): pass
class not_navigating(SingletonBelief): pass

# Graph navigation procedures
class follow_path(Procedure) : pass
class generate_and_follow_min_path(Procedure) : pass
class go_to_tower(Procedure): pass
class go_to_start(Procedure): pass

# Goal to check if drone is close enough to the node
class closeDroneNode(Goal): pass

# Procedure to scan the world with the drone and put blocks in the corresponding towers
class pick(Procedure) : pass

# Block nodes currently not checked by the drone
class slotNotChecked(Belief): pass

# Procedure to uncheck block slots when generating new blocks or when the world scan has ended
class restoreSlots(Procedure) : pass

# Remove tower blocks from kb when resetting towers
class remove_towers_blocks(Procedure): pass

# ------- Comunication ------- #

# Procedures that talk to GUI server
class send_heldBlock(Procedure) : pass
class send_releaseBlock(Procedure) : pass
class sense(Procedure) : pass
class generate(Procedure) : pass
class go_node(Procedure) : pass
class go(Procedure) : pass
class reset_towers(Procedure): pass

# Server beliefs
class go_to_node(Belief): pass
class go_to(Belief): pass
class send_held_block(Belief): pass
class sense_color(Belief): pass
class sense_distance(Belief): pass
class generate_blocks(Belief): pass
class releaseBlockToTower(Belief): pass
class resetTowers(Belief):pass

# Reactors
class target_got(Reactor): pass
class distance(Reactor): pass
class color(Reactor): pass


def_vars('Src', 'Dest', 'Next', 'Cost', 'P', 'Total', 'CurrentMin', 'CurrentMinCost','Node','drone','pathLength','N','currentTarget','X','Z','C','_A','D')
class main(Agent):
    def main(self):

      go_to_start() / droneNode(drone) >> [
                                  show_line("Ritorno alla posizione Start"),
                                  path(drone,"Start",[]),
                                  "N = 1",
                                  +targetReached(drone),
                                  follow_path(drone)
                                  ]

      generate_and_follow_min_path(Node,P,N,pathLength) / (blockSlot(Node) & droneNode(drone)) >> [
                                  show_line(Node," generazione ",P," e seguo path ", N,pathLength),
                                  path(drone,Node,P),
                                  "N = 1",
                                  +targetReached(drone),
                                  follow_path(drone)
                                  ]

      generate_and_follow_min_path(Node,P,N,pathLength) / (towerColor(Node,C,X) & droneNode(drone)) >> [
                                  show_line(Node," generazione ",P," e seguo path  per tower ", N,pathLength),
                                  path(drone,Node,P),
                                  "N = 1",
                                  +targetReached(drone),
                                  follow_path(drone)
                                  ]

      pick() / (blockSlot(Node) & slotNotChecked(Node)) >> [
        pick(Node)
      ]
      pick() >> [
        show_line("Finished scanning all slots"), 
        go_to_start()
      ]

      pick(Node) / (slotNotChecked(Node) & blockSlot(Node) & droneNode(drone) & not_navigating(C)) >> [ 
                                  show_line("picking"),
                                  +targetNode(Node),
                                  -not_navigating(C),
                                  generate_and_follow_min_path(Node,[],0,0)
                                  ]

      restoreSlots()['all'] / blockSlot(Node) >> [+slotNotChecked(Node) ]

      go(X,Z) >> [ +go_to(X,Z)[{'to': 'robot@127.0.0.1:6566'}] ]

      send_heldBlock(Node) >> [ +send_held_block(Node)[{'to': 'robot@127.0.0.1:6566'}] ]

      send_releaseBlock() >> [ +releaseBlockToTower()[{'to': 'robot@127.0.0.1:6566'}] ]

      go_node(Node)  >> [ show_line("sending the go node request"),
                          +go_to_node(Node)[{'to': 'robot@127.0.0.1:6566'}] ]

      remove_towers_blocks()['all'] / towerColor(Node,C,N) >> [
        -towerColor(Node,C,N),
        +towerColor(Node,C,0)
      ]

      reset_towers() >> [
        remove_towers_blocks(), 
        +resetTowers()[{'to': 'robot@127.0.0.1:6566'}],
        ]

      #follow_path(currentTarget) / sensing(C) >> [show_line("currently sensing, not following path")]

      follow_path(currentTarget) / (selected_path(P,pathLength,N) & eq(pathLength, N)) >> [ 
                                              show_line("target reached"),
                                              "N = 1"
                                              ]

      follow_path(currentTarget) / (targetReached(Node) & selected_path(P,pathLength,N) ) >> [ 
                        show_line("current node reached ",Node, " with index ", N),
                        "currentTarget = P[N]",
                        "N = N+1",
                        +selected_path(P,pathLength,N),
                        +targetIntermediateNode(currentTarget),
                        -targetReached(Node),
                        show_line("current target ",currentTarget, " next index ", N),
                        go_node(currentTarget)
                        ]

      follow_path(currentTarget) >> []
      
      sense() / heldBlock(X,C) >> [ follow_path(X)]

      sense() >> [ 
        show_line("sensing"),
        +sense_distance()[{'to': 'robot@127.0.0.1:6566'}],
                     +sense_color()[{'to': 'robot@127.0.0.1:6566'}] ]


      generate() >> [ 
        show_line("generazione 6 blocchi"),
        +generate_blocks(6)[{'to': 'robot@127.0.0.1:6566'}] ,
        restoreSlots()]
      generate(N) / gt(N,6) >> [ show_line("cannot generate more than 6 blocks") ]
      generate(N) >> [
        show_line("generazione ",N," blocchi"), 
        +generate_blocks(N)[{'to': 'robot@127.0.0.1:6566'}], 
        restoreSlots()]


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
      
      path(P, Total, Node,  Dest) / (link(Node,Dest,Cost) & nodeNotInPath(P,Dest))  >> \
        [
            #show_line(P," path , ",Next," next"),
            "P = P.copy()",
            "P.append(Node)",
            "Total = Total + Cost",
            select_min(P, Total, Dest, Dest)
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
        ] 

      +target_got()[{'from': _A}] / (targetIntermediateNode(Node) & targetNode(Node) & heldBlock(X,C) & towerColor(Node,C,N) ) >> \
        [
            show_line('Reached Tower ', Node),
            +targetReached(Node),
            +droneNode(Node),
            +not_navigating("1"),
            -heldBlock(X,C),
            send_releaseBlock(),
            pick()
        ]

      +target_got()[{'from': _A}] / (targetIntermediateNode(Node) & eq(Node, "Start") ) >> \
        [
            #show_line('Reached starting node ', Node),
            +targetReached(Node),
            +droneNode(Node),
            restoreSlots()
        ]

      +target_got()[{'from': _A}] / (targetIntermediateNode(Node) & targetNode(Node) ) >> \
        [
            show_line('Reached Node ', Node),
            +targetReached(Node),
            +droneNode(Node),
            -slotNotChecked(Node),
            show_line("checked slot node ",Node),
            +not_navigating("1"),
            sense(),
            pick()
        ]

      +target_got()[{'from': _A}] / (targetIntermediateNode(X)) >> \
        [
            #show_line('Reached Node intermediate ', X),
            +targetReached(X),
            +droneNode(X),
            show_line("checked slot node intermidiate ",X),
            -slotNotChecked(X),
            sense()
            #follow_path(X)
        ]      

      closeDroneNode(Node,D) << (droneNode(Node) & lt(D,1.22))


      +distance(D)[{'from':_A}] / closeDroneNode(Node,D) >> [ 
                                                                    show_line("Block found in slot ", Node),
                                                                    +block(Node)
                                                                    ]

      +distance(D) [{'from':_A}] /droneNode(drone) >> [follow_path(drone)]

      +color(C)[{'from':_A}] / ( block(X) & towerColor(Node,C,N) & geq(N,3) ) >> [ 
                                                              show_line("Tower ", C, " full, cannot pick block sampled in slot ", X),
                                                              -block(X),
                                                              -slotNotChecked(X),
                                                              +not_navigating("1"),
                                                              pick()
                                                              ]

      +color(C)[{'from':_A}] / ( block(X) & towerColor(Node,C,N) & lt(N,4) ) >> [ 
                                                              show_line("Color ", C, " sampled in slot ", X),
                                                              -block(X),
                                                              +heldBlock(X,C),
                                                              -slotNotChecked(X),
                                                              send_heldBlock(X),
                                                              +targetNode(Node),
                                                              go_to_tower(Node)
                                                              ]

      
      
      go_to_tower(Node) / (heldBlock(X,C) & towerColor(Node,C,Z))  >> [
          #show_line("trying to go to tower ",Node, " with color ", C,"and length ",Z),
          -towerColor(Node,C,Z),
          "Z = Z+1", 
          +towerColor(Node,C,Z),
          generate_and_follow_min_path(Node,[],0,0), 
      ]





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

ag.assert_belief(towerColor("tow_red","red",0))
ag.assert_belief(towerColor("tow_green","green",0))
ag.assert_belief(towerColor("tow_blue","blue",0))

PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())
