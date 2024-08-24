from imports import *

from config.window import windowConfig
from config.module import module

from config.assets import button
from config.assets import panel
from config.assets import font

import generator.scroll_area

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setFixedSize(WINDOW.width, WINDOW.height)
        self.setWindowTitle(WINDOW.title)

        self.setWindowIcon(QIcon(QPixmap.fromImage(PANEL_ASSETS.icon)))

        label = QLabel(self)
        label.setPixmap(QPixmap.fromImage(PANEL_ASSETS.background))
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
    def __init__(self, new: bool = True, position: QPoint = None) -> None:
        '''Main menu creation class for the main UI which can be re-created.

        Parameters:
            new [bool] = True: if True, will create an Application - if False, will not.
            position [QPoint] = None: if None, and new is False, will fail - QPoint of previous main window.

        Usage:
            ui(new = False): This will re-create the main UI without closing the Application.
        '''
        if new is True: self.main_app = self.createApp()
        
        self.main_window = MainWindow()

        if new is False: self.main_window.move(position)

        # Initialise text.
        self.text = text(self.main_window)

        # Initialise scroll area
        scroll = generator.scroll_area.scrollArea(self.main_window)
        #generator.scroll_area.addToScrollArea(scroll.grid_layout, scroll.scroll_area, self.main_window, modulesConfig().list)
        scroll.addItems(module().list)

        # Initialise buttons.
        self.buttons = buttons(self.main_window)

        self.main_window.show()

        if new is True: self.createExit()
    
    def createApp(self) -> QApplication:
        main_app = QApplication(sys.argv)

        return main_app
    
    def createExit(self):
        sys.exit(self.main_app.exec())

class text():
    def __init__(self, main_window: MainWindow) -> None:
        '''Text class containing and initilising all text related to the main ui.
        
        Attributes:
            title [QLabel]: Title of the main UI.
        '''
        self.main_window = main_window

        QFontDatabase.addApplicationFont(FONT_ASSETS.inpin)
        
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
        self.home = self.homeButton()
        
    def exitButton(self) -> QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.exit.down)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.exit.up)))
        
        def func():
            sys.exit()

        # Creating button widget
        button = QPushButton("", self.main_window)
        button.clicked.connect(func)
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(690, 30, 80, 52)

        # Setting icon
        button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.exit.up)))
        button.setIconSize(QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button
    
    def minimiseButton(self) -> QPushButton:
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.minimise.down)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.minimise.up)))
        
        def func():
            self.main_window.showMinimized()

        # Creating button widget
        button = QPushButton("", self.main_window)
        button.clicked.connect(func)
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(600, 30, 80, 52)

        # Setting icon
        button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.minimise.up)))
        button.setIconSize(QSize(80, 52))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button

    def homeButton(self) -> QPushButton:
        def pressed():
            button.setGeometry(22, 22, 60, 60)
            button.setIconSize(QSize(60, 60))
        
        def released():
            button.setGeometry(20, 20, 64, 64)
            button.setIconSize(QSize(64, 64))

        def func():
            self.main_window.deleteLater()
            ui(new = False, position = self.main_window.pos())

        # Creating button widget
        button = QPushButton("", self.main_window)
        button.clicked.connect(func)
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.setGeometry(20, 20, 64, 64)

        # Setting icon
        button.setIcon(QIcon(QPixmap.fromImage(PANEL_ASSETS.icon)))
        button.setIconSize(QSize(64, 64))

        # Object styling handling
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")

        return button

if __name__ == "__main__":
    BUTTON_ASSETS = button()
    PANEL_ASSETS = panel()
    FONT_ASSETS = font()
    WINDOW = windowConfig()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(WINDOW.app_id)

    if '--debug' in sys.argv:
        # If --debug is provided, relaunch the script with the console visible
        subprocess.run(['python', __file__] + [arg for arg in sys.argv if arg != '--debug'])
    else:
        ui()