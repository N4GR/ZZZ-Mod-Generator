from sql import sql
import obj
import ast

from PIL import Image, ImageDraw, ImageFont

### IMAGES
class images:
    def __init__(self, module_name: str) -> None:
        self.__sq = sql()
        self.__module_name = module_name

        self.side_panel = obj.image(self.__sq.get("images", "name = 'side_panel'"))
        self.upload_button = obj.button(up = self.__sq.get("images", "name = 'upload_up'"), down = self.__sq.get("images", "name = 'upload_down'"))

        self.data = self.__makeImages()

        self.__sq.close()
    
    def __makeImages(self):
        data_list = ast.literal_eval(self.__sq.get("modules", f"name = '{self.__module_name}'")[0][5])["positions"]

        default_image_objects = []

        for data in data_list:
            default_image_objects.append(obj.defaultImage(data))
        
        
        return default_image_objects