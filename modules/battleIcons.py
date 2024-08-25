from imports import *
log = setup("BATTLE ICONS")

from modules import uploading

class battleIcons:
    def __init__(self, main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window, "battleIcons", specialties = True)