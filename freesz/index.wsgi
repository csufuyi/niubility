# -*- coding: utf-8 -*-
from robot  import robot
from bottle import Bottle, request, run

import sae

app = Bottle()

@app.get('/')
def welcome():
    return "Welcome to Niubility!"

@app.get('/ted')
def tedlist():
    return "andy"

@app.get('/admin')
def login():
    return "admin"

# douban api callback
@app.get('/douban')
def douban():
    code = request.GET.get('code', None)
    return "paste the code to wechat:  " + code

# wechat request
app.mount('/api', robot.wsgi)

application = sae.create_wsgi_app(app)



