#
#
#
import math

class PathControl:

    def __init__(self, _autopilot):
         self.path = [ ]
         self.autopilot = _autopilot
         self.threshold = 0.2 # 20cm
         self.current_point_index = 0
         self.path_completed = False

    def add_new_point(self, x, z):
         if self.current_point_index >= len(self.path):
             start_path = True
         else:
             start_path = False

         self.path.append( (x, z) )
         if start_path:
             (x, z) = self.path[self.current_point_index]
             self.autopilot.x_target = x
             self.autopilot.z_target = z
             self.path_completed = False


    def run(self, delta_t):
         if self.current_point_index < len(self.path):
             (x, z) = self.path[self.current_point_index]
             current_x = self.autopilot.quadrotor.x
             current_z = self.autopilot.quadrotor.z
             d = math.sqrt ( (x - current_x)**2 + (z - current_z)**2 )
             if d < self.threshold:
                 self.current_point_index = self.current_point_index + 1
                 if self.current_point_index < len(self.path):
                     (x, z) = self.path[self.current_point_index]
                     self.autopilot.x_target = x
                     self.autopilot.z_target = z
                 else:
                     self.path_completed = True

         self.autopilot.run(delta_t)



