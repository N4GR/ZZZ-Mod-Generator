import sys, ctypes

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QScrollArea
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap, QIcon
from PyQt6.QtCore import QSize, Qt

from config.window import windowConfig
from config.assets import assetConfig
from config.module import modulesConfig

import generator.scroll_area

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setFixedSize(WINDOW.width, WINDOW.height)
        self.setWindowTitle(WINDOW.title)

        self.setWindowIcon(QIcon(QPixmap.fromImage(ASSETS.images.icon.image)))

        label = QLabel(self)
        label.setPixmap(QPixmap.fromImage(ASSETS.images.background.image))
        self.setCentralWidget(label)

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


        # Initialise text.
        self.text = text(self.main_window)

        # Initialise scroll area
        scroll = generator.scroll_area.scrollArea(self.main_window)
        generator.scroll_area.addToScrollArea(scroll.grid_layout, scroll.scroll_area, self.main_window, modulesConfig().list)

        # Initialise buttons.
        self.buttons = buttons(self.main_window)

        self.main_window.show()
        sys.exit(self.main_app.exec())

class text():
    def __init__(self, main_window: MainWindow) -> None:
        '''Text class containing and initilising all text related to the main ui.
        
        Attributes:
            title [QLabel]: Title of the main UI.
        '''
        self.main_window = main_window

        QFontDatabase.addApplicationFont(ASSETS.fonts.inpin)
        
        self.title = self.titleText()
    
    def titleText(self):
        font = QFont("inpin", 18)
        font.setBold(True)

        label = QLabel(self.main_window)
        label.setFont(font)
        label.setText("ZZZ Mod Generator")

        label.resize(QSize(250, 30))

        label.move(100, 35)

        return label

class buttons():
    def __init__(self, main_window: MainWindow) -> None:
        '''Buttons class containing and initilising all buttons related to the main ui.
        
        Attributes:
            exit [QPushButton]: Exit push button of the main UI.
            minimise [QPushButton]: Minimise push button of the main UI.
        '''
        self.main_window = main_window

        self.exit = self.exitButton()
        self.minimise = self.minimiseButton()
        
    def exitButton(self) -> QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ASSETS.buttons.exit.down.image)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ASSETS.buttons.exit.up.image)))
        
        def func():
            sys.exit()

        # Creating button widget
        button = QPushButton("", self.main_window)
        button.clicked.connect(func)
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(690, 30, 80, 52)

        # Setting icon
        button.setIcon(QIcon(QPixmap.fromImage(ASSETS.buttons.exit.up.image)))
        button.setIconSize(QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button
    
    def minimiseButton(self) -> QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ASSETS.buttons.minimise.down.image)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ASSETS.buttons.minimise.up.image)))
        
        def func():
            self.main_window.showMinimized()

        # Creating button widget
        button = QPushButton("", self.main_window)
        button.clicked.connect(func)
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(600, 30, 80, 52)

        # Setting icon
        button.setIcon(QIcon(QPixmap.fromImage(ASSETS.buttons.minimise.up.image)))
        button.setIconSize(QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button

if __name__ == "__main__":
    ASSETS = assetConfig()
    WINDOW = windowConfig()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(WINDOW.app_id)

    ui()