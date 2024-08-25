from imports import *
log = setup("MODULE")

# Local imports
from config.paths import *
import modules.agentIcons
import modules.agentIcons.init

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
        log.info("Box Art")
        modules.boxArt.init.boxArt(main_window)
    
    def posterArt(main_window: QMainWindow):
        log.info(moduleFunctions.posterArt.__name__)
        modules.posterArt.init.posterArt(main_window)
    
    def magazineArt(main_window: QMainWindow):
        log.info("Magazine Art")
        modules.magazineArt.init.magazineArt(main_window)
    
    def agentIcons(main_window: QMainWindow):
        log.info("Agent Icons")
        modules.agentIcons.init.agentIcons(main_window)