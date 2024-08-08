from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QMainWindow, QToolButton, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont

from PIL.ImageQt import ImageQt
from PIL import Image

from config.window import windowConfig
import math
import io

import config.module

class N4QToolButton(QToolButton):
    def __init__(self, button_name: str, button_icon: bytes) -> None:
        super(N4QToolButton, self).__init__()

        font = QFont("inpin", 12)

        self.setFont(font)
        self.setText(button_name)
        self.setFixedSize(150, 200)
        self.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(button_icon))))))
        self.setIconSize(QSize(124, 124))
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 0px;
            }
        """)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

class N4QImageWithText(QWidget):
    def __init__(self, text: str, type: str, image_path: str = None, img: object = None) -> None:
        super(N4QImageWithText, self).__init__()
        width, height = (100, 150)

        # Creating image label
        if type == "image":
            img = Image.open(image_path)

        img.thumbnail((width, height), Image.Resampling.LANCZOS)

        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt(img)))
        self.image_label.setFixedSize(width, height)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #img.close()

        # Creating text label
        if len(text) > 13: text = f"{text[:11]}..."
        self.text_label = QLabel(self)
        font = QFont("inpin", 12)
        self.text_label.setFont(font)
        self.text_label.setText(text)
        self.text_label.setFixedWidth(width)

        # Creating layout to add the widgets to
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

class scrollArea():
    def __init__(self, main_window: QMainWindow, size: tuple[int] = None, max_column: int = 4) -> None:
        '''scrollArea class generator for creating scrollable areas within the main UI.

        Attributes:
            scroll_area [QScrollArea]: The scroll area being generated.
            grid_layout [QGridLayout]: The grid layout being used inside the scroll area.
        '''
        self.main_window = main_window

        if size == None: size = (790, 460)

        # Create a scroll area
        self.scroll_area = QScrollArea(main_window)

        # Create a widget to hold the grid layout
        container = QWidget()
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        # Create a grid layout
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setSpacing(5)

        # Set up the container widget
        container.setLayout(self.grid_layout)
        
        self.scroll_area.resize(size[0], size[1])
        self.scroll_area.move(5, 110)

        self.scroll_area.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.scroll_area.setStyleSheet("background-color: transparent; border: 0px")

        self.scroll_area.show()

        # Initialising addItems requirements.
        self.row = 0
        self.column = 0

        self.max_column = max_column

    def addItems(self, items: list[object]):
        def getFunc(function_name: str):
            return getattr(config.module.moduleFunctions, function_name)

        def makeLambda(func):
            return lambda: func(self.main_window)

        for item in items:
            if self.column == self.max_column:
                self.column = 1
                self.row += 1
            else: self.column += 1

            if item.type == "module":
                func = getFunc(item.function_name)
                widget = N4QToolButton(item.name, item.thumbnail)
                widget.clicked.connect(makeLambda(func))
                widget.clicked.connect(self.delete)
            if item.type == "image":
                widget = N4QImageWithText(text = f"{item.name}.{item.file_type}", type = "image", image_path = item.path)
            if item.type == "default":
                widget = N4QImageWithText(text = f"{item.name}", type = "default", img = item.image)

            self.grid_layout.addWidget(widget, self.row, self.column)
    
    def delete(self):
        self.scroll_area.setParent(None)