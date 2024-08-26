from imports import *
log = setup("ASSETS")

# Local imports
from config.paths import *

class button(object):
    def __init__(self) -> None:
        self.exit = self.ToggleButton("exit")
        self.minimise = self.ToggleButton("minimise")
        self.start = self.ToggleButton("start")
        self.upload = self.ToggleButton("upload")

    class ToggleButton(object):
        def __init__(self,
                     name: str) -> None:
            self.up = self.openImage(name,
                                     "up")
            self.down = self.openImage(name,
                                       "down")
        
        def openImage(self,
                      name: str,
                      type: str) -> ImageQt:
            return ImageQt(Image.open(f"{BUTTON_PATH}\\{name}_{type}.png"))

class panel(object):
    def __init__(self) -> None:
        self.background = self.openImage("background")
        self.icon = self.openImage("icon")
        self.right_panel = self.openImage("right_panel")
    
    def openImage(self,
                  name: str) -> Image.Image:
        return ImageQt(Image.open(f"{PANEL_PATH}\\{name}.png"))

class font(object):
    def __init__(self) -> None:
        self.inpin = f"{FONT_PATH}\\inpin.ttf"