
import serial
import os
import time
from PIL import Image

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

def display():
    app = QtWidgets.QApplication(sys.argv)
    FrontWindow = QtWidgets.QMainWindow()
    FrontWindow.setObjectName("SJEC")
    FrontWindow.resize(800, 480)
    centralwidget = QtWidgets.QWidget(FrontWindow)
    centralwidget.setObjectName("main-widget")
    FrontWindow.setCentralWidget(centralwidget)
    label = QtWidgets.QLabel(centralwidget)
    label.setGeometry(QtCore.QRect(0, 0, 800, 480))
    label.setMinimumSize(QtCore.QSize(800, 480))
    label.setMaximumSize(QtCore.QSize(800, 480))
    label.setObjectName("lb1")
    movie = QMovie("sjec.jpeg")
    label.setMovie(movie)
    timer = QtCore.QTimer()
    timer.timeout.connect(movie.start)
    timer.start(50) # 50 ms
    FrontWindow.show()
    sys.exit(app.exec_())
    
display()
