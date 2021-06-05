#
#
#

import sys
import math


from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QTransform
from PyQt5.QtCore import Qt, QTimer
from autopilot import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('QuadRotor 2D Simulator')
        self.drone = QPixmap("drone.png")
        self.show()

        self.delta_t = 1e-3 # 1ms of time-tick
        
        self.autopilot = Autopilot()
        self.autopilot.x_target = -2
        self.autopilot.z_target = 3

        self.timer = QTimer()
        self.timer.timeout.connect(self.go)
        self.timer.start(1000*self.delta_t)
        



    def go(self):
        self.autopilot.run(self.delta_t) # autopilot + multirotor dynamics
        self.update() # repaint window


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(255,255,255))
        qp.setBrush(QColor(255,255,255))
        qp.drawRect(event.rect())

        x_pos = 336 + (self.autopilot.quadrotor.xPosition * 100)
        y_pos = 500 - (self.autopilot.quadrotor.zPosition * 100)

        t = QTransform()
        s = self.drone.size()
        t.translate(x_pos + s.height()/2, y_pos + s.width()/2)
        t.rotate(-math.degrees(self.autopilot.quadrotor.theta))
        t.translate(-(x_pos + s.height()/2), - (y_pos + s.width()/2))

        qp.setTransform(t)
        qp.drawPixmap(x_pos,y_pos,self.drone)
        qp.end()



def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()