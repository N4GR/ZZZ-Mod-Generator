import os
ASSET_PATH = f"{os.getcwd()}\\assets"

import sqlite3
import io
class getImages():
    def __init__(self) -> None:
        '''Creates a dictionary of dictionaries containing image data.

        Attributes:
            images: list of image data
        '''
        self.connection = sqlite3.connect(f"{ASSET_PATH}\\data.sqlite")
        self.cursor = self.connection.cursor()

        self.images = self.makeImages()
        '''list: a list of image data
        
        Attributes:
            image:      bytes image\n
            category:   str category
            type:       str file type
            height:     int image height
            width:      int image width
            bytes:      int image bytes size
        '''

        self.connection.close()

    def makeImages(self):
        images = self.cursor.execute("SELECT * FROM images").fetchall()

        x = {}

        for image in images:
            x[image[1]] = {
                "image": image[2],
                "category": image[3],
                "type": image[4],
                "height": image[5],
                "width": image[6],
                "bytes": image[7]
            }
        
        return x

img = getImages().images

class assetConfig:
    def __init__(self) -> None:
        # Buttons
        self.buttons = buttons()

        # Images
        self.images = images()

        # Fonts
        self.fonts = fonts()

from PIL import Image
from PIL.ImageQt import ImageQt
### BUTTONS
class buttons:
    def __init__(self) -> None:
        self.exit = exit()
        self.minimise = minimise()

class exit:
    def __init__(self) -> None:
        self.up = image(img["exit_up"]["image"])
        self.down = image(img["exit_down"]["image"])

class minimise:
    def __init__(self) -> None:
        self.up = image(img["minimise_up"]["image"])
        self.down = image(img["minimise_down"]["image"])

### IMAGES
class images:
    def __init__(self) -> None:
        self.background = image(img["background"]["image"])
        self.icon = image(img["icon"]["image"])

class image:
    def __init__(self, image_bytes: bytes) -> None:
        self.bytes = image_bytes
        self.image = ImageQt(Image.open(io.BytesIO(image_bytes)))

### FONTS
class fonts:
    def __init__(self) -> None:
        self.inpin = f"{ASSET_PATH}\\inpin.ttf"