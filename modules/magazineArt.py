from imports import *
log = setup("MAGAZINE ART")

from modules import uploading

class magazineArt:
    def __init__(self, main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window, "magazineArt")