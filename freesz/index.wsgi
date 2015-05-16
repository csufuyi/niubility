# -*- coding: utf-8 -*-
from robot  import robot
from bottle import Bottle, request, run

import sae

app = Bottle()
app.mount('/api', robot.wsgi)

@app.get('/')
def welcome():
	return "2015年05月"

@app.get('/ted')
def tedlist():
	return "andy"

@app.get('/douban')
def douban():
    code = request.GET.get('code', None)
    return "paste the code to wechat:  " + code

application = sae.create_wsgi_app(app)



