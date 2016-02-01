import json
from flask import Flask
from flask import request
from flask.ext.bcrypt import Bcrypt
from wtforms import Form, TextField, PasswordField, validators
from random import randint

import database_helper

app = Flask(__name__)
bcrypt = Bcrypt(app)

class SignUpForm(Form):
    firstName = TextField('First name', [validators.Required()])
    lastName = TextField('Last name', [validators.Required()])
    gender = TextField('Gender', [validators.Required()])
    city = TextField('City', [validators.Required()])
    country = TextField('Country', [validators.Required()])
    signupEmail = TextField('Email', [validators.Required(), validators.Email()])
    signupPassword = PasswordField('Password', [validators.Required(), validators.Length(min=6, max=30), validators.EqualTo('repeatPassword', message='Password doesn\'t match')])
    repeatPassword = PasswordField('Repeat password', [validators.Required()])

@app.before_request
def beforeRequest():
    database_helper.connectToDatabase()

@app.teardown_request
def teardownRequest(exception):
    database_helper.closeDatabaseConnection()

def createToken():
    letters = 'abcdefghiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    token = ''
    for i in range(0, 36):
        token += letters[randint(0,len(letters) - 1)]
    return token

def validLogin(email, password):
    user = database_helper.getUserByEmail(email)
    if user is None:
        return False
    else:
        print user
        if bcrypt.check_password_hash(user[1], password):
            return True
        else:
            return False    

def validEmail(email):
    user = database_helper.getUserByEmail(email)
    if user is None:
        return True
    else:
        return False

@app.route('/')
def main():
    return "Hello"

@app.route('/sign_in', methods=['POST'])
def signIn():
    if validLogin(request.form['loginEmail'], request.form['loginPassword']):
        token = createToken()
        result = database_helper.insertSignedInUser(token, request.form['loginEmail']);
        if result == True:
            return json.dumps({'success': True, 'message': 'Successfully signed in.', 'data': token}), 200
        else:
            return json.dumps({'success': False, 'message': 'Could not sign in user.'}), 501
    else:
        return json.dumps({'success': False, 'message': 'Wrong username or password.'}), 404

@app.route('/sign_up', methods=['POST'])
def signUp():
    form = SignUpForm(request.form)
    if form.validate():
        if validEmail(request.form['signupEmail']):
            passwordHash = bcrypt.generate_password_hash(request.form['signupPassword'])
            result = database_helper.insertUser(request.form['signupEmail'], request.form['firstName'], request.form['lastName'], request.form['gender'], request.form['city'], request.form['country'], passwordHash)
            if result == True:            
                return json.dumps({'success': True, 'message': 'Successfully created a new user.'}), 200
            else:
                return json.dumps({'success': False, 'message': 'Could not create user.'}), 501
        else:
            return json.dumps({'success': False, 'message': 'User already exists.'}), 404
    else:
        return json.dumps({'success': False, 'message': 'Form data missing or incorrect type.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
