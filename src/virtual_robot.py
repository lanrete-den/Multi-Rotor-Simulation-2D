#
#
#

import math

class VirtualRobotPositionController():

    def __init__(self, quadrotor, vmax, accel, decel):
        self.vmax = vmax
        self.accel = accel
        self.decel = decel
        self.decel_distance = self.vmax * self.vmax / (2 * self.decel)
        self.decel_time = self.vmax / self.decel
        self.current_time = 0
        self.virtual_robot_speed = 0
        self.virtual_robot_pos = 0
        self.quadrotor = quadrotor
        self.threshold = 0.005 # 5mm


    def set_target(self, x, z):
        self.target_x = x
        self.target_z = z
        self.current_time = 0
        self.virtual_robot_speed = 0
        self.virtual_robot_pos = 0

        pos_x, pos_z = self.quadrotor.get_pose_xz()
        dx = self.target_x - pos_x
        dz = self.target_z - pos_z
        self.linear_distance = math.hypot(dx, dz)
        self.heading = math.atan2(dz,dx)
        self.start_x = pos_x
        self.start_z = pos_z


    def compute_virtual_robot_pos(self, delta_t):
        pos_error = self.linear_distance - self.virtual_robot_pos
        if pos_error < 0:
            pos_error = 0
        if pos_error < self.decel_distance:
            expected_speed = math.sqrt(self.vmax*self.vmax - 2 * self.decel * (self.decel_distance - pos_error))
            if expected_speed > self.virtual_robot_speed:
                # siamo ancora in fase di accelerazione
                current_accel = self.accel
            else:
                # fase di decelerazione
                current_accel = -self.decel
        else:
            # fase di accelerazione o moto a vel costante
            current_accel = self.accel

        self.virtual_robot_speed = self.virtual_robot_speed + current_accel * delta_t

        if self.virtual_robot_speed >= self.vmax:
            self.virtual_robot_speed = self.vmax
            current_accel = 0

        if self.virtual_robot_speed <= 0:
            self.virtual_robot_speed = 0
            current_accel = 0

        self.virtual_robot_pos = self.virtual_robot_pos + self.virtual_robot_speed * delta_t + \
          0.5 * current_accel * delta_t * delta_t

    def evaluate(self, delta_t):
        self.compute_virtual_robot_pos(delta_t)
        x_temp = self.virtual_robot_pos * math.cos(self.heading) + self.start_x
        z_temp = self.virtual_robot_pos * math.sin(self.heading) + self.start_z
        #print(x_temp,y_temp)
        return x_temp, z_temp

    def evaluate2(self, delta_t):
        pos_x, pos_z = self.quadrotor.get_pose_xz()
        dx = self.target_x - pos_x
        dz = self.target_z - pos_z
        distance = math.hypot(dx, dz)
        if distance < self.threshold:
            #self._target_got = True
            self.motion.evaluate(0.0, 0.0, delta_t)
        else:
            #self._target_got = False
            self.compute_virtual_robot_pos(delta_t)
            x_temp = self.virtual_robot_pos * math.cos(self.heading) + self.start_x
            y_temp = self.virtual_robot_pos * math.sin(self.heading) + self.start_y
            #print(x_temp,y_temp)
            return x_temp, y_temp



