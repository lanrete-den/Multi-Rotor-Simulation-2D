#
#
#

import math

from quadrotor_model import *
from angle_control import *
from z_control import *
from x_control import *

class Autopilot:

    def __init__(self):
        self.quadrotor = Quadrotor2D(1.5, 0.25)   #mass of 1.5 kg and 0.25 arm length from the center of the multirotor to the propeller
        self.angle_controller = AngleController(self.quadrotor,
                                                4.0, # kp theta
                                                2.0, # kp omega
                                                0.2, # ki omega
                                                math.radians(80), # omega_max
                                                15)  # delta_f max

        self.z_controller = ZController(self.quadrotor,
                                                4.0, # kp z
                                                20.0, # kp vz
                                                40.0, # ki vz
                                                2, # vz_max
                                                20)  # f max total of the two propellers

        self.x_controller = XController(self.quadrotor,
                                                0.2, # kp x
                                                1.0, # kp vx
                                                0.1, # ki vx
                                                4, # vx_max = 4 m/s
                                                math.radians(25))  # theta max ~25 degrees
        self.theta_target = 0
        self.z_target = 0
        self.x_target = 0

    def run(self, delta_t):
        self.power = self.z_controller.evaluate(self.z_target, delta_t)
        self.theta_target = - self.x_controller.evaluate(self.x_target, delta_t)
        delta_f = self.angle_controller.evaluate(self.theta_target, delta_t)
        self.quadrotor.evaluate(self.power - delta_f, self.power + delta_f, delta_t)




