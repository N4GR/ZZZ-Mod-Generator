from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QErrorMessage, QMessageBox, QInputDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize

from PIL import Image, ImageOps
from PIL.ImageQt import ImageQt

import io

from generator.scroll_area import scrollArea
from modules.base import assets
import obj
import sql

from wand import image

import os

class uploading():
    def __init__(self, main_window: QMainWindow, module_name: str) -> None:
        IMAGE_ASSETS = assets.images(module_name)
        self.module_name = module_name

        # Initialising new images
        self.images = Images(main_window, image_assets = IMAGE_ASSETS)
        
        # Initialising new scroll area
        self.scroll_area = scrollArea(main_window, (683, 460), 5)
        self.scroll_area.addItems(IMAGE_ASSETS.data, initial = True)

        # Initialising new buttons
        self.buttons = Buttons(main_window, self.scroll_area, image_assets = IMAGE_ASSETS, module_name = module_name)

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
    def __init__(self, main_window: QMainWindow, scroll_area: scrollArea, image_assets, module_name: str) -> None:
        '''Buttons class containing and initialising all buttons for base.

        Attributes:
            upload_button [QPushButton]: Upload button of the base UI.
            open_images [list[object]]: List of scrollImages objects of currently open images.
        '''
        # Creates private attributes
        self.__main_window = main_window
        self.__scroll_area = scroll_area
        self.__image_assets = image_assets
        self.__module_name = module_name

        # Creates open_images list for self.upload() to add to
        self.open_images = []

        # Creating button objects
        self.upload_button = self.uploadButton()
        self.start_button = self.startButton()
    
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

            if self.__maximum_replaced is True:
                error_message = QErrorMessage(self.__main_window)
                error_message.setWindowTitle("Maximum Images")
                error_message.showMessage(f"Only {opened_widgets} images can be used, the rest have been skipped.")
                error_message.exec()

                button.setDisabled(True)

            if failed != []:
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
    
    def startButton(self):
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(self.__image_assets.start_button.down.bytes))))))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(self.__image_assets.start_button.up.bytes))))))
        
        def warning():
            '''
            Warning function that will tell the user if they haven't inputted all the necessary images.
            '''
            if self.__maximum_replaced is False:
                dialog = QMessageBox(self.__main_window)
                dialog.setWindowTitle("Images Not Used")
                dialog.setText(f"You haven't replaced all the images, do you want to continue anyway?")
                dialog.setIcon(QMessageBox.Icon.Information)

                dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                clicked = dialog.exec()

                if clicked == QMessageBox.StandardButton.Yes:
                    getModName()
                else:
                    return
            else:
                getModName()
        
        def getModName():
            '''
            Opens an input dialog for getting the name of the mod generated.
            '''
            dialog = QInputDialog(self.__main_window)
            dialog.setWindowTitle("Input Mod Name")
            dialog.setLabelText("Enter Mod Name:")
            dialog.setInputMode(QInputDialog.InputMode.TextInput)

            clicked = dialog.exec()

            if clicked:
                self.mod_name = dialog.textValue()
                getModLocation()
            else:
                return
            
        def getModLocation():
            '''
            Opens an input dialog for getting the location to where the mod is generated.
            '''
            dialog = QInputDialog(self.__main_window)
            dialog.setWindowTitle("Input Save Location")
            dialog.setLabelText("Enter Save Location:")
            dialog.setInputMode(QInputDialog.InputMode.TextInput)
            
            clicked = dialog.exec()

            if clicked:
                self.mod_save_path = dialog.textValue()
                func()
            else:
                return

        def func():
            '''
            Starts the process of creating the mod with the given variables.
            '''
            button.setDisabled(True)
            self.upload_button.setDisabled(True)

            # Pass on to image generator
            modGenerator(self.__main_window, self.__image_assets.data, button, self.upload_button, self.__module_name, self.mod_name, self.mod_save_path)

        # Creating variables for save locations.
        self.mod_name = None
        self.mod_save_path = None

        # Creates the QPushbutton.
        button = QPushButton(self.__main_window)
        button.setText("")
        button.setGeometry(700, 225, 80, 52)

        # Sets the button's icon QPixmap to a given image in assets.
        button.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(self.__image_assets.start_button.up.bytes))))))
        button.setIconSize(QSize(52, 52))

        # Attaches functions to correct button positions.
        button.pressed.connect(pressed)
        button.released.connect(released)
        button.clicked.connect(warning)

        # Removes border from the back of the images.
        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")
        
        # Sets the button to show once created.
        button.show()

        return button

class modGenerator():
    def __init__(self, main_window: QMainWindow, image_asset_data: list[object], start_button: QPushButton, upload_button: QPushButton, module_name: str, mod_name: str, save_location: str) -> None:
        '''Mod Generator function that will create the modded image, convert it to DDS and then create an INI image.
        
        Attributes:
            canvas [PIL.Image.Image]: Canvas image object of generated image.
            iniBytes [bytes]: Bytes of INI file.
            DDSLocation [str]: Location for where the DDS was saved.
            INILocation [str]: Location for where the INI was saved.
        '''
        
        self.__main_window = main_window
        self.__image_asset_data = image_asset_data
        self.__start_button = start_button
        self.__upload_button = upload_button
        self.__module_name = module_name
        self.__mod_name = mod_name
        self.__save_location = save_location

        self.canvas = self.makeCanvas()
        self.iniBytes = self.getINI()

        self.mod_location = self.makeFolder()

        self.DDSLocation = self.convertToDDS(self.canvas)
        self.INILocation = self.saveINI(self.iniBytes)

        self.__start_button.setDisabled(False)
        self.__upload_button.setDisabled(False)

    def makeCanvas(self) -> Image.Image:
        '''A canvas function to create a canvas with Image.new()'''
        canvas_data = obj.Canvas(self.__module_name, self.__image_asset_data)
        canvas = canvas_data.background

        for image in canvas_data.images:
            res_image = image.image.resize((image.width, image.height), Image.Resampling.LANCZOS)
            rot_image = res_image.rotate(image.rotation, expand = True)
        
            canvas.paste(rot_image, (image.x, image.y))

        return canvas
    
    def getINI(self) -> bytes:
        '''getINI function to retrieve bytes of module name from database.'''
        sq = sql.sql()

        iniblob = sq.get("modules", f"name = '{self.__module_name}'", "ini")
        iniblob = iniblob[0]

        sq.close()

        return iniblob
    
    def makeFolder(self) -> str:
        mod_path = f"{self.__save_location}\\{self.__mod_name}"

        if not os.path.exists(mod_path):
            os.makedirs(mod_path)
            print("Created")
        else:
            print("Already exists")

        return mod_path

    def convertToDDS(self, canvas: Image.Image) -> str:
        '''Convert canvas image to DDS and save it to a location.'''
        canvas = ImageOps.flip(canvas)
        stream = io.BytesIO()
        canvas.save(stream, format = "PNG")
        imagebytes = stream.getvalue()

        file_path = f"{self.mod_location}\\{self.__module_name}"

        with image.Image(blob = imagebytes) as img:
            img.compression = "dxt5"
            img.save(filename = f"{file_path}.dds")

        return f"{file_path}.dds"

    def saveINI(self, iniBytes: bytes) -> str:
        '''Creates an INI file and saves it to a location.'''
        file_path = f"{self.mod_location}\\{self.__mod_name}"

        with open(f"{file_path}.ini", "wb") as binary:
            binary.write(iniBytes)

        return f"{file_path}.ini"