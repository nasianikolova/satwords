# DB Connector with Singleton Design Pattern
import mysql.connector as mysql
from typing import Dict

class User:
    __connectedUser = None


    @staticmethod
    def set_connectedUser(username):
        User.__connectedUser = username

    @staticmethod
    def get_connectedUser():
        return User.__connectedUser