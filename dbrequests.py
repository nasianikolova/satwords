# Requests to MySQL Database using the Singleton Design Pattern
from dbconnector import MySQLConnection
import uuid
from dotenv import load_dotenv
import os

class DBRequests:
    _connection = None
    _mycursor = None

    def __init__(self):
        load_dotenv()
        host = os.getenv("HOST")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        name = os.getenv("NAME")
        port = os.getenv("PORT")

        dbConnection = MySQLConnection(host, user, password, name, port)
        DBRequests._connection = dbConnection.get_instance()
        DBRequests._mycursor =  DBRequests._connection.cursor()

    def insertUser(self, firstname, lastname, email, username, password):
        new_uuid = uuid.uuid4()
        sql = "INSERT INTO Users (uuid, firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (str(new_uuid), firstname, lastname, email, username, password)
        DBRequests._mycursor.execute(sql, val)

        DBRequests._connection.commit()

    def authenticateUser(self, email, password):
        sql = "SELECT username, firstname, lastname FROM Users WHERE email = %s AND password = %s"
        val = (email, password)
        try:
            DBRequests._mycursor.execute(sql, val)
            result = DBRequests._mycursor.fetchall()
            return result
        except:
            print(Exception)

    def fetchWords(self, username):
        sql = "SELECT uuid, word, translation, sentence FROM words WHERE username = %s"
        val = (username,)

        try:
            DBRequests._mycursor.execute(sql, val)
            result = DBRequests._mycursor.fetchall()
            return result
        except Exception as e:
            print(e)


    # identifyUser method
    # parameters username, password
    # SQL Request: SELECT firstname, lastname FROM Users WHERE username = username AND password = password
    # Python Integration: SELECT firstname, lastname FROM Users WHERE username = ? AND password = ?