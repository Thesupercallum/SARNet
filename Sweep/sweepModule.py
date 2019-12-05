"""
SARNet
Author:      Cameron Stauffer
Last Edited: November 22, 2019

PyQT Sweep Module
"""

import sys
import time
from compassbeta1 import getHeading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# global variables
            
class Worker(QThread):
    updateAngle = pyqtSignal(float)
    
    def __init__(self):
        QThread.__init__(self)


    def run(self):
        
        while True:
            """
            heading = getHeading()
            heading
            """
            heading_file = open('/mnt/rd/testdoc', 'r')          
            heading = heading_file.read()
            heading_file.close()
                
            if not heading:
                pass
            else:
                heading = int(heading)
                print('Heading Read: ',heading)
                self.updateAngle.emit(heading)
                print("Compass Reading: "+str(heading))
            time.sleep(0.25)

class CompassWidget(QWidget):

    angleChanged = pyqtSignal(float)
    
    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
                            225: "SW", 270: "W", 315: "NW"}
        
        self._worker = Worker()
        self._worker.updateAngle.connect(self.setAngle)
        self._worker.start()
     
    def paintEvent(self, event):
     
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
        self.drawMarkings(painter)
        
        #sweepFlag_file = open('/mnt/GUI/sweepFlag', 'w+')
        sweepFlag_file = open('/home/pi/Documents/SARNet/GUI/sweepFlag', 'r')
        sweepFlag = sweepFlag_file.readline()
        print('Sweep Flag1: ',sweepFlag)
        
        if sweepFlag == '0':
            print('Entered sweepFlag argument 0')
            self.drawNeedle(painter)
            self.drawSweepRings(painter)
            print('Needle drawn')
            
        if sweepFlag == '1':
            print('Entered sweepFlag argument 1')
            self.drawSweepRings(painter)
            self.plotReadings(painter)
        
        print('Sweep Flag: ',sweepFlag)
         
        painter.end()
   
    def drawMarkings(self, painter):
     
        darkThemeFlag_file = open('/home/pi/Documents/SARNet/GUI/darkThemeFlag')
        darkThemeFlag = darkThemeFlag_file.readline()
        
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
             
        font = QFont(self.font())
        font.setPixelSize(10)
        metrics = QFontMetricsF(font)
             
        painter.setFont(font)
        painter.setPen(self.palette().color(QPalette.Shadow))
             
        i = 0
        while i < 360:
             
            if i % 45 == 0:
                painter.drawLine(0, 0, 0, -50)
                painter.drawText(-metrics.width(self._pointText[i])/2.0, -52,
                                    self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)
                 
            painter.rotate(15)
            i += 15           
         
        painter.restore()
     
    def drawNeedle(self, painter):
     
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
        
        painter.setPen(QColor(0,0,1))
        painter.setBrush(self.palette().brush(QPalette.Shadow))
        
        #RSSI_file = open('/mnt/GUI/activeDevID', 'w+')
        RSSI_file = open('/home/pi/Documents/SARNet/GUI/activeDevID', 'r')
        self.RSSIactive = RSSI_file.readline()
        RSSI_file.close()
        
        #curRSSI_file = open('/mnt/GUI/RSSIuser_'+self.RSSIactive+'.txt', 'w+')
        curRSSI_file = open('/home/pi/Documents/SARNet/GUI/RSSIuser_'+self.RSSIactive+'.txt', 'r')
        curRSSI = curRSSI_file.readline()  
        
        amplitude = (((int(curRSSI) + 50)/2)+40)*-1
        
        """
        painter.drawPolygon(
            QPolygon([QPoint(-10, 0), QPoint(0, -45), QPoint(10, 0),
                      QPoint(0, 45), QPoint(-10, 0)])
            )
        """
        painter.drawLine(0, 0, 0, amplitude)
        
        painter.setBrush(self.palette().brush(QPalette.Highlight))
        
        painter.drawPolygon(
            QPolygon([QPoint(-2, amplitude), QPoint(0, amplitude-5), QPoint(2, amplitude)])
                      #QPoint(0, -30)]) #QPoint(-5, -25)])
            )
        
        print('RSSI Reading: ',curRSSI)
        print('Amplitude: ',amplitude)
        print('************************************************')
         
        painter.restore()
        
    def plotReadings(self, painter):
     
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
        
        painter.setPen(QColor(0,0,1))
        painter.drawEllipse(0, 0, 10, 10)
        #painter.setBrush(self.palette().brush(QPalette.Shadow))
        
        #RSSI_file = open('/mnt/GUI/activeDevID', 'w+')
        RSSI_file = open('/home/pi/Documents/SARNet/GUI/activeDevID', 'r')
        self.RSSIactive = RSSI_file.readline()
        RSSI_file.close()
        
        #curRSSI_file = open('/mnt/GUI/RSSIuser_'+self.RSSIactive+'.txt', 'w+')
        curRSSI_file = open('/home/pi/Documents/SARNet/GUI/RSSIuser_'+self.RSSIactive+'.txt', 'r')
        curRSSI = curRSSI_file.readline()  
        
        amplitude = ((int(curRSSI) + 50)/2)
        """
        painter.drawPolygon(
            QPolygon([QPoint(-10, 0), QPoint(0, -45), QPoint(10, 0),
                      QPoint(0, 45), QPoint(-10, 0)])
            )
        """
        #painter.drawLine(0, 0, 0, amplitude)
        
        painter.setBrush(self.palette().brush(QPalette.Highlight))
        """
        painter.drawPolygon(
            QPolygon([QPoint(-2, amplitude), QPoint(0, amplitude-5), QPoint(2, amplitude)])
                      #QPoint(0, -30)]) #QPoint(-5, -25)])
            )
        """
        print('RSSI Reading: ',curRSSI)
        print('Amplitude: ',amplitude)
        print('************************************************')
         
        painter.restore()
        
    def drawSweepRings(self, painter):
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
        
        ### this draws the circles that make the sweep rings ###
        radx1 = 40;radx2 = 25;radx3 = 10; radx4 = 2
        rady1 = 40;rady2 = 25;rady3 = 10; rady4 = 2
        
        center = QPoint(0, 0)
        painter.drawEllipse(center, radx1, rady1)
        
        center = QPoint(0, 0)
        painter.drawEllipse(center, radx2, rady2)
        
        center = QPoint(0, 0)
        painter.drawEllipse(center, radx3, rady3)
        
        center = QPoint(0, 0)
        painter.drawEllipse(center, radx4, rady4)
        painter.end()
            
    def sizeHint(self):
     
        return QSize(150, 150)
     
    def angle(self):
        return self._angle
    
    @pyqtSlot(float)
    def setAngle(self, angle):
   
       if angle != self._angle:
            self._angle = angle
            self.angleChanged.emit(angle)
            self.update()

    angle = pyqtProperty(float, angle, setAngle)     
 
if __name__ == "__main__":
        
    app = QApplication(sys.argv)  
    window = QWidget()
    compass = CompassWidget()
    spinBox = QSpinBox()
    spinBox.setRange(0, 359)

    #spinBox.valueChanged.connect(compass.setAngle)
    
    layout = QVBoxLayout()
    layout.addWidget(compass)
    #layout.addWidget(spinBox)
    window.setLayout(layout)
    
    window.setGeometry(506, 263, 300, 215)
    window.wm_attributes('-type','splash')
    
    window.show()
    sys.exit(app.exec_())