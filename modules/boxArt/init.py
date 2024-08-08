from PyQt6.QtWidgets import QMainWindow

from modules.base import uploading

class boxArt():
    def __init__(self, main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window)

        print("boxArt")