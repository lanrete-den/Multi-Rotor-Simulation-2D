#
#
#

import pylab
import math

from autopilot import *

autopilot = Autopilot(testing=True)

t = 0
delta_t = 1e-3

vettore_tempi = []

vettore_z = []
vettore_z_t = []

vettore_vz = []
vettore_vz_t = []

autopilot.z_target = 20

while t < 10:
    autopilot.run(delta_t)
    t = t + delta_t

    vettore_tempi.append(t)
    vettore_vz.append(autopilot.quadrotor.zVelocity)
    vettore_vz_t.append(autopilot.z_controller.vz_target)

    vettore_z.append(autopilot.quadrotor.zPosition)
    vettore_z_t.append(autopilot.z_target)

pylab.figure(1)
pylab.plot(vettore_tempi, vettore_vz, 'r-+', label="Vz")
pylab.plot(vettore_tempi, vettore_vz_t, 'b-+', label="Vz target")
pylab.legend()

pylab.figure(2)
pylab.plot(vettore_tempi, vettore_z, 'r-+', label="Z")
pylab.plot(vettore_tempi, vettore_z_t, 'b-+', label="Z Target")
pylab.legend()

pylab.show()

