from imports import *
log = setup("CHAIN ICONS")

from modules import uploading

class chainIcons:
    def __init__(self, main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window, "chainIcons", specialties = True)