#
#
#

import sys
import math
import random
import time

from phidias_interface import Messaging
from block import *
from world import *

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication,QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QTransform,QPen,QBrush
from PyQt5.QtCore import Qt, QTimer
from autopilot import *

COLOR_NAMES = ['red', 'green', 'blue']

class MainWindow(QMainWindow):

    def __init__(self):
        self.nodes, self.block_slot_nodes, self.tower_slot_nodes, _ = readNodesCoordsAndEdges("nodes.txt")
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('QuadRotor 2D Simulator')
        self.label = QLabel(self)
        self.label.resize(600, 40)

        self.show()

        self.delta_t = 1e-3 # 1ms of time-tick
        
        self.world = World(self)

        self.autopilot = Autopilot()
        self.autopilot.x_target = 5
        self.autopilot.z_target = 2

        self.timer = QTimer()
        self.timer.timeout.connect(self.go)
        self.timer.start(1000*self.delta_t)
        
    def go_to(self,target_x, target_z):
        self.notification = False
        self.autopilot.set_target(target_x, target_z)

    def go_to_node(self,Node):
        self.notification = False
        target_x, target_z = self.nodes[Node]
        self.autopilot.set_target(target_x, target_z)
    
    def go_to_tower(self,color):#TODO
        self.notification = False
        target_x, target_z = self.nodes[Node]
        self.autopilot.set_target(target_x, target_z)

    def notify_target_got(self):
        self.notification = True
        if self._from is not None:
            Messaging.send_belief(self._from, 'target_got', [], 'robot')

            
    def generate_blocks(self, num_blocks):
        if num_blocks > 6:
            return
        if self.world.count_blocks() == 10:
            return
        generated_blocks = 0
        free_slots = []
        for slot in self.world.block_slot_busy:
            if not self.world.block_slot_busy[slot]:
                free_slots.append(slot)
        while self.world.count_blocks() < 10 and generated_blocks < num_blocks:
            generated_blocks = generated_blocks + 1
            node_slot = random.choice(free_slots)
            random_color = random.choice(COLOR_NAMES)
            self.world.new_block(random_color, node_slot)
            free_slots.remove(node_slot)

        #while True:
        #    col = int(random.uniform(0, 2))
        #    if not(self.world.floor_position_busy(x, z)):
        #        self.world.new_block(COLOR_NAMES[col], x)
        #        return

    def go(self):
        self.autopilot.run(self.delta_t) # autopilot + multirotor dynamics
        self.update() # repaint window

    def mouseMoveEvent(self, event):
        self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(255,255,255))
        qp.setBrush(QColor(255,255,255))
        qp.drawRect(event.rect())

        self.world.paint(qp, self.width(), self.height())

        qp.setPen(QColor(0,0,0))
        qp.drawText(self.width() - 150, 20, "X = %6.3f m" % (self.autopilot.quadrotor.xPosition))
        qp.drawText(self.width() - 150, 40, "Vx = %6.3f m/s" % (self.autopilot.quadrotor.xVelocity))
        qp.drawText(self.width() - 150, 60, "Z = %6.3f m" % (self.autopilot.quadrotor.zPosition))
        qp.drawText(self.width() - 150, 80, "Vz = %6.3f m/s" % (self.autopilot.quadrotor.zVelocity))
        qp.drawText(self.width() - 150,100, "Th = %6.3f deg" % (math.degrees(self.autopilot.quadrotor.theta)))
        qp.drawText(self.width() - 150,120, "Omega = %6.3f deg" % (math.degrees(self.autopilot.quadrotor.omega)))

        self.autopilot.quadrotor.paint(qp,self.height(),self.width())
        
        



        qp.end()



def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.generate_blocks(5)
    ex.generate_blocks(5)
    ex.autopilot.quadrotor.set_held_block(ex.world.get_block("genG"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()