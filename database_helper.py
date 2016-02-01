from flask import Flask
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = 'database.db'

databaseConnection = None

def connectToDatabase():
    global databaseConnection
    databaseConnection = sqlite3.connect(DATABASE)

def closeDatabaseConnection():
    if databaseConnection is not None: 
        databaseConnection.close()

def getUserByPassword(email, passwordHash):
    cursor = databaseConnection.cursor()
    cursor.execute('select * from users where email = ? and password = ?', (email, passwordHash))
    result = cursor.fetchone()
    cursor.close()
    return result

def getUserByEmail(email):
    cursor = databaseConnection.cursor()
    cursor.execute('select * from users where email = ?', (email,))
    result = cursor.fetchone()
    cursor.close()
    return result

def insertSignedInUser(token, email):
    cursor = databaseConnection.cursor()
    cursor.execute('insert into signedInUsers values (?, ?)', (token, email))
    databaseConnection.commit()
    cursor.close()
    return True

def insertUser(email, firstName, lastName, gender, city, country, passwordHash):
    cursor = databaseConnection.cursor()
    cursor.execute('insert into users values (?, ?, ?, ?, ?, ?, ?)', (email, passwordHash, firstName, lastName, gender, city, country))
    databaseConnection.commit()
    cursor.close()
    return True

