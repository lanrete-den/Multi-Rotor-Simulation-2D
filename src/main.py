#
#
#

import pylab
import math

from autopilot import *

autopilot = Autopilot()

t = 0
delta_t = 1e-3

vettore_tempi = []

vettore_theta = []
vettore_theta_t = []

vettore_omega = []
vettore_omega_t = []

autopilot.theta_target = math.radians(30)

while t < 4:
    autopilot.run(delta_t)
    t = t + delta_t

    vettore_tempi.append(t)
    vettore_omega.append(autopilot.quadrotor.omega)
    vettore_omega_t.append(autopilot.angle_controller.omega_target)

    vettore_theta.append(autopilot.quadrotor.theta)
    vettore_theta_t.append(autopilot.theta_target)

pylab.figure(1)
pylab.plot(vettore_tempi, vettore_omega, 'r-+', label="Omega")
pylab.plot(vettore_tempi, vettore_omega_t, 'b-+', label="Omega target")
pylab.legend()

pylab.figure(2)
pylab.plot(vettore_tempi, vettore_theta, 'r-+', label="Theta")
pylab.plot(vettore_tempi, vettore_theta_t, 'b-+', label="Theta Target")
pylab.legend()

pylab.show()

