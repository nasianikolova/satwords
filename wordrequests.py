from dbconnector import MySQLConnection
import uuid
from dotenv import load_dotenv
import os

class DBRequests:
    def __init__(self):
        load_dotenv()
        host = os.getenv("HOST")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        name = os.getenv("NAME")
        port = os.getenv("PORT")
        
        dbConnection = MySQLConnection(host, user, password, name, port)
        self._connection = dbConnection.get_instance()
        self._mycursor = self._connection.cursor(dictionary=True)
        self.ensure_fails_column_exists()

    def ensure_fails_column_exists(self):
        try:
            self._mycursor.execute("SHOW COLUMNS FROM words LIKE 'fails'")
            result = self._mycursor.fetchone()
            if not result:
                alter_sql = "ALTER TABLE words ADD COLUMN fails INT DEFAULT 0"
                self._mycursor.execute(alter_sql)
                self._connection.commit()
                print("Column 'fails' successfully added.")
        except Exception as e:
            print("Check/Create 'fails' column failed:", e)

    def insert_word(self, username, word, translation, sentence):
        new_uuid = str(uuid.uuid4())
        sql = """
            INSERT INTO words (uuid, username, word, translation, sentence)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (new_uuid, username, word, translation, sentence)
        try:
            self._mycursor.execute(sql, val)
            self._connection.commit()
        except Exception as e:
            print("Insert word failed:", e)

    def delete_word(self, uuid):
        sql = "DELETE FROM words WHERE uuid = %s"
        try:
            self._mycursor.execute(sql, (uuid,))
            self._connection.commit()
        except Exception as e:
            print("Delete word failed:", e)

    def reset_fail(self, uuid):
        sql = "UPDATE words SET fails = 0 WHERE uuid = %s"
        try:
            self._mycursor.execute(sql, (uuid,))
            self._connection.commit()
        except Exception as e:
            print("Reset fail count failed:", e)

    def increment_fail(self, uuid):
        sql = "UPDATE words SET fails = COALESCE(fails, 0) + 1 WHERE uuid = %s"
        try:
            self._mycursor.execute(sql, (uuid,))
            self._connection.commit()
        except Exception as e:
            print("Increment fail count failed:", e)

    def insert_user(self, firstname, lastname, email, username, password):
        new_uuid = uuid.uuid4()
        sql = """
            INSERT INTO Users (uuid, firstname, lastname, email, username, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (str(new_uuid), firstname, lastname, email, username, password)
        try:
            self._mycursor.execute(sql, val)
            self._connection.commit()
        except Exception as e:
            print("Insert user failed:", e)

    def authenticate_user(self, email, password):
        sql = """
            SELECT username, firstname, lastname
            FROM Users
            WHERE email = %s AND password = %s
        """
        val = (email, password)
        try:
            self._mycursor.execute(sql, val)
            result = self._mycursor.fetchall()
            return result
        except Exception as e:
            print("Authentication failed:", e)
            return []

    def fetch_words(self, username):
        sql = """
            SELECT uuid, word, translation, sentence, fails
            FROM words
            WHERE username = %s
        """
        try:
            self._mycursor.execute(sql, (username,))
            result = self._mycursor.fetchall()
            return result
        except Exception as e:
            print("Fetch words failed:", e)
            return []

    def identify_user(self, username, password):
        sql = """
            SELECT firstname, lastname
            FROM Users
            WHERE username = %s AND password = %s
        """
        try:
            self._mycursor.execute(sql, (username, password))
            result = self._mycursor.fetchall()
            return result
        except Exception as e:
            print("Identify user failed:", e)
            return []

    def fetch_top_failed_words(self, username):
        sql = """
            SELECT uuid, word, translation, sentence, fails
            FROM words
            WHERE username = %s AND fails > 0
            ORDER BY fails DESC
            LIMIT 20
        """
        try:
            self._mycursor.execute(sql, (username,))
            return self._mycursor.fetchall()
        except Exception as e:
            print("Fetch top failed words failed:", e)
            return []
