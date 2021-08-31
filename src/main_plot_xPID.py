import pylab
import math

from autopilotXcontrPID import *

autopilot = AutopilotPID(testing=True)

t = 0
delta_t = 1e-3

vettore_tempi = []

vettore_x = []
vettore_x_t = []

vettore_vx = []
vettore_vx_t = []

vettore_theta = [ ]
vettore_theta_target = [ ]


autopilot.set_target(5,5)

#autopilot.change_control_type('virtual_robot')
#autopilot.change_control_type('speed_profile')
autopilot.change_control_type('PID')

while t < 30:
    autopilot.run(delta_t)
    t = t + delta_t

    vettore_tempi.append(t)
    vettore_vx.append(autopilot.quadrotor.xVelocity)
    vettore_vx_t.append(autopilot.x_controller.vx_target)

    vettore_x.append(autopilot.quadrotor.xPosition)
    vettore_x_t.append(autopilot.x_target)

    vettore_theta.append(autopilot.quadrotor.theta)
    vettore_theta_target.append(autopilot.theta_target)

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
pylab.plot(vettore_tempi, vettore_theta_target, 'b-+', label="Theta target")
pylab.legend()

pylab.show()

