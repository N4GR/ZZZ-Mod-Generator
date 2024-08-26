from datetime import datetime
import logging
import sys

class Logger:
    def __init__(self,
                 class_name: str) -> None:
        now = datetime.now()
        current_datetime = now.strftime("%d-%m-%Y_%H-%M-%S")

        # Suppress debug logging from PIL
        logging.getLogger('PIL').setLevel(logging.WARNING)

        self.log = logging.getLogger(class_name)

        logging.basicConfig(
            level = logging.DEBUG,
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers = [
                logging.FileHandler(f"logs\\{current_datetime}.log"),
                logging.StreamHandler()
            ]
        )
    
    def custom_excepthook(self,
                          exc_type,
                          exc_value,
                          exc_traceback):
        if issubclass(exc_type,
                      KeyboardInterrupt):
            # Allow the program to terminate on a keyboard interrupt
            sys.__excepthook__(exc_type,
                               exc_value,
                               exc_traceback)
            return
        logging.error("Uncaught exception",
                      exc_info = (exc_type,
                                  exc_value,
                                  exc_traceback))