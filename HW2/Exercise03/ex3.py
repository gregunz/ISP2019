from flask import Flask, request, abort, make_response
import base64
import hmac
import time

enc = 'utf-8'
key = 'KRcTAh1JAQBAB0wETQ0bGSELUBIDDgcH'.encode(enc)

def is_logged_in(cookie, hashmac):
    true_hashmac = hmac.new(key, cookie.encode(enc)).hexdigest()
    return hashmac == true_hashmac

def is_user(): return True

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ex3/login', methods=['POST'])
def login():
    payload = request.get_json()
    usr = payload['user']
    pwd = payload['pass']
    ts = int(time.time())
    if usr == 'administrator' and pwd == '42':
        cookie = '{},{},com402,hw2,ex3,administrator'.format(usr, ts)
    else:
        cookie = '{},{},com402,hw2,ex3,user'.format(usr, ts)
    hashmac = hmac.new(key, cookie.encode(enc)).hexdigest()
    cookie += ',{}'.format(hashmac)
    cookie = base64.b64encode(cookie.encode(enc)).decode(enc)
    resp = make_response()
    resp.set_cookie('LoginCookie', cookie)
    return resp

@app.route('/ex3/list', methods=['POST'])
def access():
    cookie = request.cookies.get('LoginCookie')
    if cookie:
        cookie = base64.b64decode(cookie.encode(enc)).decode(enc)
        cookie = cookie.split(',')
        is_admin = cookie[-2] == 'administrator'
        cookie, hashmac = ','.join(cookie[:-1]), cookie[-1]
        if is_admin and is_logged_in(cookie, hashmac):
            return "success"
        elif is_logged_in(cookie, hashmac):
            return make_response('success', 201)
    return abort(403)
    
    

app.run()