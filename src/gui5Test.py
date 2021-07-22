#
#
#

import sys
import math
import random
import time

from phidias_interface import *
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

        self.notification = False

        self.delta_t = 1e-2 # 10ms of time-tick

        self.autopilot = Autopilot()

        #self.autopilot.x_target = -5
        #self.autopilot.z_target = 2

        self.world = World(self)


        self.timer = QTimer()
        self.timer.timeout.connect(self.go)
        self.timer.start(1000*self.delta_t)

        self._from = None

    def set_from(self, _from):
        self._from = _from
        
    def go_to(self,target_x, target_z):
        self.notification = False
        self.autopilot.set_target(target_x, target_z)

    def go_to_node(self,Node):
        self.notification = False
        target_x, target_z = self.nodes[Node]
        target_x, target_z = pixel_to_meter(target_x,target_z,self.width(),self.height(), self.autopilot.quadrotor.dronePix.height()-10)
        print("going to " + Node)
        self.autopilot.set_target(target_x,target_z)
    
    def go_to_tower(self,color):#TODO
        self.notification = False
        target_x, target_z = self.nodes[Node]
        self.autopilot.set_target(target_x, target_z)

    def notify_target_got(self):
        self.notification = True
        if self._from is not None:
            print("sending to strategy target got")
            Messaging.send_belief(self._from, 'target_got', [], 'robot')

    def go_lower(self,initial_x, initial_pos_z, shift):
        self.autopilot.set_target(initial_x, initial_pos_z + shift)
        if(distanceCouple(self.autopilot.quadrotor.get_pose_xz(),(self.autopilot.x_target,self.autopilot.z_target)) <0.1 ): 
            return False
        else : 
            return True

    
    def go_up(self,initial_x, initial_pos_z):
        self.autopilot.set_target(initial_x, initial_pos_z)
        if(distanceCouple(self.autopilot.quadrotor.get_pose_xz(),(self.autopilot.x_target,self.autopilot.z_target)) <0.1 ): 
            return False
        else : 
            return True

    def set_held_block(self, Node):
        #self.autopilot.take_block(Node)
        (initial_x,initial_z) = self.autopilot.quadrotor.get_pose_xz()
        x_block,_ = self.world.get_block(Node).get_pose()
        while (self.go_lower(x_block,initial_z,-0.50)): pass
        self.autopilot.quadrotor.set_held_block(self.world.pop_block(Node))
        while (self.go_up(x_block, initial_z)): pass

    def release_block_to_tower(self):
        released_block = self.autopilot.quadrotor.free_block()
        self.world.add_block_to_tower(released_block)
            
    def generate_blocks(self, num_blocks):
        print("generation blocks")
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

    def sense_distance(self):
        if self._from is not None:
            d = self.world.sense_distance()
            if d is None:
                params = []
            else:
                params = [d]
            print("sending distance " + str(d) + " to robot")
            Messaging.send_belief(self._from, 'distance', params, 'robot')

    def sense_color(self):
        if self._from is not None:
            d = self.world.sense_color()
            if d is None:
                params = []
            else:
                params = [d]
            print("sending color " + str(d) + " to robot")
            Messaging.send_belief(self._from, 'color', params, 'robot')
    
    def resetTowers(self):
        self.world.release_towers()

    def go(self):
        self.autopilot.run(self.delta_t) # autopilot + multirotor dynamics
        self.update() # repaint window

        if self.autopilot.target_got and not(self.notification):
            self.notify_target_got()

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
    ex.generate_blocks(1)
    start_message_server_http(ex)

    #ex.generate_blocks(5)
    #ex.autopilot.quadrotor.set_held_block(ex.world.get_block("genG"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()