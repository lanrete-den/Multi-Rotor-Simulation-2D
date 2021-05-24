#
# angle controller
#

from controllori import *

class AngleController:

    def __init__(self, _multirotor, _kp_theta, _kp_omega, _ki_omega, _omega_sat, _force_sat):
        self.multirotor = _multirotor
        self.omega_controller = PI_SAT_Controller(_kp_omega, _ki_omega, _force_sat)
        self.theta_controller = P_SAT_Controller(_kp_theta, _omega_sat)

    def evaluate(self, theta_target, delta_t):
        theta_error = theta_target - self.multirotor.theta
        self.omega_target = self.theta_controller.evaluate(theta_error)

        omega_error = self.omega_target - self.multirotor.omega
        delta_f = self.omega_controller.evaluate(omega_error, delta_t)

        return delta_f

