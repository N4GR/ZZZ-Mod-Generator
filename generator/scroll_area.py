from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QMainWindow, QToolButton
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

from config.window import windowConfig
from config.module import modulesConfig
import config.module

from PIL import Image
from PIL.ImageQt import ImageQt

import io

import math

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

class addItems():
    def __init__(self, main_window: QMainWindow, grid_layout: QGridLayout) -> None:
        '''
        Adds items to the scrollable region with a grid layout and an actions list.
        The button actions will be grabbed form the list in sequential order.

        actions = list[Object] : List of action objects
        '''
        # Create module object list
        modules_list = modulesConfig().list
        mods_count = len(modules_list)
        # Calculate number of rows needed in grid
        row_count = int(math.ceil(mods_count / 4))
        # Number of columns to have on one row; 4 is sufficient.
        column_count = 4

        loop_count = 0
        # Add buttons to the grid layout
        for row in range(row_count):
            for col in range(column_count):
                loop_count += 1
                if loop_count > mods_count:
                    return
                
                module = config.module.moduleOBJConstructur(modules_list[loop_count - 1])
                
                font = QFont("inpin", 12)

                button = QToolButton()
                button.setFont(font)
                button.setText(module.name)
                button.setFixedSize(150, 200)
                button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(module.thumbnail))))))
                button.setIconSize(QSize(124, 124))
                button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: 0px;
                    }
                """)

                button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

                ### Adds action to the button
                # Obtains the function using name and assigns it to button
                func = getattr(config.module.moduleFunctions, module.function_name)
                button.clicked.connect(lambda: func(main_window))

                grid_layout.addWidget(button, row, col)