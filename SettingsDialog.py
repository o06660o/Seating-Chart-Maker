# -*- coding: utf-8 -*-

import json

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout)

from util import read_settings

class SettingsDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUI(self)
        
    def setupUI(self, MainWindow: QDialog) -> None:
        MainWindow.setWindowTitle("Settings")
        MainWindow.resize(400, 200)
        MainWindow.setWindowIcon(QPixmap("./assets/icons/SettingsDialog.png"))

        # Create widgets for the settings
        self.lbel_exception = QLabel(
            "输入坐在最后两个的同学学号(不输入表示不修改):\
            \n样例输入1,2\
            \n请用英文逗号分隔两个数据, 逗号前后不要加空格")
        self.edit_exception = QLineEdit()
        self.label_names = QLabel("输入同学的姓名(不输入表示不修改):")
        self.edit_names = QLineEdit()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.open_warning_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.lbel_exception)
        layout.addWidget(self.edit_exception)
        layout.addWidget(self.label_names)
        layout.addWidget(self.edit_names)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        
        
    def open_warning_dialog(self) -> None:
        warningdialog = self.WarningDialog(
            self.edit_exception.text(),
            self.edit_names.text()
        )
        warningdialog.exec()
        
    class WarningDialog(QDialog):
        def __init__(self, text1, text2) -> None:
            super().__init__()
            self.text1 = text1
            self.text2 = text2
            self.setupUI(self)
            
            
        def setupUI(self, MainWindow: QDialog) -> None:
            MainWindow.setWindowTitle("Warning")
            MainWindow.resize(400, 200)
            MainWindow.setWindowIcon(
                QPixmap("./assets/icons/WarningDialog.jpg"))
            
            self.warning = QLabel()
            self.warning.setText(
                "<span style='font-size:24pt; color:red;'>\
                在修改设置前请备份原文件\
                </span>"
            )
            self.save_button = QPushButton("Save")
            self.save_button.clicked.connect(self.save_settings)
            layout = QVBoxLayout()
            layout.addWidget(self.warning)
            layout.addWidget(self.save_button)
            self.setLayout(layout)
            
            
        def save_settings(self) -> None:
            """Save the settings to the settings file"""
            settings = read_settings()
            if self.text1!= "" and "," in self.text1:
                temp = self.text1.split(",")
                temp = [int(a) for a in temp]
                settings["exception"] = temp
            if self.text2 != "" and "," in self.text2:
                temp = self.text2.split(",")
                settings["names"] = temp

            with open("settings.json", "w", encoding="utf-8") as file:
                json.dump(settings, file, ensure_ascii=False, indent=4)

            self.accept()
