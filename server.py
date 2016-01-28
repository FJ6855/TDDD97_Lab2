from __future__ import print_function # In python 2.7
from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.bcrypt import Bcrypt
import sys
#import database_helper

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return 'Hello'

def createToken():
    letters = 'abcdefghiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    token = ''
    for i in range(0, 36):
        token += letters[randint(0,len(letters))]
    return token

def validLogin(email, password):
    passwordHash = bcrypt.generate_password_hash(password);
    user = queryDb('select * from users WHERE email = ? and password = ?', [email, passwordHash], one=True)
    return user is None

@app.route('/sign_in', methods=['POST'])
def signIn():
    if validLogin(request.form['loginEmail'], request.form['loginPassword']):
        token = createToken()
        return jsonify(success=True, message='Successfully signed in.', data=token)
    else:
        return jsonify(success=False, message='Wrong username or password.')

if __name__ == '__main__':
    app.run(debug=True)
