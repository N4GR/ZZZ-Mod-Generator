import sys, ctypes
from screeninfo import get_monitors

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QScrollArea, QWidget, QGridLayout, QToolButton
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap, QIcon
from PyQt6.QtCore import QSize, Qt

from config.window import windowConfig
from config.assets import assetConfig
from config.module import modulesConfig
from config.module import moduleFunctions
from config.module import moduleOBJConstructur

import io
from PIL.ImageQt import ImageQt
from PIL import Image

import math

class getMonitors:
    def __init__(self) -> None:
        self.monitors = self.getMonitors()
        self.main_monitor = self.getMainMonitor()
    
    def getMonitors(self) -> list[object]:
        '''
        A function to return a list of the current monitors.

        -> list[obj] = Objects of monitors
        '''
        monitors = []
        for m in get_monitors():
            monitors.append(m)

        return monitors

    def getMainMonitor(self) -> object:
        '''
        A function to get the main monitor from the monitors object list.

        -> object = Object of main monitor.
        '''

        for m in self.monitors:
            if m.is_primary is True: return m

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.monitors = getMonitors()

        self.setFixedSize(window.width, window.height)
        self.setWindowTitle(window.title)

        self.setWindowIcon(QIcon(QPixmap.fromImage(assets.images.icon)))

        label = QLabel(self)
        label.setPixmap(QPixmap.fromImage(assets.images.background))
        self.setCentralWidget(label)
        #self.resize(window.width, window.height)

        self.setStyleSheet(r"QMainWindow {background: transparent}")
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.pos().y() < 100:
                self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        try:
            if self.offset is not None:
                pass
        except AttributeError:
            self.offset = None

        if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

class ui():
    def __init__(self) -> None:
        self.main_app = QApplication(sys.argv)
        self.main_window = MainWindow()

        # Initialise images.
        self.images = images(self.main_window)

        self.images.icon()

        # Initialise text.
        self.text = text(self.main_window)

        self.text.title()

        # Initialise scroll area
        self.scroll = scroll(self.main_window).getScrollArea()

        # Initialise buttons.
        self.buttons = buttons(self.main_window)

        self.buttons.exitButton()
        self.buttons.minimiseButton()

        self.main_window.show()
        sys.exit(self.main_app.exec())

class scroll():
    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window
        # Create a scroll area
        self.scroll_area = QScrollArea(self.main_window)
        #self.scroll_area.setParent(None)

        # Create a widget to hold the grid layout
        container = QWidget()
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        # Create a grid layout
        grid_layout = QGridLayout(container)

        grid_layout.setSpacing(5)

        # Adds items to layout
        self.addItems(grid_layout)

        # Set up the container widget
        container.setLayout(grid_layout)

        self.scroll_area.resize(window.width - 10, window.height - 140)
        self.scroll_area.move(5, 110)

        self.scroll_area.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.scroll_area.setStyleSheet("background-color: transparent; border: 0px")
    
    def getScrollArea(self):
        return self.scroll_area

    def addItems(self, grid_layout: QGridLayout):
        '''
        Adds items to the scrollable region with a grid layout and an actions list.
        The button actions will be grabbed form the list in sequential order.

        actions = list[Object] : List of action objects
        '''
        # Create module object list
        mods = modulesConfig().list
        mods_count = len(mods)
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
                
                module = moduleOBJConstructur(mods[loop_count - 1])
                
                font = QFont("inpin", 12)

                button = QToolButton()
                button.setFont(font)
                button.setText(module.name)
                button.setFixedSize(150, 200)
                button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(module.thumnail))))))
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
                func = getattr(moduleFunctions, module.function_name)
                button.clicked.connect(lambda: func(self.main_window))

                # Make button hide scrollArea when clicked
                button.clicked.connect(lambda: buttonFunctions.removeScrollArea(self.scroll_area))

                grid_layout.addWidget(button, row, col)

class text():
    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window

        QFontDatabase.addApplicationFont(assets.fonts.inpin)
    
    def title(self):
        font = QFont("inpin", 18)
        font.setBold(True)

        label = QLabel(self.main_window)
        label.setFont(font)
        label.setText("ZZZ Mod Generator")

        label.resize(QSize(250, 30))

        label.move(100, 35)

class images():
    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window
    
    def icon(self):
        label = QLabel(self.main_window)
        image = QPixmap.fromImage(assets.images.icon)

        image = image.scaled(
            QSize(64, 64),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.resize(QSize(64, 64))
        label.setPixmap(image)

        label.move(20, 20)

class buttons():
    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window
        
    def exitButton(self) -> QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(assets.buttons.exit.down)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(assets.buttons.exit.up)))

        # Creating button widget
        button = QPushButton("", self.main_window)
        button.clicked.connect(buttonFunctions.exitButton)
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(690, 30, 80, 52)

        # Setting icon
        button.setIcon(QIcon(QPixmap.fromImage(assets.buttons.exit.up)))
        button.setIconSize(QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button
    
    def minimiseButton(self) -> QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(assets.buttons.minimise.down)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(assets.buttons.minimise.up)))

        # Creating button widget
        button = QPushButton("", self.main_window)
        button.clicked.connect(lambda: buttonFunctions.minimiseButton(self.main_window))
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(600, 30, 80, 52)

        # Setting icon
        button.setIcon(QIcon(QPixmap.fromImage(assets.buttons.minimise.up)))
        button.setIconSize(QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button

class buttonFunctions:
    def exitButton():
        sys.exit()
    
    def minimiseButton(window: MainWindow):
        window.showMinimized()
    
    def removeScrollArea(scrollArea: QScrollArea):
        scrollArea.setParent(None)


if __name__ == "__main__":
    assets = assetConfig()
    window = windowConfig()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(window.app_id)

    ui()