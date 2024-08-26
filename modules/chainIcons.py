from imports import *
log = setup("CHAIN ICONS")

from modules import uploading

class chainIcons:
    def __init__(self,
                 main_window: QMainWindow) -> None:
        """Chain Icons module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        base = uploading.uploading(main_window,
                                   "chainIcons",
                                   specialties = True)