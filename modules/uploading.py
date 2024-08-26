from imports import *
log = setup("UPLOADING")

# Local imports
from modules.specialties import Specialties
from generator.scroll_area import scrollArea
from config import assets
from config.paths import *
import obj

BUTTON_ASSETS = assets.button()
PANEL_ASSETS = assets.panel()
FONT_ASSETS = assets.font()

class uploading():
    def __init__(self,
                 main_window: QMainWindow,
                 module_name: str,
                 specialties: bool = False) -> None:
        """Uploading function that is called to create a mod that requires any kind of uploading of images.

        Args:
            main_window (QMainWindow): QMainWindow object crated from the main PyQt6 application.
            module_name (str): Name of the module the user clicked on from the main PyQt6 application.
            specialties (bool, optional): Specialties booleon if the clicked module contains any special requirements. Defaults to False.
        """
        self.module_name = module_name
        self.main_window = main_window

        # Initialising new images
        self.window_images = Images(main_window)
        
        # Initialising new scroll area
        self.scroll_area, self.other_images = self.createDefaultScrollArea()

        # Initialising new buttons
        self.buttons = Buttons(main_window,
                               self.scroll_area,
                               module_name = module_name,
                               images = self.other_images,
                               specialties = specialties,
                               window_images = self.window_images)
    
    def createDefaultScrollArea(self) -> scrollArea:
        """Function to create a scroll area.

        Returns:
            scrollArea: scrollArea that's generated for the module.
        """
         # Creating list of default images.
        images = []
        with open(f"{MODULE_PATH}\\{self.module_name}\\positions.json") as file:
            for position in json.load(file)["positions"]:
                images.append(obj.defaultImage(position))
        
        # Initialising new scroll area
        scroll_area = scrollArea(self.main_window,
                                 (683, 460),
                                 5)
        scroll_area.addItems(images,
                             initial = True)

        return scroll_area, images


class Images():
    def __init__(self,
                 main_window: QMainWindow) -> None:
        '''Images class containing and initialising all images for base.

        Attributes:
            side_panel [QLabel]: Side panel of the boxArt UI.
        '''
        self.__main_window = main_window
        
        self.side_panel = self.sidePanel()
        self.loading_animation = self.loadingAnimation()
    
    def sidePanel(self) -> QLabel:
        """Side panel function that creates a QLabel and assigns the panel image to it.

        Returns:
            QLabel: Created for the side panel.
        """
        label = QLabel(self.__main_window)
        pixmap = QPixmap.fromImage(PANEL_ASSETS.right_panel)

        label.setPixmap(pixmap)
        label.setGeometry(690, 108,
                          PANEL_ASSETS.right_panel.width(),
                          PANEL_ASSETS.right_panel.height())

        label.show()

        return label
    
    def loadingAnimation(self) -> QLabel:
        """Loading animation function that creates the loading animation that will be displayed when the mod is being generated.

        Returns:
            QLabel: Object of the label that's generated.
        """
        label = QLabel(self.__main_window)
        label.setFixedSize(52, 52)
        movie = QMovie(f"{PANEL_PATH}\\loading.gif")
        movie.setScaledSize(QSize(label.width(), label.height()))

        label.setMovie(movie)
        movie.start()

        label.setGeometry(715, 500, 52, 52)

        label.hide()

        return label

