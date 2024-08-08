from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize

from PIL import Image
from PIL.ImageQt import ImageQt

import io

from generator.scroll_area import scrollArea, addToScrollArea

from config.assets import assetConfig
from config.module import modulesConfig
from modules.boxArt import assets
BASE_ASSETS = assetConfig()
IMAGES = assets.images()

import obj

class uploading():
    def __init__(self, main_window: QMainWindow) -> None:
        # Initialising new images
        self.images = Images(main_window)
        
        # Initialising new scroll area
        scroll = scrollArea(main_window, (683, 460), 5)
        #addToScrollArea(scroll.grid_layout, scroll.scroll_area, main_window, modulesConfig().list)

        # Initialising new buttons
        self.buttons = Buttons(main_window, scroll)

class Images():
    def __init__(self, main_window: QMainWindow) -> None:
        '''Images class containing and initialising all images for base.

        Attributes:
            side_panel [QLabel]: Side panel of the boxArt UI.
        '''
        self.__main_window = main_window
        
        self.side_panel = self.sidePanel()
    
    def sidePanel(self):
        label = QLabel(self.__main_window)
        pixmap = QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(IMAGES.side_panel.bytes))))

        label.setPixmap(pixmap)
        label.setGeometry(690, 108, IMAGES.side_panel.width, IMAGES.side_panel.height)

        label.show()
        return label

class Buttons():
    def __init__(self, main_window: QMainWindow, scroll_area: scrollArea) -> None:
        '''Buttons class containing and initialising all buttons for base.

        Attributes:
            upload_button [QPushButton]: Upload button of the base UI.
        '''
        self.__main_window = main_window
        self.__scroll_area = scroll_area

        self.__sa = None

        # Creates upload button
        self.upload_button = self.uploadButton()
    
    def uploadButton(self):
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(IMAGES.upload_button.down.bytes))))))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(IMAGES.upload_button.up.bytes))))))

        def func():
            files = QFileDialog.getOpenFileUrls(self.__main_window, "Open File", filter = "Image Files (*.png *.jpg)")

            x = []

            for file in files[0]:
                path = file.path()[1:]

                x.append(obj.scrollImages(path))
            
            self.__scroll_area.addItems(x)

        button = QPushButton(self.__main_window)
        button.setText("")
        button.setGeometry(700, 150, 80, 52)

        button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(IMAGES.upload_button.up.bytes))))))
        button.setIconSize(QSize(52, 52))

        button.pressed.connect(pressed)
        button.released.connect(released)
        button.clicked.connect(func)

        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")
        button.show()

        return button