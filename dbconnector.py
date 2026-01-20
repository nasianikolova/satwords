# DB Connector with Singleton Design Pattern
import mysql.connector as mysql
from typing import Dict

class MySQLConnection:
    __instance = None

    def __init__(self, host, user, password, name, port) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.name = name
        self.port = port
        
        if MySQLConnection.__instance is None:
            MySQLConnection.__instance = mysql.connect(host = self.host, user = self.user, passwd = password, database = self.name, port = self.port)
        
    @staticmethod
    def get_instance():
        if MySQLConnection.__instance:
            return MySQLConnection.__instance
    
    @staticmethod
    def close_instance() -> None:
        MySQLConnection.__instance.close()