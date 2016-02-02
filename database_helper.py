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

def executeSelect(sql, args, one = True):
    cursor = databaseConnection.cursor()
    cursor.execute(sql, args)
    if one:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    cursor.close()
    return result

def executeChange(sql, args):
    cursor = databaseConnection.cursor()
    cursor.execute(sql, args)
    databaseConnection.commit()
    cursor.close()
    return True

def getUserByPassword(email, passwordHash):
    return executeSelect('select * from users where email = ? and password = ?', (email, passwordHash))

def getUserByEmail(email):
    return executeSelect('select email, firstName, lastName, gender, city, country from users where email = ?', (email,))

def getUserPasswordByEmail(email):    
    return executeSelect('select password from users where email = ?', (email,))
    
def getUserEmailByToken(token):
    return executeSelect('select email from signedInUsers where token = ?', (token,))

def getUserMessagesByEmail(email):
    return executeSelect('select * from messages where wallEmail = ?', (email,))

def insertUser(email, firstName, lastName, gender, city, country, passwordHash):
    return executeChange('insert into users values (?, ?, ?, ?, ?, ?, ?)', (email, passwordHash, firstName, lastName, gender, city, country))

def insertSignedInUser(token, email):
    return executeChange('insert into signedInUsers values (?, ?)', (token, email))

def insertMessage(writerEmail, email, message):
    return executeChange('insert into messages (message, wallEmail, writer) values (?, ?, ?)', (message, email, writerEmail))

def deleteSignedInUser(token):
    return executeChange('delete from signedInUsers where token = ?', (token,))

def updateUserPassword(email, passwordHash):
    return executeChange('update users set password = ? where email = ?', (passwordHash, email))
