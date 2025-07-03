import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)


Application = QApplication
MainWindow = QMainWindow

SysArgv = sys.argv
SysExit = sys.exit

APP_NAME: str = "Voice Bot"
APP_WIDTH: int = 600
APP_HEIGHT: int = 600