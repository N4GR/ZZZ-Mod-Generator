from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QMainWindow, QToolButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont

from PIL.ImageQt import ImageQt
from PIL import Image

from config.window import windowConfig
import math
import io

from config.module import moduleFunctions

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
        window = windowConfig()
        self.main_window = main_window
        # Create a scroll area
        self.scroll_area = QScrollArea(self.main_window)
        #self.scroll_area.setParent(None)

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
    
    def getGridLayout(self):
        return self.grid_layout

class addToScrollArea():
    def __init__(self, grid_layout: QGridLayout, main_window: QMainWindow, items: list[object]) -> None:
        '''Adds items to the scroll area from a list of objects

        Requirements:
            grid_layout: QGridLayout
            items: list[object]; object must contain 'type', 'name', 'thumbnail'
        '''
        self.grid_layout = grid_layout
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
                    func = getattr(moduleFunctions, item.function_name)
                    widget.clicked.connect(lambda: func(main_window))
                
                # If they're trying to add an image, do this
                if item.type == "image":
                    widget = None
                
                grid_layout.addWidget(widget, row, col)