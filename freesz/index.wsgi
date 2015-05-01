from bottle import Bottle, debug, run, request
import sae

app = Bottle()

@app.route('/')
def hello():
    print "hello log"
    return request.GET.get('echostr', None)

application = sae.create_wsgi_app(app)

