# -*- coding: utf-8 -*-
from robot  import robot
from bottle import Bottle, request, run, template

from douban_client import DoubanClient
from douban import *

client_login = DoubanClient(LOGIN_API_KEY, LOGIN_API_SECRET, LOGIN_REDIRECT_URI, LOGIN_SCOPE)

import sae

app = Bottle()

@app.get('/')
def welcome():
    return "Welcome to Niubility!"

@app.get('/ted')
def tedlist():
    return "andy"
 
@app.get('/auth')
def login():
    return  client_login.authorize_url
 
    #return template('Hello {{name}}, how are you?', name=name)
@app.get('/login')
def greet():
    code = request.GET.get('code', 0)
    client_login.auth_with_code(code)
    print client_login.token_code
    print client_login.user.me
    return template('Hello {{name}}, how are you?', name=client_login.user.me)
   
# douban api callback
@app.get('/douban')
def douban():
    code = request.GET.get('code', None)
    return "paste the code to wechat:  " + code

# wechat request
app.mount('/api', robot.wsgi)

application = sae.create_wsgi_app(app)



