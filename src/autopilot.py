#
#
#

import math
from utilities import *

from quadrotor_model import *
from angle_control import *
from z_control import *
from x_control import *

class Autopilot:

    def __init__(self, testing=False):
        self.quadrotor = Quadrotor2D(1.5, 0.25, testing)   #mass of 1.5 kg and 0.25 arm length from the center of the multirotor to the propeller
        self.angle_controller = AngleController(self.quadrotor,
                                                4.0, # kp theta
                                                2.0, # kp omega
                                                0.2, # ki omega
                                                80*0.017453, # omega_max
                                                15)  # delta_f max

        self.z_controller = ZController(self.quadrotor,
                                                4.0, # kp z
                                                20.0, # kp vz
                                                40.0, # ki vz
                                                2, # vz_max
                                                20)  # f max total of the two propellers

        self.x_controller = XController(self.quadrotor,
                                                0.7, # starting phase acceleration
                                                0.3, # ending phase deceleration
                                                0.7, # kp vx #0.7
                                                0.6, # ki vx #0.3
                                                0.1, # kd vx #0.1
                                                4, # vx_max = 4 m/s
                                                math.radians(25))  # theta max ~25 degrees
        self.theta_target = 0
        self.z_target = 0
        self.x_target = 0
        self.target_got = False

    def run(self, delta_t):
        self.power = self.z_controller.evaluate(self.z_target, delta_t)
        self.theta_target = - self.x_controller.evaluate(self.x_target, delta_t)
        delta_f = self.angle_controller.evaluate(self.theta_target, delta_t)
        self.quadrotor.evaluate(self.power - delta_f, self.power + delta_f, delta_t)
        if(distanceCouple(self.quadrotor.get_pose_xz(),(self.x_target,self.z_target)) <0.1 ):
            self.target_got = True
        else:
            self.target_got = False
            
    def set_target(self,x_position,z_position):
        self.z_target = z_position
        self.x_target = x_position




