#
#
#

import math
from utilities import *

from quadrotor_model import *
from angle_control import *
from z_control import *
from x_control import *

from virtual_robot import VirtualRobotPositionController

class AutopilotPID:

    def __init__(self, testing=False):
        self.quadrotor = Quadrotor2D(1.5, 0.25, testing)   #mass of 1.5 kg and 0.25 arm length from the center of the multirotor to the propeller
        self.angle_controller = AngleController(self.quadrotor,
                                                15.0, # kp theta 4.0
                                                8.0, # kp omega 2.0
                                                0.2, # ki omega 0.2
                                                0, # kd omega
                                                80*0.017453, # omega_max
                                                15)  # delta_f max

        self.z_controller = ZController(self.quadrotor,
                                                50.0, # kp z
                                                1000.0, # kp vz
                                                50.0, # ki vz
                                                2, # vz_max
                                                20)  # f max total of the two propellers

        self.x_controller = XController(self.quadrotor,
                                                0.7, # starting phase acceleration
                                                0.3, # ending phase deceleration
                                                1.0, # kp x
                                                11.3, # kp vx #0.7  ##1.5
                                                0.1, # ki vx #0.6  ##0.1
                                                1.6, # kd vx #0.1  ##0.3
                                                4, # vx_max = 4 m/s
                                                math.radians(25))  # theta max ~25 degrees
        self.virtual_robot = VirtualRobotPositionController(self.quadrotor,4.0,0.7,0.3)
        self.use_virtual_robot = False
        self.theta_target = 0
        self.z_target = 0
        self.x_target = 0
        self.virtual_robot.set_target(0,0)
        self.target_got = False

    def run(self, delta_t):
        if self.use_virtual_robot:
            current_x_target, current_z_target = self.virtual_robot.evaluate(delta_t)
        else:
            current_x_target, current_z_target = self.x_target, self.z_target
        self.power = self.z_controller.evaluate(current_z_target, delta_t)
        self.theta_target = - self.x_controller.evaluate(current_x_target, delta_t)
        delta_f = self.angle_controller.evaluate(self.theta_target, delta_t)
        self.quadrotor.evaluate(self.power - delta_f, self.power + delta_f, delta_t)
        if(distanceCouple(self.quadrotor.get_pose_xz(),(self.x_target,self.z_target)) <0.01 ):
            self.target_got = True
            #print("current x e y " , self.quadrotor.get_pose_xz())
            #print("target x e y " , self.x_target , " " ,self.z_target)   #this should not be printed when distance <0.1
        else:
            self.target_got = False
            
    def set_target(self,x_position,z_position):
        self.z_target = z_position
        self.x_target = x_position
        self.virtual_robot.set_target(x_position, z_position)
        self.target_got = False

    def change_control_type(self, control_type):
        print("Changing x control to ", control_type)
        if control_type == 'virtual_robot':
            self.use_virtual_robot = True
            self.x_controller.use_PID()
        if control_type == 'speed_profile':
            self.use_virtual_robot = False
            self.x_controller.use_speed_profile()
        if control_type == 'PID':
            self.use_virtual_robot = False
            self.x_controller.use_PID()



