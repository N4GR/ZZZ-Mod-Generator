import json
import os
from PIL import Image
import math

class JSON:
    def __init__(self,
                 amount: int,
                 columns: int) -> None:
        """Class to create the positions.json for modules.
        Only requires one image of equal size to the others to operate.

        Args:
            amount (int): The amount of images you'd like to add to the JSON.
        """
        self.data_dir = "generator\\data"
        self.image_dir = f"{self.data_dir}\\{os.listdir(self.data_dir)[0]}"

        self.template = {
            "canvas_side": {},
            "positions": []
        }

        image = Image.open(self.image_dir)

        x = 0
        y = 0
        max_width = image.width * columns
        self.positions = []
        for z in range(amount):
            self.positions.append({
                "name": "BLANK",
                "image_x": x,
                "image_y": y,
                "image_width": image.width,
                "image_height": image.height,
                "rotation": 0
            })
            
            # X = columns in one row
            # Y = Every column item, go down one.
            x += image.width
            if x % max_width == 0:
                x = 0
                y += image.height
        
        self.data = {
            "canvas_size": {
                "height": image.height * math.ceil(amount / columns),
                "width": image.width * columns
            },
            "positions": self.positions
        }
    
    def Create(self,
               data: str):
        with open(f"{self.data_dir}\\positions.json", "w") as file:
            json.dump(data, file, indent = 4)