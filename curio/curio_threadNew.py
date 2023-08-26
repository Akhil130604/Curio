import serial
import os
import sys
import time
import pyttsx3
from PIL import Image

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

from threading import Thread


def speak():
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('rate',150)
    engine.say("Hi")
    engine.runAndWait()
    engine.say("I am curio")
    engine.runAndWait()
    engine.say("Welcome to Saint Joseph Engineering College")
    engine.runAndWait()
    engine.say("curio 3 point O is unnder daevelopmeent ")
    engine.runAndWait()
    engine.say("Stay Tuned")
    engine.runAndWait()

    
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
    movie = QMovie("sjec_gif.gif")
    label.setMovie(movie)
    timer = QtCore.QTimer()
    timer.timeout.connect(movie.start)
    timer.start(50) # 50 ms
    FrontWindow.show()
    sys.exit(app.exec_())
    
def obstacleDetection():
    ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    
    previousData=0
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(data)
            if data == "1":
                if previousData == 0:
                    previousData=1
                    print("Success")
                    speak_thread = Thread(target=speak)
                    speak_thread.start()
            else:
                previousData=0

if __name__ == '__main__':
    try:
        t1 = Thread(target=obstacleDetection)
        t2 = Thread(target=display)
        t1.start()
        t2.start()
    except:
        print("Error in thread")
