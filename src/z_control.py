#
# z controller
#

from controllori import *

class ZController:

    def __init__(self, _multirotor, _kp_z, _kp_vz, _ki_vz, _vz_sat, _power_sat):
        self.multirotor = _multirotor
        self.vz_controller = PI_SAT_Controller(_kp_vz, _ki_vz, _power_sat)
        self.z_controller = P_SAT_Controller(_kp_z, _vz_sat)

    def evaluate(self, z_target, delta_t):
        z_error = z_target - self.multirotor.zPosition
        self.vz_target = self.z_controller.evaluate(z_error)

        vz_error = self.vz_target - self.multirotor.zVelocity
        power = self.vz_controller.evaluate(vz_error, delta_t)

        return power

