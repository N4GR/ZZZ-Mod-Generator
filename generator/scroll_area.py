from imports import *
log = setup("SCROLL AREA")

# Local imports
import config.module

class N4QToolButton(QToolButton):
    def __init__(self,
                 button_name: str,
                 button_icon: ImageQt) -> None:
        super(N4QToolButton, self).__init__()

        font = QFont("inpin", 12)

        self.setFont(font)
        self.setText(button_name)
        self.setFixedSize(150, 200)
        self.setIcon(QIcon(QPixmap.fromImage(button_icon)))
        self.setIconSize(QSize(124, 124))
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 0px;
            }
        """)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

class N4QImageWithText(QWidget):
    def __init__(self,
                 text: str,
                 type: str,
                 image_path: str = None,
                 img: object = None) -> None:
        '''QWidget object containing an image QLabel and a text QLabel positioned in a QVBoxLayout for text below images.
        
        Paramteres:
            text [str]: Text to be used under the image. "Hello!"
            type [str]: Type of item being added to the scroll area. "module"
            image_path [str] = None: Path to the image if type = "image". "this\\path\\hello.png"
            img [object] = None: Image.Image object if type is not "image".
        '''
        super(N4QImageWithText, self).__init__()
        width, height = (100, 150)

        # Creating image label
        if type == "image":
            img = Image.open(image_path)
            img = img.convert("RGBA")

        img.thumbnail((width, height), Image.Resampling.LANCZOS)

        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt(img)))
        self.image_label.setFixedSize(width, height)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #img.close()

        # Creating text label
        if len(text) > 13: text = f"{text[:11]}..."
        self.text_label = QLabel(self)
        font = QFont("inpin", 12)
        self.text_label.setFont(font)
        self.text_label.setText(text)
        self.text_label.setFixedWidth(width)

        if type == "default": self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Creating layout to add the widgets to
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

class scrollArea():
    def __init__(self,
                 main_window: QMainWindow,
                 size: tuple[int] = (790, 460),
                 max_column: int = 4) -> None:
        '''scrollArea class generator for creating scrollable areas within the main UI.

        Parameters:
            main_window [QMainWindow]: The main window of the root application.
            size [tuple[int]] = (790, 460): Size of the scroll area (width, height). (100, 100)
            max_column [int] = 4: Max number of columns to use when adding to scroll area. 5

        Attributes:
            scroll_area [QScrollArea]: The scroll area being generated.
            grid_layout [QGridLayout]: The grid layout being used inside the scroll area.
            row [int]: The current row the scroll area is on. 6
            column [int]: The current column the scroll area is on. 7
        '''
        self.main_window = main_window

        # Create a scroll area
        self.scroll_area = QScrollArea(main_window)

        # Create a widget to hold the grid layout
        container = QWidget()
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        # Create a grid layout
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setSpacing(5)

        # Set up the container widget
        container.setLayout(self.grid_layout)
        
        self.scroll_area.resize(size[0], size[1])
        self.scroll_area.move(5, 110)

        self.scroll_area.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.scroll_area.setStyleSheet("background-color: transparent; border: 0px")

        self.scroll_area.show()

        # Initialising addItems requirements.
        self.row = 0
        self.column = 0

        self.max_column = max_column

    def addItems(self,
                 items: list[object],
                 initial: bool = False):
        '''Function to add items to a scroll area.
        
        Parameters:
            items [list[object]]: A list of objects that contains different things depending on item.type
            initial [bool] = False: An indicator for uploading.py to reset column and row back to 0 if it's initiating default images.
        '''
        def getFunc(function_name: str):
            '''Basic function to return a function by a string.

            Return:
                function: function found from config.module.moduleFunctions from function_name string.
            '''
            return getattr(config.module.moduleFunctions, function_name)

        def makeLambda(func):
            '''Basic function to return a lambda for buttons
            
            Return:
                lambda func(self.main_menu)
            '''
            return lambda: func(self.main_window)

        for item in items:
            # Column will rise up to 4 then reset to 1
            # When column reached 4, row increases to next line.
            if self.column == self.max_column:
                self.column = 1
                self.row += 1
            else: self.column += 1

            # Adds module type to scroll area
            if item.type == "module":
                # Logging
                log.info(f"adding {item.name} to scroll area.")

                func = getFunc(item.function_name)
                widget = N4QToolButton(item.name,
                                       item.thumbnail)
                widget.clicked.connect(makeLambda(func))
                widget.clicked.connect(self.delete)

            # Adds image type to scroll area
            if item.type == "image":
                # Logging
                log.info(f"adding {item.name} to scroll area.")

                widget = N4QImageWithText(text = f"{item.name}.{item.file_type}",
                                          type = "image",
                                          image_path = item.path)

            # Adds default type to scroll area when uploading.py is called
            if item.type == "default":
                # Logging
                log.info(f"adding {item.name} to scroll area.")
                
                widget = N4QImageWithText(text = f"{item.name}",
                                          type = "default",
                                          img = item.image)

            # Checks if there is any item there, deletes it if it is.
            remove_widget = self.grid_layout.itemAtPosition(self.row,
                                                            self.column)

            if remove_widget is not None:
                remove_widget = remove_widget.widget()

                # Removes widget from grid
                self.grid_layout.removeWidget(remove_widget)
                # Completely destroys widget object
                remove_widget.deleteLater()

            # Adds item to the given position
            self.grid_layout.addWidget(widget,
                                       self.row,
                                       self.column)

        if initial is True:
            self.column = 0
            self.row = 0
    
    def delete(self):
        self.scroll_area.setParent(None)