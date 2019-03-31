from flask import Flask, request, abort
import base64

def superencryption(msg,key):
    if len(key) < len(msg):
        diff = len(msg) - len(key)
        key += key[:diff]
    amsg = [ord(c) for c in msg]
    akey = [ord(c) for c in key[:len(amsg)]]

    s = [chr(m ^ k) for m, k in zip(amsg, akey)]
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

app.run()