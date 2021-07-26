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

from threading import Lock

COLOR_NAMES = ['red', 'green', 'blue']

class MainWindow(QMainWindow):

    def __init__(self, _mutex):
        self.nodes, self.block_slot_nodes, self.tower_slot_nodes, _ = readNodesCoordsAndEdges("nodes.txt")
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.mutex = _mutex

    def initUI(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('QuadRotor 2D Simulator')
        self.label = QLabel(self)
        self.label.resize(600, 40)

        self.show()

        self.notification = False

        self.delta_t = 1e-3 # 1ms of time-tick

        self.autopilot = Autopilot()

        self.world = World(self)


        self.timer = QTimer()
        self.timer.timeout.connect(self.go)
        self.timer.start(1000*self.delta_t)

        self._from = None

    def set_from(self, _from):
        self._from = _from
    
    # Go to target coordinates after receving the instruction from strategy
    def go_to(self,target_x, target_z):
        self.notification = False
        self.autopilot.set_target(target_x, target_z)

    # Go to target node after receving the instruction from strategy
    def go_to_node(self,Node):
        self.notification = False
        target_x, target_z = self.nodes[Node]
        target_x, target_z = pixel_to_meter(target_x,target_z,self.width(),self.height(), self.autopilot.quadrotor.dronePix.height()-10)
        #self.mutex.acquire()
        self.autopilot.set_target(target_x,target_z)
        #self.mutex.release()
        print("[WORLD] :" + " drone going to " + Node)
        #print("gui target x e y " , target_x , " " ,target_z)
    

    # Informing strategy of having reached the target node
    def notify_target_got(self):
        self.notification = True
        if self._from is not None:
            print("[WORLD COMMUNICATION] :" + " sending to ROBOT target got")
            Messaging.send_belief(self._from, 'target_got', [], 'robot')

    def wait_for_target(self):
        while not distanceCouple(self.autopilot.quadrotor.get_pose_xz(),(self.autopilot.x_target,self.autopilot.z_target)) <0.1: pass

    # Give block to quadrotor after receiving the message from strategy
    def set_held_block(self, Node):
        (initial_x,initial_z) = self.autopilot.quadrotor.get_pose_xz()
        x_block,_ = self.world.get_block(Node).get_pose()
        # Go lower animation when picking blocks
        self.autopilot.set_target(x_block, initial_z - 0.5)
        self.wait_for_target()
        self.autopilot.quadrotor.set_held_block(self.world.pop_block(Node))
        # Go up animation when picking blocks
        self.autopilot.set_target(x_block, initial_z)
        self.wait_for_target()

    # Remove block from quadrotor and add it to tower after receiving the message from strategy
    def release_block_to_tower(self):
        (initial_x,initial_z) = self.autopilot.quadrotor.get_pose_xz()
        x_block,_ = self.autopilot.quadrotor.held_block.get_pose()
        tower_height_z = self.world.getTowerHeight(self.autopilot.quadrotor.held_block.get_color())
        shift = initial_z - tower_height_z
        self.autopilot.set_target(x_block, initial_z - shift)
        self.wait_for_target()
        released_block = self.autopilot.quadrotor.free_block()
        self.world.add_block_to_tower(released_block)
        self.autopilot.set_target(x_block, initial_z)
        self.wait_for_target()

    # Generate blocks and put them in world after receiving the message from strategy        
    def generate_blocks(self, num_blocks):
        print("[WORLD] " + "generating blocks")
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

    # Compute and send distance from closest block to strategy
    def sense_distance(self):
        if self._from is not None:
            d = self.world.sense_distance()
            if d is None:
                params = []
            else:
                params = [d]
            print("[WORLD COMMUNICATION] :"+" sending distance " + str(d) + " to ROBOT")
            Messaging.send_belief(self._from, 'distance', params, 'robot')

    # Compute and send color from closest block to strategy
    def sense_color(self):
        if self._from is not None:
            d = self.world.sense_color()
            if d is None:
                params = []
            else:
                params = [d]
            print("[WORLD COMMUNICATION] :"+" sending color " + str(d) + " to robot")
            Messaging.send_belief(self._from, 'color', params, 'robot')
    
    def resetTowers(self):
        self.world.release_towers()

    def change_control_type(self,control_type):
        self.autopilot.change_control_type(control_type)

    def go(self):
        self.mutex.acquire()
        self.autopilot.run(self.delta_t) # autopilot + multirotor dynamics
        self.update() # repaint window
        self.mutex.release()

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
    mutex = Lock()
    app = QApplication(sys.argv)
    ex = MainWindow(mutex)
    start_message_server_http(ex, mutex)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()