from flask import Flask
from flask import request, abort
import base64
import sys

def superencryption(msg,key):
    if len(key) < len(msg):
        diff = len(msg) - len(key)
        key += key[:diff]
    amsg = [ord(c) for c in msg]
    akey = [ord(c) for c in key[:len(amsg)]]
    assert len(amsg) == len(akey)

    s = [chr(m ^ akey[i]) for i, m in enumerate(amsg)]
    s = ''.join(s).encode('ascii')
    return base64.b64encode(s).decode('utf-8')

mySecureOneTimePad = "Never send a human to do a machine's job"
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hw2/ex1', methods=['POST'])
def login():
    payload = request.get_json()
    usr = payload['user']
    pwd = payload['pass']
    if superencryption(usr, mySecureOneTimePad) == pwd:
        return 'success'
    else:
        return abort(400)