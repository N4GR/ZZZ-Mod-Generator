from imports import *
log = setup("PROFILE ICONS")

from modules import uploading

class profileIcons:
    def __init__(self,
                 main_window: QMainWindow) -> None:
        """Profile Icons module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        base = uploading.uploading(main_window,
                                   "profileIcons",
                                   specialties = True)