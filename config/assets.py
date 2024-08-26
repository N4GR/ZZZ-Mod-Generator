from imports import *
log = setup("ASSETS")

# Local imports
from config.paths import *

class button(object):
    def __init__(self) -> None:
        """Button object containing ToggleButtons."""
        self.exit = self.ToggleButton("exit")
        self.minimise = self.ToggleButton("minimise")
        self.start = self.ToggleButton("start")
        self.upload = self.ToggleButton("upload")

    class ToggleButton(object):
        def __init__(self,
                     name: str) -> None:
            """Togglebutton.

            Args:
                name (str): Name of the button.
            """
            self.up = self.openImage(name, "up")
            self.down = self.openImage(name, "down")
        
        def openImage(self,
                      name: str,
                      type: str) -> ImageQt:
            """openImage function to create an ImageQt object for the button.

            Args:
                name (str): Name of the button to open.
                type (str): Type of button to open. up | down

            Returns:
                ImageQt: ImageQt object for PyQt6
            """
            return ImageQt(Image.open(f"{BUTTON_PATH}\\{name}_{type}.png"))

class panel(object):
    def __init__(self) -> None:
        """Panel object to open panel images."""
        self.background = self.openImage("background")
        self.icon = self.openImage("icon")
        self.right_panel = self.openImage("right_panel")
    
    def openImage(self,
                  name: str) -> ImageQt:
        """openImage function for Panels, which opens images with a given name.

        Args:
            name (str): Name of the panel image to open.

        Returns:
            Image.Image: ImageQt object for PyQt6. 
        """
        return ImageQt(Image.open(f"{PANEL_PATH}\\{name}.png"))

class font(object):
    def __init__(self) -> None:
        """Fonts object containing all available fonts."""
        self.inpin = f"{FONT_PATH}\\inpin.ttf"