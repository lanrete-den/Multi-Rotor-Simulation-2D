
from phidias.Types import *
from phidias.Lib import *
from phidias.Main import *

class link(Belief): pass
class path(Procedure): pass
class select_min(Procedure): pass
class show_min(Procedure): pass
class selected(SingletonBelief): pass

#
def_vars('Source', 'Target', 'Next', 'Cost', 'P', 'Total', 'CurrentMin', 'CurrentMinCost')

path(Source, Target) >> \
  [
      +selected([], 99999),
      path([], 0, Source, Target),
      show_min()
  ]

path(P, Total, Target, Target) >> \
  [ 
      "P.append(Target)", 
      select_min(P, Total)
  ]
path(P, Total, Source,  Target)['all'] / link(Source,Next,Cost) >> \
  [
      "P = P.copy()",
      "P.append(Source)",
      "Total = Total + Cost",
      path(P, Total, Next, Target)
  ]

select_min(P, Cost) / (selected(CurrentMin, CurrentMinCost) & lt(Cost, CurrentMinCost)) >> \
  [
      +selected(P, Cost)
  ]

show_min() / selected(CurrentMin, CurrentMinCost)  >> \
  [
      show_line("Minimum Cost Path ", CurrentMin, ", cost ", CurrentMinCost)
  ]

PHIDIAS.assert_belief(link('A', 'B', 2))


PHIDIAS.run()
PHIDIAS.shell(globals())