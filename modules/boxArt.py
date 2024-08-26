from imports import *
log = setup("BOX ART")

from modules import uploading

class boxArt:
    def __init__(self,
                 main_window: QMainWindow) -> None:
        """Box Art module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        base = uploading.uploading(main_window,
                                   "boxArt",
                                   specialties = True)