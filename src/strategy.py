
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


def_vars('Source', 'Target', 'Next', 'Cost', 'P', 'Total', 'CurrentMin', 'CurrentMinCost')
class main(Agent):
    def main(self):

      gen_block() >> [ +new_block()[{'to': 'robot@127.0.0.1:6566'}] ]

      gen_block(0) >> [ ]
      gen_block(N) >> [ gen_block(), "N = N - 1", gen_block(N) ]

      path(Src, Dest) >> \
        [
            path([], 0, Src, Dest),
            show_min()
        ]

      path(P, Total, Dest, Dest) >> \
        [ 
            "P.append(Dest)", 
            show_line(P, " ", Total),
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
            show_line(P, " ", Next, ", cost ", Total, " [CUT]")
        ]
      select_min(P, Total, Next, Dest) >> \
        [
            path(P, Total, Next, Dest)
        ]

      show_min() / selected(CurrentMin, CurrentMinCost)  >> \
        [
            show_line("Minimum Cost Path ", CurrentMin, ", cost ", CurrentMinCost)
        ]




ag = main()
ag.start()
nodes, edges = readNodesCoordsAndEdges("nodes.txt")
for edge in edges:
  ag.assert_belief(link(edge[0],edge[1],edge[2]))
  if("gen" in edge[0]):
    ag.assert_belief(blockSlot(edge[0]))
  if("gen" in edge[1]):
    ag.assert_belief(blockSlot(edge[1]))
  if("tow" in edge[1]):
    ag.assert_belief(towerSlot(edge[1]))
  if("tow" in edge[0]):
    ag.assert_belief(towerSlot(edge[0]))

#PHIDIAS.run()
PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())
