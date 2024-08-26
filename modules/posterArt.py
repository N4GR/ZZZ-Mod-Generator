from imports import *
log = setup("POSTER ART")

from modules import uploading

class posterArt():
    def __init__(self,
                 main_window: QMainWindow) -> None:
        """Poster Art module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        base = uploading.uploading(main_window,
                                   "posterArt")