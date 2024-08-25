from imports import *

from modules.base import uploading

class posterArt():
    def __init__(self, main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window, "posterArt")

        print(base.buttons.open_images)

        print("posterArt")