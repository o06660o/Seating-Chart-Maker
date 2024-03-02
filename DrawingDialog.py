# -*- coding: utf-8 -*-

import random

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPixmap, QPalette, QFont
from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QStackedLayout,
    QLabel,
    QTableWidget,
    QAbstractItemView,
    QHeaderView,
    QTableWidgetItem,
)

from util import read_settings


class DrawingDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.settings = read_settings()
        self.names = random.sample(self.settings["names"], 10)
        self.table_font = QFont()
        self.table_font.setPointSize(24)

        self.setupUI()
        self.draw10()

    def setupUI(self) -> None:
        self.setWindowTitle("Drawing")
        self.resize(920, 560)
        self.setWindowIcon(QPixmap("./assets/icons/DrawingDialog.png"))
        background = QPixmap("./assets/background.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, background)
        self.setPalette(palette)

        self.button_draw1 = QPushButton("抽取一名学生", self)
        self.button_draw1.setGeometry(QRect(100, 480, 200, 60))
        self.button_draw1.setObjectName("settings_button")
        self.button_draw1.clicked.connect(self.draw1)

        self.button_draw10 = QPushButton("抽取十名学生", self)
        self.button_draw10.setGeometry(QRect(620, 480, 200, 60))
        self.button_draw10.setObjectName("button_draw10")
        self.button_draw10.clicked.connect(self.draw10)

        self.label_result = QLabel(self)
        self.label_result.setGeometry(QRect(60, 50, 800, 380))
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_result.setStyleSheet("background-color: white")

        self.table_result = QTableWidget(self)
        self.table_result.setGeometry(QRect(60, 50, 800, 380))
        # set the content of the table uneditable
        self.table_result.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_result.horizontalHeader().setVisible(False)
        self.table_result.verticalHeader().setVisible(False)
        self.table_result.setColumnCount(5)
        self.table_result.setRowCount(2)
        self.table_result.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_result.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_result.cellClicked.connect(self.name_clicked)
        self.table_result.setStyleSheet(
            "QTableWidget::item:selected \
            { color: black; background-color: transparent; }"
        )

        self.layout_stacked = QStackedLayout()
        self.layout_stacked.addWidget(self.label_result)
        self.layout_stacked.addWidget(self.table_result)

    def draw1(self) -> None:
        self.layout_stacked.setCurrentIndex(0)
        name = random.choice(self.settings["names"])
        self.label_result.setText(
            f"<span style='font-size:60pt; color:red;'>\
            {name}\
            </span>"
        )

    def draw10(self) -> None:
        self.layout_stacked.setCurrentIndex(1)
        self.names = random.sample(self.settings["names"], 10)
        for key in range(10):
            item = QTableWidgetItem(self.names[key])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFont(self.table_font)
            self.table_result.setItem(key // 5, key % 5, item)

    def name_clicked(self, row: int, col: int) -> None:
        name = random.choice(self.settings["names"])
        while name in self.names:
            name = random.choice(self.settings["names"])
        old = self.names.index(self.table_result.item(row, col).text())
        self.names[old] = name
        item = QTableWidgetItem(name)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFont(self.table_font)
        self.table_result.item(row, col).setSelected(False)
        self.table_result.setItem(row, col, item)
