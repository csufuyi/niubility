from robot  import robot
from douban import client
from bottle import Bottle, request, run

import sae

app = Bottle()
app.mount('/api', robot.wsgi)

@app.get('/douban')
def douban():
    code = request.GET.get('code', None)
    client.auth_with_code(code)
    print client.token_code
    return "douban auth sucess, please backto wechat"

application = sae.create_wsgi_app(app)



