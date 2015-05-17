# -*- coding: utf-8 -*-
from robot  import robot
from bottle import Bottle, request, run, template
from bottle import jinja2_view as view
from douban_client import DoubanClient
from douban import *
import urllib2
import sae
import sae.kvdb

client_login = DoubanClient(LOGIN_API_KEY, LOGIN_API_SECRET, LOGIN_REDIRECT_URI, LOGIN_SCOPE)

kv = sae.kvdb.Client()

app = Bottle()

@app.get('/')
@view('templates/index.html')
def welcome():
    number = 10
    return {'hello_world_str':'Hello world! Number:%s ' % str(number)}

@app.get('/ted')
def tedlist():
    return "andy"
 
@app.get('/auth')
def login():
    return client_login.authorize_url
#    return urllib2.urlopen(client_login.authorize_url)
 
@app.get('/login')
def greet():
    code = request.GET.get('code', 0)
    client_login.auth_with_code(code)
    uid =  client_login.user.me.get('uid', 0)
    
    uid_utf8 = uid.encode('utf-8')
    kv.set(uid_utf8, client_login.token_code)
#    token = kv.get(uid_utf8)
    uid = uid_utf8.decode('utf-8')

    return template('Hello {{name}}, how are you?', name=uid)
   
# douban api callback
@app.get('/douban')
def douban():
    code = request.GET.get('code', None)
    return "paste the code to wechat:  " + code

# wechat request
app.mount('/api', robot.wsgi)

application = sae.create_wsgi_app(app)



