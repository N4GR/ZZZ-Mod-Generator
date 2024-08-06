from PyQt6.QtWidgets import QMainWindow, QPushButton

from generator.scroll_area import scrollArea, addToScrollArea

from config.assets import assetConfig
from config.module import modulesConfig
from modules.boxArt import assets
BASE_ASSETS = assetConfig()

import time
class boxArt():
    def __init__(self, main_window: QMainWindow) -> None:
        # Initialising new buttons
        #self.buttons = Buttons(main_window)

        print("I'm working! box")
        
        # Initialising new scroll area
        self.scroll_area = scrollArea(main_window)

class Buttons():
    def __init__(self, main_window: QMainWindow) -> None:
        '''Buttons class containing and initialising all buttons for boxArt.

        Attributes:
            upload_button [QPushButton]: Upload button of the boxArt UI.
        '''
        self.main_window = main_window

        # Creates upload button
        self.upload_button = self.uploadButton()
    
    def uploadButton(self):
        def func():
            pass

        button = QPushButton(self.main_window)
        button.setText("Hello")
        button.setGeometry(500, 30, 80, 52)
        button.show()

        return button