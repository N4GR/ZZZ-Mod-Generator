import os
import json

from config.paths import *

from PIL.ImageQt import ImageQt
from PIL import Image

class module():
    def __init__(self) -> None:
        module_directories = os.listdir(MODULE_PATH)

        self.list = []
        for path in module_directories:
            self.list.append(self.moduleObject(f"{MODULE_PATH}\\{path}"))

    class moduleObject():
        def __init__(self, path: str) -> None:
            '''
            Object constructur for the module dictionary.

            Attributes:
                name:           str name of module\n
                function_name:  str name of function
                thumbnail:      bytes image of thumbnail
                description:    str description of module
                data:           any data for module to use
            '''
            with open(f"{path}\\data.json") as file:
                data = json.load(file)

            self.type = "module"
            self.name =  data["name"]
            self.function_name = data["function_name"]
            self.thumbnail = ImageQt(Image.open(f"{path}\\thumbnail.png"))

from PyQt6.QtWidgets import QMainWindow

import modules.boxArt.init
import modules.posterArt.init
import modules.magazineArt.init
class moduleFunctions:
    def boxArt(main_window: QMainWindow):
        modules.boxArt.init.boxArt(main_window)
    
    def posterArt(main_window: QMainWindow):
        modules.posterArt.init.posterArt(main_window)
    
    def magazineArt(main_window: QMainWindow):
        modules.magazineArt.init.magazineArt(main_window)