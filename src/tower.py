import math

from block import *
from pose import Pose

from PyQt5.QtGui import QColor, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt

class Tower:

    def __init__(self, ui, _tower_node, _tower_pos, _tower_color):
        self.blocks = list()
        self.tower_node = _tower_node
        self.tower_pos = Pose(ui)
        self.tower_pos.set_pose(_tower_pos[0],_tower_pos[1] - 1.9,0)
        self.tower_color = _tower_color
        if self.tower_color == 'red':
            self.qt_color = Qt.red
        elif self.tower_color == 'blue':
            self.qt_color = Qt.blue
        elif self.tower_color == 'green':
            self.qt_color = Qt.green
        self.ui = ui
    
    def get_color(self):
        return self.tower_color

    def add_block_to_tower(self, block):
        if len(self.blocks) >= 3:
            print("Maximum tower size reached")
            return
        tower_x, tower_z = self.tower_pos.get_pose()
        block.set_pose(tower_x, tower_z + (self.get_tower_length() + 1) * Block.HEIGHT - Block.HEIGHT/2, 0)
        self.blocks.append(block)

    def get_tower_length(self):
        return len(self.blocks)

    def get_tower_color(self):
        return self.tower_color

    def release_tower(self):
        self.blocks.clear()

    def paint(self, qp, window_width, window_height):
        
        # Draw tower base
        qp.setPen(QPen(self.qt_color, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(self.qt_color, Qt.SolidPattern)))

        tower_pixel_x, tower_pixel_z = self.tower_pos.to_pixel()

        qp.drawRect(tower_pixel_x - 30,tower_pixel_z,60,10)

        # Draw tower blocks
        for b in self.blocks:
            b.paint(qp)
