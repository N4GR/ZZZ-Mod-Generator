import sqlite3
import pickle

class sql():
    def __init__(self) -> None:
        '''SQL Class to obtain data from the database.'''
        self.__connection = sqlite3.connect("config\\data.sqlite")
        self.__cursor = self.__connection.cursor()
    
    def close(self):
        '''SQL close function to close and commit the connection to the database.'''
        self.__connection.commit()
        self.__connection.close()
    
    def get(self, table: str, query: str = None) -> list[tuple]:
        '''SQL get function to retrieve data from a table within the database
        
        Parameters:
            table [str]: Name of the table to get the data from.
            query [str] = None: Query to be used to obtain the data.

        Usage:
            get("images", "name = test")
        
        Returns:
            list[tuple]: Data requested.
        '''
        if query is None:
            sql_insert = f"SELECT * FROM {table}"
        else:
            sql_insert = f"SELECT * FROM {table} WHERE {query}"

        fetch = self.__cursor.execute(sql_insert)
        
        return fetch.fetchall()

class __SQL():
    def __init__(self) -> None:
        '''SQL Class to obtain data from the database.'''
        self.__connection = sqlite3.connect("config\\data.sqlite")
        self.__cursor = self.__connection.cursor()
    
    def close(self):
        '''SQL close function to close and commit the connection to the database.'''
        self.__connection.commit()
        self.__connection.close()
    
    def addImage(self, image_directory: str, category: str):
        img = image(image_directory)

        query = """ INSERT INTO images
                                    (name, image, category, type, height, width, bytes) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        data_tuple = (img.name, img.bytes, category, img.type, img.height, img.width, img.size)

        self.__cursor.execute(query, data_tuple)

        self.close()

from PIL import Image
import os
class image():
    def __init__(self, image_directory: str) -> None:
        self.__image_directory = image_directory
        image_info = self.__ImageINFO()
        split = image_directory.split("\\")[-1].split(".")

        self.bytes = self.__getIO()
        self.name = split[0] # First item in name . png split
        self.type = split[1] # Second item, file type.
        self.height = image_info.height
        self.width = image_info.width
        self.size = os.path.getsize(self.__image_directory)


    def __getIO(self) -> bytes:
        with open(self.__image_directory, "rb") as file:
            blobData = file.read()
            
        return blobData
    
    def __ImageINFO(self) -> Image.Image:
        return Image.open(self.__image_directory)