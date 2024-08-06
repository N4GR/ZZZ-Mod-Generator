from PyQt6.QtWidgets import QMainWindow, QPushButton

from generator.scroll_area import scrollArea, addToScrollArea

from config.assets import assetConfig
from config.module import modulesConfig
ASSETS = assetConfig()


import time
class boxArt():
    def __init__(self, main_window: QMainWindow) -> None:
        # Initialising new buttons
        self.buttons = Buttons(main_window)
        
        time.sleep(5)
        # Initialising new scroll area
        y = []
        for x in range(20):
            y.append(test())

        self.scroll_area = scrollArea(main_window)
        addToScrollArea(self.scroll_area.grid_layout, self.scroll_area.scroll_area, main_window, y)
        self.scroll_area.scroll_area.show()

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
    
class test:
    def __init__(self) -> None:
        self.name = "Lebron James"
        self.type = "module"
        self.thumbnail = ASSETS.images.icon.bytes
        self.function_name = "boxArt"