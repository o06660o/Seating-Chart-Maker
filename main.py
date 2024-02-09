# -*- coding: utf-8 -*-

import sys

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())
