#
#
#

import math

class Quadrotor2D:

    def __init__(self, _m, _L):
        self.armLength = _L
        self.mass = _m
        self.momentInertia = (_m*(2.0*_L)**2)/12.0  #momento di inerzia approssimato ad una barra di lunghezza 2*L
        self.omega = 0
        self.theta = 0
        self.viscosity = 7e-5  #coefficiente di attrito viscoso 7*10^-5
        self.xVelocity = 0
        self.xPosition = 0
        self.zVelocity = 0
        self.zPosition = 0

    def evaluate(self, f1, f2, delta_t):

        # dinamiche di traslazione sull'asse z
        self.zPosition = self.zPosition + self.zVelocity * delta_t
        tmpVel = (1 - delta_t * self.viscosity / self.mass) * self.zVelocity + delta_t * (f1 + f2) * math.cos(self.theta) / self.mass - 9.81 * delta_t
        self.zVelocity = tmpVel

        if self.zPosition < 0:      #quota 0, non è possibile andare oltre
            self.zPosition = 0
            self.zVelocity = 0
        # dinamiche di traslazione sull'asse x
        self.xPosition = self.xPosition + self.xVelocity * delta_t
        self.xVelocity = (1 - delta_t * self.viscosity / self.mass) * self.xVelocity + delta_t * (f1 + f2) * math.sin(-self.theta) / self.mass
        # rotazione del multirotore
        self.theta = self.theta + self.omega * delta_t

        tmpOmega = self.omega + delta_t * (f2 - f1) * self.armLength / self.momentInertia
        self.omega = tmpOmega
