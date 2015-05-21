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
import bs4

client_login = DoubanClient(LOGIN_API_KEY, LOGIN_API_SECRET, LOGIN_REDIRECT_URI, LOGIN_SCOPE)
ted_url = 'http://www.ted.com/talks?sort=popular'
kv = sae.kvdb.Client()

app = Bottle()

@app.get('/')
@view('templates/index.html')
def welcome():
    number = 10
    return {'hello_world_str':'Hello world! Number:%s ' % str(number)}

'''
  <div class="media__message">
             <h4 class="h12 talk-link__speaker">Ken Robinson</h4>
             <h4 class="h9 m5"> <a href="/talks/ken_robinson_says_schools_kill_creativity"> How schools kill creativity </a> </h4>
             <div class="meta">
              <span class="meta__item"> <span class="meta__val"> 33M views </span> </span>
              <span class="meta__item"> <span class="meta__val"> Jun 2006 </span> </span>
             </div>
            </div>

'''
def get_video_page_urls():
        response = requests.get(ted_url)
        soup = bs4.BeautifulSoup(response.text)
        ret_str = ''
        for tag in soup.find_all("h4"):
            if None != tag.string:
                ret_str += tag.string + '\n'
        return ret_str

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



