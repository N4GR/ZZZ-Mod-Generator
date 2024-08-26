from imports import *
log = setup("AGENT ICONS")

from modules import uploading

class agentIcons:
    def __init__(self,
                 main_window: QMainWindow) -> None:
        base = uploading.uploading(main_window,
                                   "agentIcons",
                                   specialties = True)