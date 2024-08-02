import os
ASSET_PATH = f"{os.getcwd()}\\assets"

class assetConfig:
    def __init__(self) -> None:
        # Buttons
        self.buttons = buttons()

        # Images
        self.images = images()

        # Fonts
        self.fonts = fonts()

### BUTTONS
class buttons:
    def __init__(self) -> None:
        self.exit = exit()
        self.minimise = minimise()

class exit:
    def __init__(self) -> None:
        self.up = f"{ASSET_PATH}\\buttons\\exit_up.png"
        self.down = f"{ASSET_PATH}\\buttons\\exit_down.png"

class minimise:
    def __init__(self) -> None:
        self.up = f"{ASSET_PATH}\\buttons\\minimise_up.png"
        self.down = f"{ASSET_PATH}\\buttons\\minimise_down.png"

### IMAGES
class images:
    def __init__(self) -> None:
        self.background = f"{ASSET_PATH}\\images\\background.png"
        self.icon = f"{ASSET_PATH}\\images\\icon.png"

### FONTS
class fonts:
    def __init__(self) -> None:
        self.inpin = f"{ASSET_PATH}\\fonts\\inpin.ttf"