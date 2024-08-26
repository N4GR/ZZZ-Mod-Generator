from imports import *
log = setup("MODULE")

# Local imports
from config.paths import *

class module():
    def __init__(self) -> None:
        """Module class which contains a list of module objects."""
        module_directories = os.listdir(MODULE_PATH)

        self.list = []
        for path in module_directories:
            self.list.append(self.moduleObject(f"{MODULE_PATH}\\{path}"))

    class moduleObject():
        def __init__(self,
                     path: str) -> None:
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

import modules.boxArt
import modules.posterArt
import modules.magazineArt
import modules.agentIcons
import modules.battleIcons
import modules.chainIcons
class moduleFunctions:
    def boxArt(main_window: QMainWindow):
        """Box Art module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        log.info("Box Art")
        modules.boxArt.boxArt(main_window)
    
    def posterArt(main_window: QMainWindow):
        """Poster Art module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        log.info(moduleFunctions.posterArt.__name__)
        modules.posterArt.posterArt(main_window)
    
    def magazineArt(main_window: QMainWindow):
        """Magazine Art module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        log.info("Magazine Art")
        modules.magazineArt.magazineArt(main_window)
    
    def agentIcons(main_window: QMainWindow):
        """Agent Icons module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        log.info("Agent Icons")
        modules.agentIcons.agentIcons(main_window)
    
    def battleIcons(main_window: QMainWindow):
        """Battle Icons module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        log.info("Battle Icons")
        modules.battleIcons.battleIcons(main_window)

    def chainIcons(main_window: QMainWindow):
        """Chain Icons module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        log.info("Chain Icons")
        modules.chainIcons.chainIcons(main_window)