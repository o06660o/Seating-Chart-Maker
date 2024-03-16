# -*- coding: utf-8 -*-

import json

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
)

from util import read_settings


class SettingsDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.settings = read_settings()
        self.setupUI()

    def setupUI(self) -> None:
        self.setWindowTitle("Settings")
        self.resize(400, 270)
        self.setWindowIcon(QPixmap("./assets/icons/SettingsDialog.png"))

        # Create widgets for the settings
        self.label_exception = QLabel(
            "输入坐在最后两个的同学学号(不输入表示不修改):\
            \n样例输入1, 2\
            \n请用英文逗号分隔两个数据"
        )
        self.edit_exception = QTextEdit()
        text = str(self.settings["exception"])[1:-1]
        self.edit_exception.setPlainText(text)
        self.edit_exception.setMaximumSize(400, 28)
        self.label_names = QLabel("输入同学的姓名(不输入表示不修改):")
        text = str(self.settings["names"])[1:-1]
        text = text.replace("'", "")
        self.edit_names = QTextEdit()
        self.edit_names.setPlainText(text)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.open_warning_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.label_exception)
        layout.addWidget(self.edit_exception)
        layout.addWidget(self.label_names)
        layout.addWidget(self.edit_names)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def open_warning_dialog(self) -> None:
        warningdialog = self.WarningDialog(
            self.edit_exception.toPlainText(), self.edit_names.toPlainText()
        )
        warningdialog.exec()

    class WarningDialog(QDialog):
        def __init__(self, text1, text2) -> None:
            super().__init__()
            self.text1 = text1
            self.text2 = text2
            self.setupUI()

        def setupUI(self) -> None:
            self.setWindowTitle("Warning")
            self.resize(400, 200)
            self.setWindowIcon(QPixmap("./assets/icons/WarningDialog.jpg"))

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

        def settings_valid(self) -> bool:
            """return True if the input settings are valid"""
            if self.text1 != "" and "," in self.text1:
                temp = self.text1.split(",")
                for number in temp:
                    try:
                        number = int(number)
                    except ValueError:
                        return False
                    except Exception as e:
                        print(e)
                        return False
                    if number <= 0 or number >= 51:
                        return False
            if self.text2 != "" and "," in self.text2:
                temp = self.text2.split(",")
                if len(temp) != 50:
                    return False
            return True

        def save_settings(self) -> None:
            """Save the settings to the settings file"""
            if not self.settings_valid():
                return None
            settings = read_settings()
            if self.text1 != "" and "," in self.text1:
                temp = self.text1.split(",")
                temp = [int(a) for a in temp]
                settings["exception"] = temp
            if self.text2 != "" and "," in self.text2:
                temp = self.text2.split(",")
                temp = [name.strip() for name in temp]
                settings["names"] = temp

            with open("settings.json", "w", encoding="utf-8") as file:
                json.dump(settings, file, ensure_ascii=False, indent=4)

            self.accept()
