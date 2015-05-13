import sae

from robot  import robot
from douban import client
from bottle import Bottle, request, run

application = sae.create_wsgi_app(robot.wsgi)

'''
import sys
print sys.path

application.mount('/api', wxrobot.wsgi)

@application.get('/douban')
def douban():
    code = request.GET.get('code', None)
    print code
    client.auth_with_code(code)
    print client.token_code
    print 'from douban'
    return "oauth begin"

'''
