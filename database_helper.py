import sqlite3
from flask import g

DATABASE = 'database.db'

def getDb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def closeConnection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def queryDb(query, args=(), one=False):
    cursor = getDb().execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    return (result[0] if result else None) if one else result
