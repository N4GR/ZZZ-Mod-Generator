from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize

from PIL import Image
from PIL.ImageQt import ImageQt

import io

from generator.scroll_area import scrollArea

from config.assets import assetConfig
from modules.base import assets

import obj

class uploading():
    def __init__(self, main_window: QMainWindow, module_name: str) -> None:
        ROOT_ASSETS = assetConfig()
        IMAGE_ASSETS = assets.images(module_name)

        # Initialising new images
        self.images = Images(main_window, image_assets = IMAGE_ASSETS)
        
        # Initialising new scroll area
        self.scroll_area = scrollArea(main_window, (683, 460), 5)
        self.scroll_area.addItems(IMAGE_ASSETS.data)

        # Initialising new buttons
        self.buttons = Buttons(main_window, self.scroll_area, image_assets = IMAGE_ASSETS)

class Images():
    def __init__(self, main_window: QMainWindow, image_assets) -> None:
        '''Images class containing and initialising all images for base.

        Attributes:
            side_panel [QLabel]: Side panel of the boxArt UI.
        '''
        self.__image_assets = image_assets 
        self.__main_window = main_window
        
        self.side_panel = self.sidePanel()
    
    def sidePanel(self):
        label = QLabel(self.__main_window)
        pixmap = QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(self.__image_assets.side_panel.bytes))))

        label.setPixmap(pixmap)
        label.setGeometry(690, 108, self.__image_assets.side_panel.width, self.__image_assets.side_panel.height)

        label.show()
        return label

class Buttons():
    def __init__(self, main_window: QMainWindow, scroll_area: scrollArea, image_assets) -> None:
        '''Buttons class containing and initialising all buttons for base.

        Attributes:
            upload_button [QPushButton]: Upload button of the base UI.
            open_images [list[object]]: List of scrollImages objects of currently open images.
        '''
        # Creates private attributes
        self.__main_window = main_window
        self.__scroll_area = scroll_area
        self.__image_assets = image_assets

        # Creates open_images list for self.upload() to add to
        self.open_images = []

        # Creates upload button
        self.upload_button = self.uploadButton()
    
    def uploadButton(self):
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(self.__image_assets.upload_button.down.bytes))))))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(self.__image_assets.upload_button.up.bytes))))))

        def func():
            files = QFileDialog.getOpenFileUrls(self.__main_window, "Open File", filter = "Image Files (*.png *.jpg)")

            x = []

            for file in files[0]:
                path = file.path()[1:]

                scroll_image = obj.scrollImages(path)

                x.append(scroll_image)
                self.open_images.append(scroll_image)
            
            self.__scroll_area.addItems(x)

        button = QPushButton(self.__main_window)
        button.setText("")
        button.setGeometry(700, 150, 80, 52)

        button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(self.__image_assets.upload_button.up.bytes))))))
        button.setIconSize(QSize(52, 52))

        button.pressed.connect(pressed)
        button.released.connect(released)
        button.clicked.connect(func)

        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")
        button.show()

        return button