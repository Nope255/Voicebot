import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
import logging

Application = QApplication
MainWindow = QMainWindow

logging.basicConfig(
    level = logging.WARNING,
    format = "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)

Critical = logging.critical
Information = logging.info

SysArgv = sys.argv
SysExit = sys.exit
