#
# x controller
#

from controllori import *

class XController:

    def __init__(self, _multirotor, accel, decel, _kp_x, _kp_vx, _ki_vx, _kd_vx, _vx_sat, _theta_sat):
        self.multirotor = _multirotor
        self.vx_controller = PID_SAT_Controller(_kp_vx, _ki_vx, _kd_vx, _theta_sat)
        self.x_controller = ProfilePositionController(_vx_sat,accel,decel) #P_SAT_Controller(_kp_x, _vx_sat)
        self.x_controller = PID_SAT_Controller(_kp_x, 0.0, 0.0, _vx_sat)

    def evaluate(self, x_target, delta_t):
        x_error = x_target - self.multirotor.xPosition
        self.vx_target = self.x_controller.evaluate(x_error, delta_t)
        #self.vx_target = self.x_controller.evaluate(x_target,self.multirotor.xPosition,self.multirotor.xVelocity,delta_t)

        vx_error = self.vx_target - self.multirotor.xVelocity
        theta_target = self.vx_controller.evaluate(vx_error, delta_t)

        return theta_target

