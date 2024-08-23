from imports import *

from modules.base import uploading

class magazineArt:
    def __init__(self, main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window, "magazineArt")

        print("magazineArt")