from robot  import robot
from douban import client
from bottle import Bottle, request, run

import sae

app = Bottle()
app.mount('/api', robot.wsgi)

@app.get('/douban')
def douban():
    code = request.GET.get('code', None)
    return "paste the code to wechat:" + code

application = sae.create_wsgi_app(app)



