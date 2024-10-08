# Third party libraries
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QErrorMessage, QMessageBox, QInputDialog, QApplication, QWidget, QScrollArea, QGridLayout, QToolButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QIcon, QFontDatabase, QFont, QMovie
from PyQt6.QtCore import QSize, Qt, QPoint, QThread

from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance, ImageChops
from PIL.ImageQt import ImageQt

# Python libraries
from collections import Counter
import json
import sys
import ctypes
import json
import imageio
import os
import random
import logging

# Local imports
from config import logger
from config.resource_path import resource_path

def setup(name: str) -> logging.Logger:
    logging = logger.Logger(name)
    log = logging.log

    sys.excepthook = logging.custom_excepthook

    return log