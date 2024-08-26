from imports import *
log = setup("BATTLE ICONS")

from modules import uploading

class battleIcons:
    def __init__(self,
                 main_window: QMainWindow) -> None:
        """Battle Icons module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        base = uploading.uploading(main_window,
                                   "battleIcons",
                                   specialties = True)