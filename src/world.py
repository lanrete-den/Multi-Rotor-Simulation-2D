import math

from block import *
from utilities import *

from PyQt5.QtGui import QColor, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt

class World:

    FLOOR_LEVEL = -0.05
    eps_dist = 1

    def paintObstacles(self,painter,obstacle):
        painter.drawPixmap(100,400,80,80,obstacle)        
        painter.drawPixmap(800,350,80,80,obstacle)
        painter.drawPixmap(902,71,80,80,obstacle)
        painter.drawPixmap(575,220,80,80,obstacle)        
        painter.drawPixmap(800,600,80,80,obstacle)
        painter.drawPixmap(300,400,80,80,obstacle)

    def __init__(self, ui):
        self.__blocks = []
        self.block_slot_busy = dict()
        _, self.block_slot_nodes, self.tower_slot_nodes, _ = readNodesCoordsAndEdges("nodes.txt")
        for slot in self.block_slot_nodes:
            self.block_slot_busy[slot] = False
        self.ui = ui
        self.gordo = QPixmap("gordo.png")  #obstacle image
        self.start = QPixmap("start.png")  #start image

    def new_block(self, uColor, node_slot):
        b = Block(uColor)
        uX, uZ = self.block_slot_nodes[node_slot]
        b.set_pose(uX, uZ, 0)
        self.block_slot_busy[node_slot] = True
        self.__blocks.append(b)

    def count_blocks(self):
        return len(self.__blocks)

    def sense_distance(self):
        robot_pose = self.quadrotor.get_pose_xz()
        L = self.ui.arm.element_3_model.L
        d = y - L - World.FLOOR_LEVEL
        min_dist = 9999999
        for b in self.__blocks:
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, robot_pose)
            if dist < min_dist:
                min_dist = dist
        if min_dist < self.eps_dist:
            return min_dist
        else:
            return None

    def sense_color(self):
        robot_pose = self.quadrotor.get_pose_xz()
        L = self.ui.arm.element_3_model.L
        d = y - L - World.FLOOR_LEVEL
        min_dist = 9999999
        eps_dist = 1
        for b in self.__blocks:
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, robot_pose)
            if dist < min_dist:
                min_dist = dist
                min_block = b
        if min_dist < eps_dist:
            return min_block.get_color()
        else:
            return None

    def paint(self, qp, window_width, window_height):
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.red, Qt.SolidPattern)))
        qp.drawRect(0,200,300,30)

        qp.drawRect(window_width - 300,300,300,30)    #mensola 2

        qp.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.red, Qt.SolidPattern)))    #base torre rossa
        qp.drawRect(980, window_height - 15,60,10)

        qp.setPen(QPen(Qt.green, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.green, Qt.SolidPattern)))    #base torre verde
        qp.drawRect(1080, window_height - 15,60,10)

        qp.setPen(QPen(Qt.blue, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.blue, Qt.SolidPattern)))    #base torre blu
        qp.drawRect(1180, window_height - 15,60,10)

        qp.setPen(QPen(Qt.gray, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.gray, Qt.SolidPattern)))   #pavimento
        qp.drawRect(0,window_height-10,window_width,10)
        for b in self.__blocks:
            b.paint(qp)
        self.paintObstacles(qp,self.gordo)
        qp.drawPixmap(window_width/2-self.start.width()/20,window_height - self.start.height()/8,self.start.width()/10,self.start.height()/10,self.start)  