class Buttons():
    def __init__(self,
                 main_window: QMainWindow,
                 scroll_area: scrollArea,
                 module_name: str,
                 images: list,
                 specialties: bool,
                 window_images: Images) -> None:
        """Buttons class containing all the button objects created for the uploading function.

        Args:
            main_window (QMainWindow): Main Window generated from the PyQt6 main thread.
            scroll_area (scrollArea): Scroll Area created for the default uploading area.
            module_name (str): Name of the module the user clicked on.
            images (list): A list of images required for the buttons.
            specialties (bool): The specialties booleon if the module contains any special actions.
            window_images (Images): Images object of the images on the window.
        """
        # Creates private attributes
        self.__images = images
        self.__main_window = main_window
        self.__scroll_area = scroll_area
        self.__module_name = module_name
        self.__specialties = specialties
        self.__window_images = window_images

        # Creates open_images list for self.upload() to add to
        self.open_images = []

        # Creating button objects
        self.upload_button = self.uploadButton()
        self.start_button = self.startButton()
    
    def uploadButton(self) -> QPushButton:
        """UploadButton function used to create the upload button and handle its functions.

        Returns:
            QPushButton: Button created for uploading.
        """
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.upload.down)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.upload.up)))

        def func():
            """Main function called when the upload button is clicked."""
            files = QFileDialog.getOpenFileUrls(self.__main_window,
                                                "Open File",
                                                filter = "Image Files (*.png *.jpg)")

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
                    log.error(e)
                    # Add failed path to failed list
                    failed.append(path)
                    continue

                # Logging
                log.info(f"uploading {path} to {self.__module_name}")

                scroll_image = obj.scrollImages(path)

                x.append(scroll_image)
                self.open_images.append(scroll_image)

                # Replace the item in opened images assets
                self.__images[len(self.open_images) - 1] = obj.addingImage(path)

            if self.__maximum_replaced is True:
                # Logging
                log.info("Not all images added")
                
                error_message = QErrorMessage(self.__main_window)
                error_message.setWindowTitle("Maximum Images")
                error_message.showMessage(f"Only {opened_widgets} images can be used, the rest have been skipped.")
                error_message.exec()

                button.setDisabled(True)

            if failed != []:
                for fail in failed:
                    log.error(f"Corrupt Image: {fail}")

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
        opened_widgets = len(self.__images)

        button = QPushButton(self.__main_window)
        button.setText("")
        button.setGeometry(715, 150,
                           52, 52)

        button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.upload.up)))
        button.setIconSize(QSize(52, 52))

        button.pressed.connect(pressed)
        button.released.connect(released)
        button.clicked.connect(func)

        button.setStyleSheet("QPushButton {background-color: transparent; border: 0px}")
        button.show()

        return button
    
    def startButton(self) -> QPushButton:
        """Start Button function used to create the start button to create the mod.

        Returns:
            QPushButton: Button object created that's placed in the uploading window.
        """
        def pressed():
            '''
            Changes the button icon on press.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.start.down)))

        def released():
            '''
            Changes the button icon on release.
            '''
            button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.start.up)))
        
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
                # Removes unsafe characters from mod name
                dir_name = dialog.textValue()
                dir_name = "".join(c for c in dir_name if c.isalpha() or c.isdigit() or c==' ').rstrip()
                self.mod_name = dir_name

                # Logging
                log.info(f"Setting mod name: [{self.mod_name}]")
                getModLocation()
            else:
                return
            
        def getModLocation():
            '''
            Opens an input dialog for getting the location to where the mod is generated.
            '''
            while True:
                dialog = QInputDialog(self.__main_window)
                dialog.setWindowTitle("Input Save Location")
                dialog.setLabelText("Enter Save Location:")
                dialog.setInputMode(QInputDialog.InputMode.TextInput)
                
                clicked = dialog.exec()

                if clicked:
                    if not os.path.isdir(dialog.textValue()):
                        QMessageBox.warning(self.__main_window, "Invalid Input", f"{dialog.textValue()} is not a valid directory, please try again.")
                    else:
                        self.mod_save_path = dialog.textValue()

                        # Logging
                        log.info(f"Setting save path: [{self.mod_save_path}]")

                        func()
                        break
                else:
                    return

        def func():
            '''
            Starts the process of creating the mod with the given variables.
            '''
            self.thread = modGenerator(self.__images, self.__module_name, self.mod_name, self.mod_save_path, self.__specialties)
            self.thread.started.connect(HideWidgets)
            self.thread.finished.connect(ShowWidgets)

            self.thread.start()
   
        def HideWidgets():
            # Disables start and upload buttons.
            button.setDisabled(True)
            self.upload_button.setDisabled(True)

            # Show loading gif.
            self.__window_images.loading_animation.show()
        
        def ShowWidgets():
            # Disables start and upload buttons.
            button.setEnabled(True)
            self.upload_button.setEnabled(True)

            # Show loading gif.
            self.__window_images.loading_animation.hide()

        # Creating variables for save locations.
        self.mod_name = None
        self.mod_save_path = None

        # Creates the QPushbutton.
        button = QPushButton(self.__main_window)
        button.setText("")
        button.setGeometry(715, 225, 52, 52)

        # Sets the button's icon QPixmap to a given image in assets.
        button.setIcon(QIcon(QPixmap.fromImage(BUTTON_ASSETS.start.up)))
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

    def restartButton(self):
        pass

class modGenerator(QThread):
    def __init__(self,
                 images: list[object],
                 module_name: str,
                 mod_name: str,
                 save_location: str,
                 specialties: bool) -> None:
        '''Mod Generator function that will create the modded image, convert it to DDS and then create an INI image.
        
        Attributes:
            canvas [PIL.Image.Image]: Canvas image object of generated image.
            iniBytes [bytes]: Bytes of INI file.
            DDSLocation [str]: Location for where the DDS was saved.
            INILocation [str]: Location for where the INI was saved.
        '''
        super().__init__()

        self.__images = images
        self.__module_name = module_name
        self.__mod_name = mod_name
        self.__save_location = save_location
        self.__specialties = specialties
    
    def run(self):
        """Run function used to initiate the mod generator."""
        # Logging
        log.info(f"Generating [{self.__mod_name}]({self.__module_name}) -> {self.__save_location}")

        self.specialties = Specialties()
        if self.__specialties is True:
            self.special_method = getattr(self.specialties,
                                          self.__module_name)

        self.canvas, self.special_class = self.makeCanvas()

        self.mod_location = self.makeFolder()

        if self.__specialties is True:
            if self.special_class.converting is True:
                conversion_data = self.special_class.conversion()
            else:
                self.DDSLocation = self.convertToDDS(self.canvas)
        else:
            self.DDSLocation = self.convertToDDS(self.canvas)

        if self.__specialties is True:
            if self.special_class.ini is True:
                self.special_class.INI(conversion_data,
                                       self.__mod_name)
            else:
                self.INILocation = self.saveINI()
        else:
            self.INILocation = self.saveINI()

    def makeCanvas(self) -> Image.Image:
        """Function to create the canvas image that will be used for the generator.

        Returns:
            Image.Image: PIL.Image object returned for the canvas.
        """
        canvas_data = obj.Canvas(self.__module_name,
                                 self.__images)
        canvas = canvas_data.background

        # If the mod contains anything that is out of the ordinary, this will call it from Specialties.
        if self.__specialties is True:
            special = self.special_method(canvas,
                                          canvas_data,
                                          f"{self.__save_location}\\{self.__mod_name}",
                                          self.__module_name)
            if special.starting is True:
                canvas = special.start()
                
        for image in canvas_data.images:
            res_image = image.image.resize((image.width,
                                            image.height),
                                            Image.Resampling.LANCZOS)
            rot_image = res_image.rotate(image.rotation,
                                         expand = True)
        
            canvas.paste(rot_image, (image.x, image.y))

        if self.__specialties is True:
            special = self.special_method(canvas,
                                          canvas_data,
                                          f"{self.__save_location}\\{self.__mod_name}",
                                          self.__module_name)
            if special.ending is True:
                canvas = special.end()

            return canvas, special
        
        return canvas, False
    
    def makeFolder(self) -> str:
        """Function for creating the directory where the user wants to put the mod.

        Returns:
            str: The save path of where the user selected.
        """
        mod_path = f"{self.__save_location}\\{self.__mod_name}"

        if not os.path.exists(mod_path):
            os.makedirs(mod_path)
            log.info(f"Created: {mod_path}")
        else:
            log.error(f"{mod_path} | Already Exists")

        return mod_path

    def convertToDDS(self, canvas: Image.Image) -> str:
        """Function to convert a PIL.Image object into a DDS file.

        Args:
            canvas (Image.Image): Canvas that is created by the makeCanvas function.

        Returns:
            str: The DDS save location string.
        """

        canvas = ImageOps.flip(canvas)
        canvas = canvas.convert("RGBA")

        output_path = f"{self.__save_location}\\{self.__mod_name}\\{self.__module_name}.dds"

        imageio.imwrite(output_path,
                        canvas,
                        format = "dds")

        return output_path

    def saveINI(self) -> str:
        """SaveINI function that will generate an INI file towards a location.

        Returns:
            str: The lines used when saving the INI file.
        """
        def getHash() -> str:
            """Get Hash function to return the hash string from data.json.

            Returns:
                str: The hash required for the INI.
            """
            with open(f"{MODULE_PATH}\\{self.__module_name}\\data.json") as file:
                return json.load(file)["hash"]

        file_path = f"{self.mod_location}\\{self.__mod_name}"

        lines = (
            "; Overrides\n"
            f"[TextureOverride{self.__module_name}]\n"
            f"hash = {getHash()}\n"
            f"this = Resource{self.__module_name}\n\n"
            f"; Resources\n"
            f"[Resource{self.__module_name}]\n"
            f"filename = {self.__module_name}.dds\n\n"
            f"; ShaderOverride\n"
            f"[ShaderOverride {self.__module_name} Shader]\n"
            f"hash = 47a121208fd878ad\n"
            f"allow_duplicate_hash = true\n"
            f"checktextureoverride = ps-t1\n\n"
            f"; Mod Generated By N4GR\n"
            f"; https://github.com/Vamptek\n"
            f"; https://github.com/Vamptek/ZZZ-Mod-Generator"
        )

        with open(f"{file_path}.ini", "w+") as file:
            file.writelines(lines)
        
        return lines
