from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QErrorMessage
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
        self.scroll_area.addItems(IMAGE_ASSETS.data, initial = True)

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
            failed = []

            for file in files[0]:
                path = file.path()[1:]

                # Checks if the user is trying to open too many images
                if len(self.open_images) + 1 > opened_widgets:
                    self.__maximum_replaced = True
                    continue

                # Check if image is corrupt
                try:
                    img = Image.open(path)
                    img.close()
                except (IOError, SyntaxError) as e:
                    print(e)
                    # Add failed path to failed list
                    failed.append(path)
                    continue

                scroll_image = obj.scrollImages(path)

                x.append(scroll_image)
                self.open_images.append(scroll_image)

                # Replace the item in opened images assets
                self.__image_assets.data[len(self.open_images) - 1] = obj.addingImage(path)

            print(self.__image_assets.data)

            if self.__maximum_replaced is True:
                error_message = QErrorMessage(self.__main_window)
                error_message.setWindowTitle("Maximum Images")
                error_message.showMessage(f"Only {opened_widgets} images can be used, the rest have been skipped.")
                error_message.exec()

            if failed != []:
                print("Here!")
                failed_lst = [f"{x}\n" for x in failed]
                failed_str = "".join(failed_lst)

                error_message = QErrorMessage(self.__main_window)
                error_message.setWindowTitle("Corrupt Images")
                error_message.showMessage(f"The following images are corrupted and cannot be processed:\n{failed_str}")
                error_message.exec()

            if x != []:
                self.__scroll_area.addItems(x)

        # Booleon to check if maximum images have been replaced.
        self.__maximum_replaced = False

        # Obtains the amount of widgets created when the main file is initialised.
        opened_widgets = len(self.__image_assets.data)

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