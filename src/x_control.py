#
# x controller
#

from controllori import *

class XController:

    def __init__(self, _multirotor, _kp_x, _kp_vx, _ki_vx, _vx_sat, _theta_sat):
        self.multirotor = _multirotor
        self.vx_controller = PI_SAT_Controller(_kp_vx, _ki_vx, _theta_sat)
        self.x_controller = P_SAT_Controller(_kp_x, _vx_sat)

    def evaluate(self, x_target, delta_t):
        x_error = x_target - self.multirotor.x
        self.vx_target = self.x_controller.evaluate(x_error)

        vx_error = self.vx_target - self.multirotor.vx
        theta_target = self.vx_controller.evaluate(vx_error, delta_t)

        return theta_target

