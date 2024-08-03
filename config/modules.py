import sqlite3

class getModules():
    def __init__(self) -> None:
        '''Creates a dictionary of dictionaries containing image data.

        Attributes:
            images: list of image data
        '''
        self.connection = sqlite3.connect("config\\data.sqlite")
        self.cursor = self.connection.cursor()

        self.modules = self.makeModules()
        '''list: a list of image data
        
        Attributes:
            name:           str name of module\n
            function_name:  str name of function
            thumbnail:      bytes image of thumbnail
            description:    str description of module
        '''

        self.connection.close()

    def makeModules(self):
        modules = self.cursor.execute("SELECT * FROM modules").fetchall()

        x = []

        for module in modules:
            x.append({
                "name": module[1],
                "function_name": module[2],
                "thumbnail": module[3],
                "description": module[4]
            })
        
        return x

class modulesConfig():
    def __init__(self) -> None:
        '''Creates a list of module dictionaries

        Attributes:
            list: A list of module dictionaries.
        '''
        self.list = getModules().modules
        """list: list of module objects
        
        Attributes:
            name:           str name of module\n
            function_name:  str name of function
            thumbnail:      bytes image of thumbnail
            description:    str description of module
        """

from PyQt6.QtWidgets import QMainWindow

import modules.boxArt
class moduleFunctions:
    def boxArt(main_window: QMainWindow):
        modules.boxArt.boxArt(main_window)