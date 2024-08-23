from PIL import Image, ImageDraw, ImageFont

import json

from config.paths import *
from config.assets import font

class image():
    def __init__(
            self,
            data: dict) -> None:
        
        '''Image creation class, give an image from database to create object.

        Attributes:
            name [str]: Name of image.
            bytes [bytes]: Bytes object of image.
            category [str]: Image category.
            type [str]: File type of image.
            height [int]: Height of image.
            width [int]: Width of image.
            size [int]: Size of image in bytes.
            thumbnail [QIcon]: QIcon of a 64x64 thumbnailed version of the image.
        '''
        self.__data = data[0]

        self.name = self.__data[1] 
        self.bytes = self.__data[2]
        self.category = self.__data[3]
        self.type = self.__data[4]
        self.height = self.__data[5]
        self.width = self.__data[6]
        self.size = self.__data[7]

class button():
    def __init__(
            self,
            up: dict,
            down: dict) -> None:
        
        self.up = image(up)
        self.down = image(down)

class scrollImages():
    def __init__(
            self,
            path: str) -> None:
        
        x = path.split("/")[-1].split(".")

        self.path = path        
        self.name = x[0]
        self.type = "image"
        self.file_type = x[1]

class addingImage():
    def __init__(
            self,
            path: str) -> None:
        
        x = path.split("/")[-1].split(".")

        self.image = Image.open(path)
        self.name = x[0]
        self.file_type = x[1]
        self.type = "default"

class defaultImage():
    def __init__(
            self,
            data: dict) -> None:
        """DefaultImage creation class that generates an image.

        Args:
            data (dict):    Data to be passed to the default image. {image_width, image_height}

        Attributes:
            image (Image):  Image automatically created with centered text.
            name (str):     Name of the image. "Poster #1"
            type (str):     Type of Image. "default"
        """
        self.__data = data

        self.image = self.makeImage()
        self.name = self.__data["name"]
        self.type = "default"

    def makeImage(self) -> Image:
        """Creates a default image with text in the centre.

        Returns:
            Image: The image that has been created.
        """
        width, height = (self.__data["image_width"],
                         self.__data["image_height"])
            
        # Creating image canvas
        image = Image.new("RGBA",
                          (width, height),
                          color = (0, 0, 0))

        # Creating image draw
        draw = ImageDraw.Draw(image)

        # Adding text
        text = self.__data["name"]

        font_size = 20
        margin = 20

        text_color = (255, 255, 255)
        text_font = ImageFont.truetype(font().inpin,
                                       font_size)

        # Adjusting image to fill image width with a pixel margin.
        while True:
            bbox = draw.textbbox((0, 0),
                                 text,
                                 font = text_font)
            
            text_width = bbox[2] - bbox[0]

            if text_width + margin * 2 > width:
                break

            font_size += 1
            text_font = ImageFont.truetype(font().inpin,
                                           font_size)

        # Calculate text size and position using textbbox
        text_bbox = draw.textbbox((0, 0),
                                  text,
                                  font = text_font)
        
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2

        # Draw the text
        draw.text((text_x, text_y),
                  text,
                  fill = text_color,
                  font = text_font)

        return image
    
class Canvas():
    def __init__(
            self,
            module_name: str,
            image_asset_data: list) -> None:
        
        self.__module_name = module_name
        self.__image_asset_data = image_asset_data
        
        data = self.getData()
        canvas_size = data["canvas_size"] # {'height': 1024, 'width': 1024}
        self.__positions = data["positions"] # [{'name': 'image1', 'image_x': 0, 'image_y': 0, 'image_width': 104, 'image_height': 178, 'rotation': 0}]

        self.height = canvas_size["height"]
        self.width = canvas_size["width"]

        self.background = Image.open(f"{MODULE_PATH}\\{self.__module_name}\\background.png")

        # Creates a list of CanvasImage objects which contains an Image.Image object and attributes from modules.data in database.
        self.images = [CanvasImage(self.__image_asset_data[x],
                                   self.__positions[x]) for x in range(len(self.__image_asset_data))]

    def getData(self) -> dict:
        '''A function to return a dictionary of data from the modules directory with a given module name.
        
        Returns:
            dict["canvas_size", "positions"]
        '''
        with open(f"{MODULE_PATH}\\{self.__module_name}\\positions.json") as file:
            return json.load(file)
    
class CanvasImage():
    def __init__(
            self,
            image: defaultImage | addingImage,
            position: dict) -> None:
        '''CanvasImage object which contains information needed to generate a usable canvas.
        
        Attributes:
            self.image [PIL.Image.Image]
        '''
        self.image = image.image
        
        self.name = position["name"]
        self.x = position["image_x"]
        self.y = position["image_y"]
        self.width = position["image_width"]
        self.height = position["image_height"]
        self.rotation = position["rotation"]