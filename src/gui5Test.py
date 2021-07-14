#
#
#

import sys
import math


from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication,QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QTransform,QPen,QBrush
from PyQt5.QtCore import Qt, QTimer
from autopilot import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('QuadRotor 2D Simulator with controls for arrow keys')
        self.drone = QPixmap("drone.png")  #drone image
        self.gordo = QPixmap("gordo.png")  #obstacle image
        self.start = QPixmap("start.png")  #start image
        self.label = QLabel(self)
        self.label.resize(600, 40)

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
    #TODO gestione tasti direzionali
    def keyPressEvent(self, event):
  
        # if up arrow key is pressed
        if event.key() == Qt.Key_Up:
  
            # if top position is attained
            if y > 0:
                self.label.move(x, y - self.speed)
  
        # if down arrow key is pressed
        elif event.key() == Qt.Key_Down:
  
            # if bottom position is attained
            # for bottom point, bottom co-ordinate will be
            # height of window - height of label
            if y < self.w_height - self.l_height:
                self.label.move(x, y + self.speed)
  
        # if left arrow key is pressed
        elif event.key() == Qt.Key_Left:
  
            # if left end position is attained
            if x > 0:
                self.label.move(x - self.speed, y)
  
        # if down arrow key is pressed
        elif event.key() == Qt.Key_Right:
  
            # if right end position is attained
            # for right end point, right co-ordinate will be
            # width of window - width of label
            if x < self.w_width - self.l_width:
                self.label.move(x + self.speed, y)

        



    def paintObstacles(self,painter,obstacle):
        painter.drawPixmap(100,400,80,80,obstacle)        
        painter.drawPixmap(800,350,80,80,obstacle)
        painter.drawPixmap(902,71,80,80,obstacle)
        painter.drawPixmap(575,220,80,80,obstacle)        
        painter.drawPixmap(800,600,80,80,obstacle)
        painter.drawPixmap(300,400,80,80,obstacle)


    def mouseMoveEvent(self, event):
        self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(255,255,255))
        qp.setBrush(QColor(255,255,255))
        qp.drawRect(event.rect())


        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.red, Qt.SolidPattern)))
        qp.drawRect(0,200,300,30)

        qp.drawRect(self.width()-300,300,300,30)    #mensola 2

        qp.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.red, Qt.SolidPattern)))    #base torre rossa
        qp.drawRect(980, self.height() - 15,60,10)

        qp.setPen(QPen(Qt.green, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.green, Qt.SolidPattern)))    #base torre verde
        qp.drawRect(1080, self.height() - 15,60,10)

        qp.setPen(QPen(Qt.blue, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.blue, Qt.SolidPattern)))    #base torre blu
        qp.drawRect(1180, self.height() - 15,60,10)

        qp.setPen(QPen(Qt.gray, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.gray, Qt.SolidPattern)))   #pavimento
        qp.drawRect(0,self.height()-10,self.width(),10)

        

        qp.setPen(QColor(0,0,0))
        qp.drawText(self.width() - 150, 20, "X = %6.3f m" % (self.autopilot.quadrotor.xPosition))
        qp.drawText(self.width() - 150, 40, "Vx = %6.3f m/s" % (self.autopilot.quadrotor.xVelocity))
        qp.drawText(self.width() - 150, 60, "Z = %6.3f m" % (self.autopilot.quadrotor.zPosition))
        qp.drawText(self.width() - 150, 80, "Vz = %6.3f m/s" % (self.autopilot.quadrotor.zVelocity))
        qp.drawText(self.width() - 150,100, "Th = %6.3f deg" % (math.degrees(self.autopilot.quadrotor.theta)))
        qp.drawText(self.width() - 150,120, "Omega = %6.3f deg" % (math.degrees(self.autopilot.quadrotor.omega)))
        
        x_pos = self.width()/2 - self.drone.width()/2 + (self.autopilot.quadrotor.xPosition * 100)
        y_pos = self.height()-(self.drone.height())-10 - (self.autopilot.quadrotor.zPosition * 100)
        
        qp.drawPixmap(self.width()/2-self.start.width()/20,self.height() - self.start.height()/8,self.start.width() /10,self.start.height()/10,self.start)  
        
        self.paintObstacles(qp,self.gordo)

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