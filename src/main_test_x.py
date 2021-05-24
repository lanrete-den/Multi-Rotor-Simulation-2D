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

vettore_x = []
vettore_x_t = []

vettore_vx = []
vettore_vx_t = []

vettore_theta = [ ]

autopilot.x_target = 3
autopilot.z_target = 2

while t < 20:
    autopilot.run(delta_t)
    t = t + delta_t

    vettore_tempi.append(t)
    vettore_vx.append(autopilot.quadrotor.vx)
    vettore_vx_t.append(autopilot.x_controller.vx_target)

    vettore_x.append(autopilot.quadrotor.x)
    vettore_x_t.append(autopilot.x_target)

    vettore_theta.append(autopilot.quadrotor.theta)

pylab.figure(1)
pylab.plot(vettore_tempi, vettore_vx, 'r-+', label="Vx")
pylab.plot(vettore_tempi, vettore_vx_t, 'b-+', label="Vx target")
pylab.legend()

pylab.figure(2)
pylab.plot(vettore_tempi, vettore_x, 'r-+', label="X")
pylab.plot(vettore_tempi, vettore_x_t, 'b-+', label="X Target")
pylab.legend()

pylab.figure(3)
pylab.plot(vettore_tempi, vettore_theta, 'r-+', label="Theta")
pylab.legend()

pylab.show()

