from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize

from PIL.ImageQt import ImageQt
from PIL import Image

import io

class N4QToolButton(QToolButton):
    def __init__(self, button_name: str, button_icon: bytes) -> None:
        super(N4QToolButton, self).__init__()

        font = QFont("inpin", 12)

        self.setFont(font)
        self.setText(button_name)
        self.setFixedSize(150, 200)
        self.setIcon(QIcon(QPixmap.fromImage(ImageQt(Image.open(io.BytesIO(button_icon))))))
        self.setIconSize(QSize(124, 124))
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 0px;
            }
        """)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

class Module():
    def __init__(self, module_dict: dict) -> None:
        '''
        Object constructur for the module dictionary.

        Attributes:
            name:           str name of module\n
            function_name:  str name of function
            thumbnail:      bytes image of thumbnail
            description:    str description of module
            data:           any data for module to use
        '''
        self.name = module_dict["name"]
        self.function_name = module_dict["function_name"]
        self.thumbnail = module_dict["thumbnail"]
        self.description = module_dict["description"]
        self.data = module_dict["data"]

