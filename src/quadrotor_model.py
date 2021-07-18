#
#
#

import math

from PyQt5.QtGui import QPainter,  QPixmap, QTransform

from utilities import rotate_point

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
        self.x_pos_center = 0
        self.z_pos_center = 0
        self.dronePix = QPixmap("drone.png")  #drone image
        self.held_block = None

    def set_held_block(self,block):
        self.held_block = block
        #x_block, z_block = self.held_block.get_center_pixel_xz()    # si porta il cubo sotto il drone istanteneamente, quindi non si tiene conto della vecchia posizione
        #final_x_block, final_z_block = rotate_point(self.x_pos_center, self.z_pos_center,self.x_pos_center, self.z_pos_center + 10,self.theta) #x_block, z_block, self.theta)
        #self.held_block.set_pose(final_x_block,final_z_block,math.degrees(self.theta))

    def free_block(self):
        temp = self.held_block
        self.held_block = None
        return temp


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

    def get_pose_xz(self):
        return (self.xPosition, self.zPosition)

    def paint(self,qp, window_height,window_width):
        x_pos = window_width/2 - self.dronePix.width()/2 + (self.xPosition * 100)
        z_pos = window_height-(self.dronePix.height())-10 - (self.zPosition * 100)

        s = self.dronePix.size()
        self.x_pos_center = x_pos + s.height()/2
        self.z_pos_center = z_pos + s.width()/2
        
        if(self.held_block is not None):
            #x_block,z_block = self.held_block.get_center_pixel_xz()
            final_x_block, final_z_block = rotate_point(self.x_pos_center,self.z_pos_center,self.x_pos_center+28,self.z_pos_center + 30, -self.theta) # x_block, z_block, self.theta)
            self.held_block.set_pose(final_x_block/100,final_z_block/100,math.degrees(self.theta))
            self.held_block.paint(qp)
        
        t = QTransform()
        t.translate( self.x_pos_center, self.z_pos_center  )
        t.rotate(-math.degrees(self.theta))
        t.translate(-(self.x_pos_center), - (self.z_pos_center ))

        qp.setTransform(t)
        qp.drawPixmap(x_pos,z_pos,self.dronePix)
        