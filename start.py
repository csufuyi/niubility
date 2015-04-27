from bottle import route, run

@route('/hello')
def hello():
    return "Hello Nubility!"

run(host='localhost', port=8080, debug=True)
