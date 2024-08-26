from imports import *
log = setup("AGENT ICONS")

from modules import uploading

class agentIcons:
    def __init__(self,
                 main_window: QMainWindow) -> None:
        """Agent Icons module function.

        Args:
            main_window (QMainWindow): QMainWindow object generated from the main PyQt6 window.
        """
        base = uploading.uploading(main_window,
                                   "agentIcons",
                                   specialties = True)