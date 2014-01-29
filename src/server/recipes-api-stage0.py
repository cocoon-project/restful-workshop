# _*_ coding: utf-8 _*_

from bottle import route, run



@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', port=8088, debug=True, reloader=True)
