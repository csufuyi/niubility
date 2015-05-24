# -*- coding: utf-8 -*-

import os 
import sys
import json 

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

from bottle import Bottle, request, run, template
from bottle import jinja2_view as view
from jinja2 import Environment, FileSystemLoader
import sae

from robot import robot 
from db  import wechat_kv
from db  import login_kv
from douban import client_login
from douban import client_wechat
from ted import get_ted_page_name
from werobot.utils  import  to_binary

app = Bottle()

# web root 
@app.get('/')
def welcome():
    env = Environment(loader=FileSystemLoader('newhtml'))
    env.variable_start_string = '{{ '
    env.variable_end_string = ' }}'
    template = env.get_template('index.html')
    return template.render(the='variables', go='here')

# web ted
@app.get('/ted')
@view('templates/ted.html')
def tedlist():
    res = get_ted_page_name()
    print res
    return {'ted_str':res}

# web login 
@app.get('/auth')
@view('templates/login.html')
def login():
    print client_login.authorize_url
    return {'auth_str':'"'+client_login.authorize_url+ '&state=testcontext'+'"'}

# web  douban callback
@app.get('/login')
def greet():
    code = request.GET.get('code', 0)
    guid = request.GET.get('state', None)
    print guid
    client_login.auth_with_code(code)
    uid =  client_login.user.me.get('uid', 0)
    login_kv.set(to_binary(guid), client_login.token_code)
    return template('Hello {{name}}, how are you?', name=uid)


# wechat douban api callback
@app.get('/douban')
@view('templates/douban.html')
def douban():
    code = request.GET.get('code', None)
    guid = request.GET.get('state', None)
    client_wechat.auth_with_code(code)
    uid =  client_wechat.user.me.get('uid', 0)
    user = {}
    user['uid'] = uid
    user['token'] = client_wechat.token_code
    user_str = json.dumps(user)
    wechat_kv.set(to_binary(guid), user_str)
    return {'auth_str':uid}

# wechat request forward to robot
app.mount('/api', robot.wsgi)

application = sae.create_wsgi_app(app)



