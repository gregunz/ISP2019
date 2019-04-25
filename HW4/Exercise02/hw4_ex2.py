from flask import Flask, request, abort, make_response
import bcrypt

salt = bcrypt.gensalt()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hw4/ex2', methods=['POST'])
def ex2():
    payload = request.get_json()
    usr = payload['user']
    pwd = payload['pass']

    hashed = bcrypt.hashpw(pwd.encode('utf8'), salt)

    return hashed
    
app.run()