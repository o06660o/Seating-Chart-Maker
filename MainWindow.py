# -*- coding: utf-8 -*-

import random, time

from PySide6.QtCore import QTimer, QRect, QMetaObject, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QMainWindow, QLabel, QWidget, QMenuBar,
    QStatusBar, QGridLayout, QHBoxLayout, QPushButton)

from util import read_settings
from SettingsDialog import SettingsDialog
from DrawingDialog import DrawingDialog

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = read_settings()
        
        self.arrangements = [i for i in range(50)]
        # self.names = [f"00{i + 1:02d}" for i in range(50)]
        self.names: list[str] = self.settings["names"]
        
        # init the main window
        self.labels: list[QLabel] = []
        self.setupUI(self)

        self.interval = self.settings["timer_interval"]
        # init the timer to update students' names
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_names)
        self.timer.start(self.interval)       


    def setupUI(self, MainWindow: QMainWindow) -> None:
        MainWindow.setWindowTitle(self.settings["mainwindow"]["title"])
        MainWindow.setObjectName("MainWindow")
        MainWindow_size = self.settings["mainwindow"]["size"]
        MainWindow.resize(MainWindow_size[0], MainWindow_size[1])
        MainWindow.setWindowIcon(QPixmap("./assets/icons/MainWindow.jpg"))
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QMetaObject.connectSlotsByName(MainWindow)        

        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QRect(50, 130, 700, 300))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        cnt = 0
        for col in (0, 1, 3, 4, 6, 7, 9, 10, 2, 5, 8):
            for row in range(6):
                label = QLabel(self.gridLayoutWidget)
                label.setText(f"   ")
                label.setObjectName(f"Seat {cnt}")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                if col in (0, 1, 3, 4, 6, 7, 9, 10):
                    label.setStyleSheet("background-color: lightgreen;")
                self.gridLayout.addWidget(label, row, col, 1, 1)   
                self.labels.append(label)
                cnt += 1

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(
            QRect(340, 440, 120, 45))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label1 = QLabel(self.horizontalLayoutWidget)
        self.label1.setObjectName("label1")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setStyleSheet("background-color: lightgreen;")
        self.horizontalLayout.addWidget(self.label1)
        self.label2 = QLabel(self.horizontalLayoutWidget)
        self.label2.setObjectName("label_2")
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setStyleSheet("background-color: lightgreen;")
        self.horizontalLayout.addWidget(self.label2)
        exception = self.settings["exception"]
        self.label1.setText(self.names[exception[0] - 1])
        self.label2.setText(self.names[exception[1] - 1])

        self.button_continue_ = QPushButton(self.centralwidget)
        self.button_continue_.setGeometry(QRect(620, 520, 100, 30))
        self.button_continue_.setObjectName("ButtonContinue")
        self.button_continue_.setText("Continue")
        self.button_continue_.clicked.connect(self.continue_)
        self.button_continue_.setEnabled(False)
        self.button_pause = QPushButton(self.centralwidget)
        self.button_pause.setGeometry(QRect(500, 520, 100, 30))
        self.button_pause.setObjectName("ButtonPause")
        self.button_pause.setText("Pause")
        self.button_pause.clicked.connect(self.pause)

        self.label_lectern = QLabel(self.centralwidget)
        self.label_lectern.setGeometry(QRect(325, 20, 150, 80))
        self.label_lectern.setObjectName("LabelLectern")
        self.label_lectern.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_lectern.setText(
            "<span style='font-size:36pt; color:red;'>讲 台</span>")

        self.button_settings = QPushButton(self.centralwidget)
        self.button_settings.setGeometry(QRect(50, 520, 100, 30))
        self.button_settings.setObjectName("ButtonSettings")
        self.button_settings.setText("Settings")
        self.button_settings.clicked.connect(self.open_settings_dialog)

        self.button_draw = QPushButton(self.centralwidget)
        self.button_draw.setGeometry(QRect(170, 520, 100, 30))
        self.button_draw.setObjectName("ButtonDraw")
        self.button_draw.setText("抽取幸运学生")
        self.button_draw.clicked.connect(self.open_drawing_dialog)

        self.label_creator = QLabel(self.centralwidget)
        self.label_creator.setGeometry(QRect(670, 560, 120, 30))
        self.label_creator.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label_creator.setText(
            "<span style='font-size:8pt; color:gray;'>\
            Created by o06660o\
            </span>"
        )


    def update_names(self) -> None:
        """Change the name in each label in the grid layout"""
        
        random.seed(time.time())
        random.shuffle(self.arrangements)
        cur = 0
        for number in range(len(self.arrangements)):
            if (number + 1) in self.settings["exception"]:
                continue
            label = self.labels[cur]
            cur += 1
            label.setText(self.names[self.arrangements[number]])
        
        
    def pause(self) -> None:
        self.button_pause.setEnabled(False)
        self.button_continue_.setEnabled(True)
        self.timer.stop()
    
    
    def continue_(self) -> None:
        self.button_pause.setEnabled(True)
        self.button_continue_.setEnabled(False)
        self.timer.start(self.interval)


    def open_settings_dialog(self) -> None:
        """Open the settings dialog"""
        settingsdialog = SettingsDialog()
        settingsdialog.exec()


    def open_drawing_dialog(self) -> None:
        """Open the drawing dialog"""
        drawingdialog = DrawingDialog()
        drawingdialog.exec()
