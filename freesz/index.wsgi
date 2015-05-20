# -*- coding: utf-8 -*-
from robot  import robot
from robot  import client
from robot  import wechat_kv
from werobot.utils  import * 
from bottle import Bottle, request, run, template
from bottle import jinja2_view as view
from douban_client import DoubanClient
from douban import *
import urllib2
import sae
import sae.kvdb
import json
import requests

client_login = DoubanClient(LOGIN_API_KEY, LOGIN_API_SECRET, LOGIN_REDIRECT_URI, LOGIN_SCOPE)
ted_url = 'http://www.ted.com/talks?sort=popular'
kv = sae.kvdb.Client()

app = Bottle()

@app.get('/')
@view('templates/index.html')
def welcome():
    number = 10
    return {'hello_world_str':'Hello world! Number:%s ' % str(number)}


def get_video_page_urls():
        response = requests.get(ted_url)
        print response
        return response

@app.get('/ted')
def tedlist():
    res = get_video_page_urls()
    return res

# web login auth douban
@app.get('/auth')
@view('templates/login.html')
def login():
    print client_login.authorize_url
    return {'auth_str':'"'+client_login.authorize_url+ '&state=testcontext'+'"'}

# login douban callback
@app.get('/login')
def greet():
    code = request.GET.get('code', 0)
    guid = request.GET.get('state', None)
    print guid
    client_login.auth_with_code(code)
    uid =  client_login.user.me.get('uid', 0)
    kv.set(to_binary(guid), client_login.token_code)
    return template('Hello {{name}}, how are you?', name=uid)
   
# wechat douban api callback
@app.get('/douban')
@view('templates/douban.html')
def douban():
    code = request.GET.get('code', None)
    guid = request.GET.get('state', None)
    client.auth_with_code(code)
    uid =  client.user.me.get('uid', 0)
    user = {}
    user['uid'] = uid
    user['token'] = client.token_code
    user_str = json.dumps(user)
    wechat_kv.set(to_binary(guid), user_str)
    return {'auth_str':uid}

# wechat request
app.mount('/api', robot.wsgi)

application = sae.create_wsgi_app(app)



