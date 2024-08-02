import sys, os, ctypes
from screeninfo import get_monitors

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow

from config.window import windowConfig
from config.assets import assetConfig

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

        self.setWindowIcon(QtGui.QIcon(assets.images.icon))

        label = QtWidgets.QLabel(self)
        label.setPixmap(QtGui.QPixmap(assets.images.background))
        self.setCentralWidget(label)
        self.resize(window.width, window.height)

        self.setStyleSheet(r"QMainWindow {background: transparent}")
        
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
        )
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if event.pos().y() < 100:
                self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
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
    
        # Initialise buttons.
        self.buttons = buttons(self.main_window)

        self.buttons.exitButton()
        self.buttons.minimiseButton()

        # Initialise images.
        self.images = images(self.main_window)

        self.images.icon()

        self.main_window.show()
        sys.exit(self.main_app.exec())

class images():
    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window
    
    def icon(self):
        label = QtWidgets.QLabel(self.main_window)
        image = QtGui.QPixmap(assets.images.icon)

        image = image.scaled(
            QtCore.QSize(64, 64),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        label.resize(QtCore.QSize(64, 64))
        label.setPixmap(image)

        label.move(20, 20)

class buttons():
    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window
        
    def exitButton(self) -> QtWidgets.QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QtGui.QIcon(assets.buttons.exit.down))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QtGui.QIcon(assets.buttons.exit.up))

        # Creating button widget
        button = QtWidgets.QPushButton("", self.main_window)
        button.clicked.connect(lambda: buttonFunctions.exitButton(button))
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(690, 30, 80, 52)

        # Setting icon
        button.setIcon(QtGui.QIcon(assets.buttons.exit.up))
        button.setIconSize(QtCore.QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button
    
    def minimiseButton(self) -> QtWidgets.QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QtGui.QIcon(assets.buttons.minimise.down))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QtGui.QIcon(assets.buttons.minimise.up))

        # Creating button widget
        button = QtWidgets.QPushButton("", self.main_window)
        button.clicked.connect(lambda: buttonFunctions.minimiseButton(button, self.main_window))
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(600, 30, 80, 52)

        # Setting icon
        button.setIcon(QtGui.QIcon(assets.buttons.minimise.up))
        button.setIconSize(QtCore.QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button

class buttonFunctions:
    def exitButton(button: QtWidgets.QPushButton):
        sys.exit()
    
    def minimiseButton(button: QtWidgets.QPushButton, window: MainWindow):
        window.showMinimized()


if __name__ == "__main__":
    assets = assetConfig()
    window = windowConfig()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(window.app_id)

    ui()