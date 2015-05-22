# -*- coding: utf-8 -*-
from robot  import robot
from robot  import client
from robot  import wechat_kv
from robot  import ted_kv
from robot  import TED_NEWEST, TED_POPULAR
from werobot.utils  import * 
from bottle import Bottle, request, run, template
from bottle import jinja2_view as view
from jinja2 import Environment, FileSystemLoader
from douban_client import DoubanClient
from douban import *
import urllib2
import sae
import sae.kvdb
import json
import requests
import bs4

client_login = DoubanClient(LOGIN_API_KEY, LOGIN_API_SECRET, LOGIN_REDIRECT_URI, LOGIN_SCOPE)

login_kv = sae.kvdb.Client()

ted_popular_url = 'http://www.ted.com/talks?page=1&sort=popular'
ted_newest_url = 'http://www.ted.com/talks?page=1'

app = Bottle()

@app.get('/')
def welcome():
    env = Environment(loader=FileSystemLoader('newhtml'))
    env.variable_start_string = '{{ '
    env.variable_end_string = ' }}'
    template = env.get_template('index.html')
    return template.render(the='variables', go='here')

'''
TED web html
<h4 class="h12 talk-link__speaker">Ken Robinson</h4>
'''
def get_ted_page_name():
        response = requests.get(ted_popular_url)
        soup = bs4.BeautifulSoup(response.text)
        ted_name_list = []
        for tag in soup.find_all("h4"):
            if None != tag.string:
                ted_name_list.append(tag.string) 
        ted_name_str = json.dumps(ted_name_list)
        ted_kv.set(to_binary(TED_POPULAR), ted_name_str) 
        return ted_name_str

@app.get('/ted')
@view('templates/ted.html')
def tedlist():
    res = get_ted_page_name()
    print res
    return {'ted_str':res}

# web login auth douban
@app.get('/auth')
@view('templates/login.html')
def login():
    print client_login.authorize_url
    return {'auth_str':'"'+client_login.authorize_url+ '&state=testcontext'+'"'}

# web login douban callback
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



