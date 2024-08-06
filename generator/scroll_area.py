from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QMainWindow, QToolButton
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

class scrollArea():
    def __init__(self, main_window: QMainWindow) -> None:
        '''scrollArea class generator for creating scrollable areas within the main UI.

        Attributes:
            scroll_area [QScrollArea]: The scroll area being generated.
            grid_layout [QGridLayout]: The grid layout being used inside the scroll area.
        '''
        window = windowConfig()
        self.main_window = main_window

        # Create a scroll area
        self.scroll_area = QScrollArea(self.main_window)

        # Create a widget to hold the grid layout
        container = QWidget()
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        # Create a grid layout
        self.grid_layout = QGridLayout(container)

        self.grid_layout.setSpacing(5)

        # Set up the container widget
        container.setLayout(self.grid_layout)

        self.scroll_area.resize(window.width - 10, window.height - 140)
        self.scroll_area.move(5, 110)

        self.scroll_area.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.scroll_area.setStyleSheet("background-color: transparent; border: 0px")

class addToScrollArea():
    def __init__(self, grid_layout: QGridLayout, scroll_area: QScrollArea, main_window: QMainWindow, items: list[object]) -> None:
        '''Adds items to the scroll area from a list of objects

        Requirements:
            grid_layout: QGridLayout
            items list[object]: object must contain 'type', 'name', 'thumbnail'
        
        Attributes:
            item_count [int]: count of items being given.
            row_count [int]: count of rows being used.
            column_count [int]: count of columns being used. 
        '''

        self.items = items
        self.item_count = len(self.items)

        self.row_count = int(math.ceil(self.item_count / 4))
        self.column_count = 4

        loop_count = 0
        # For every row, add a column which is a widget but don't add more columns than there is items.
        for row in range(self.row_count):
            for col in range(self.column_count):
                loop_count += 1
                if loop_count > self.item_count:
                    return
                
                item = self.items[loop_count - 1]

                # Modules on the main menu are buttons
                if item.type == "module":
                    widget = N4QToolButton(item.name, item.thumbnail)
                    func = getattr(config.module.moduleFunctions, item.function_name)
                    widget.clicked.connect(lambda checked=False, f=func, mw=main_window: f(mw))
                    widget.clicked.connect(lambda: removeScrollArea(scroll_area))
                
                # If they're trying to add an image, do this
                if item.type == "image":
                    widget = None
                
                grid_layout.addWidget(widget, row, col)

def removeScrollArea(scroll_area: QScrollArea):
    '''removeScrollArea function to remove a scroll area.'''
    scroll_area.setParent(None)