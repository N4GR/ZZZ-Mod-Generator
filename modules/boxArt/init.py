from imports import *

from modules.base import uploading

class boxArt():
    def __init__(self, main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window, "boxArt", specialties = True)

        print("boxArt")