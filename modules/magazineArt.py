from imports import *
log = setup("MAGAZINE ART")

from modules import uploading

class magazineArt:
    def __init__(self,
                 main_window: QMainWindow) -> None:
        """Magazine Art module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        base = uploading.uploading(main_window,
                                   "magazineArt")