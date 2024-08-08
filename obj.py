from PyQt6.QtGui import QPixmap, QIcon

from PIL.ImageQt import ImageQt
from PIL import Image

import io

class image():
    def __init__(self, data: dict) -> None:
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
    def __init__(self, up: dict, down: dict) -> None:
        self.up = image(up)
        self.down = image(down)

class scrollImages():
    def __init__(self, path: str) -> None:
        x = path.split("/")[-1].split(".")

        self.path = path        
        self.name = x[0]
        self.type = "image"#
        self.file_type = x[1]