import sqlite3

class modulesConfig():
    def __init__(self) -> None:
        '''Creates a list of module objects

        Attributes:
            list: A list of module objects.
        '''
        self.list = self.getModules()
        """list: list of module objects
        
        Attributes:
            type:           str type of object\n
            name:           str name of module
            function_name:  str name of function
            thumbnail:      bytes image of thumbnail
            description:    str description of module
            data:           any data for module to use
        """

    def getModules(self):
        self.connection = sqlite3.connect("config\\data.sqlite")
        self.cursor = self.connection.cursor()

        modules = self.cursor.execute("SELECT * FROM modules").fetchall()
        self.connection.close()

        mods = []

        for module in modules:
            mods.append(moduleObject(module))
        
        return mods

class moduleObject():
    def __init__(self, module) -> None:
        '''
        Object constructur for the module dictionary.

        Attributes:
            name:           str name of module\n
            function_name:  str name of function
            thumbnail:      bytes image of thumbnail
            description:    str description of module
            data:           any data for module to use
        '''
        self.type = "module"
        self.name =  module[1]
        self.function_name = module[2]
        self.thumbnail = module[3]
        self.description = module[4]
        self.data = module[5]


from PyQt6.QtWidgets import QMainWindow

import modules.boxArt
import modules.posterArt
import modules.magazineArt
class moduleFunctions:
    def boxArt(main_window: QMainWindow):
        modules.boxArt.boxArt(main_window)
    
    def posterArt(main_window: QMainWindow):
        modules.posterArt.posterArt(main_window)
    
    def magazineArt(main_window: QMainWindow):
        modules.magazineArt.magazineArt(main_window)