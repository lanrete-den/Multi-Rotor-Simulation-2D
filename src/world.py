import math

from block import *
from tower import *
from utilities import *

from PyQt5.QtGui import QColor, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt

class World:

    

    def paintObstacles(self,painter,obstacle):
        painter.drawPixmap(100,400,80,80,obstacle)        
        painter.drawPixmap(800,350,80,80,obstacle)
        painter.drawPixmap(902,71,80,80,obstacle)
        painter.drawPixmap(575,220,80,80,obstacle)        
        painter.drawPixmap(800,600,80,80,obstacle)
        painter.drawPixmap(300,400,80,80,obstacle)

    def __init__(self, ui):
        self.__blocks = dict()
        self.block_slot_busy = dict()
        _, self.block_slot_nodes, self.tower_slot_nodes, _ = readNodesCoordsAndEdges("nodes.txt")
        for slot in self.block_slot_nodes:
            self.block_slot_busy[slot] = False
        self.ui = ui
        self.gordo = QPixmap("gordo.png")  #obstacle image
        self.start = QPixmap("start.png")  #start image
        self.eps_dist = 0.3
        self.towers = []
        for tower_node in self.tower_slot_nodes:
            tower_color = tower_node.split('_')[-1]
            self.towers.append(Tower(ui, tower_node, self.tower_slot_nodes[tower_node], tower_color))

    def new_block(self, uColor, node_slot):
        b = Block(uColor)
        uX, uZ = self.block_slot_nodes[node_slot]
        b.set_pose(uX, uZ, 0)
        self.block_slot_busy[node_slot] = True
        self.__blocks[node_slot] = b
    
    def get_block(self,node_name):
        self.block_slot_busy[node_name] = False
        out_block = self.__blocks.pop(node_name)
        return out_block

    def count_blocks(self):
        return len(self.__blocks)

    def sense_distance(self):
        robot_pose = self.ui.quadrotor.get_pose_xz()
        min_dist = 9999999
        for b in self.__blocks.values():
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, robot_pose)
            if dist < min_dist:
                min_dist = dist
        if min_dist < self.eps_dist:
            return min_dist
        else:
            return None

    def sense_color(self):
        robot_pose = self.ui.quadrotor.get_pose_xz()
        min_dist = 9999999
        eps_dist = 1
        for b in self.__blocks.values():
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, robot_pose)
            if dist < min_dist:
                min_dist = dist
                min_block = b
        if min_dist < eps_dist:
            return min_block.get_color()
        else:
            return None

    def add_block_to_tower(self, block):
        b_color = block.get_color()
        self.__blocks.remove(block)
        for tower in self.towers:
            if b_color == tower.get_color():
                tower.add_block_to_tower(block)
                break

    def paint(self, qp, window_width, window_height):
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.red, Qt.SolidPattern)))
        qp.drawRect(0,200,300,30)

        qp.drawRect(window_width - 300,300,300,30)    #mensola 2

        for tower in self.towers:
            tower.paint(qp, window_width, window_height)

        qp.setPen(QPen(Qt.gray, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.gray, Qt.SolidPattern)))   #pavimento
        qp.drawRect(0,window_height-10,window_width,10)
        for b in self.__blocks.values():
            b.paint(qp)
        self.paintObstacles(qp, self.gordo)
        qp.drawPixmap(window_width/2-self.start.width()/20,window_height - self.start.height()/8,self.start.width()/10,self.start.height()/10,self.start)  


