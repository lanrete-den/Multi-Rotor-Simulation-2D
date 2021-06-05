#
#
#

import sys
import math

from PyQt4 import QtGui, QtCore

from autopilot import *
from path_control import *


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('QuadRotor 2D Simulator')
        self.show()
        self.drone = QtGui.QPixmap("drone.png")

        self.delta_t = 1e-3 # 1ms of time-tick

        self._timer_painter = QtCore.QTimer(self)
        self._timer_painter.start(self.delta_t * 1000)
        self._timer_painter.timeout.connect(self.go)

        self.autopilot = Autopilot()
        self.path_control = PathControl(self.autopilot)
        self.path_control.add_new_point(0, 3)
        self.path_control.add_new_point(-2, 3)
        self.path_control.add_new_point(2, 3)
        #self.autopilot.x_target = -2
        #self.autopilot.z_target = 3



    def go(self):
        self.path_control.run(self.delta_t) # path control + autopilot + multirotor dynamics
        if self.path_control.path_completed:
            self.path_control.add_new_point(0, 4)
            self.path_control.add_new_point(0, 3)
            self.path_control.add_new_point(2, 3)
        self.update() # repaint window


    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(255,255,255))
        qp.setBrush(QtGui.QColor(255,255,255))
        qp.drawRect(event.rect())

        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(650, 20, "X = %6.3f m" % (self.autopilot.quadrotor.xPosition))
        qp.drawText(650, 40, "Vx = %6.3f m/s" % (self.autopilot.quadrotor.xVelocity))
        qp.drawText(650, 60, "Z = %6.3f m" % (self.autopilot.quadrotor.zPosition))
        qp.drawText(650, 80, "Vz = %6.3f m/s" % (self.autopilot.quadrotor.zVelocity))
        qp.drawText(650,100, "Th = %6.3f deg" % (math.degrees(self.autopilot.quadrotor.theta)))
        qp.drawText(650,120, "Omega = %6.3f deg" % (math.degrees(self.autopilot.quadrotor.omega)))

        x_pos = 336 + (self.autopilot.quadrotor.xPosition * 100)
        y_pos = 500 - (self.autopilot.quadrotor.zPosition * 100)

        t = QtGui.QTransform()
        s = self.drone.size()
        t.translate(x_pos + s.height()/2, y_pos + s.width()/2)
        t.rotate(-math.degrees(self.autopilot.quadrotor.theta))
        t.translate(-(x_pos + s.height()/2), - (y_pos + s.width()/2))

        qp.setTransform(t)
        qp.drawPixmap(x_pos,y_pos,self.drone)

        qp.end()



def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
