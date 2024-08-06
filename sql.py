import sqlite3

class sql():
    def __init__(self) -> None:
        '''SQL Class to obtain data from the database.'''
        self.__connection = sqlite3.connect("config\\data.sqlite")
        self.__cursor = self.connection.cursor()
    
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