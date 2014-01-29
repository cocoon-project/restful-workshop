# _*_ coding: utf-8 _*_
"""

    Utiliser bottle server pour obtenir des info sur la platform_machine






"""

from bottle import route, run , response
from tools import platform_kinds,platform_information,get_environ_variables
from tools import to_json


@route('/hello')
def hello():
    return "Hello World!"


@route('/platform')
def get_platform_kinds():
    response.content_type = "application/json"
    return to_json(platform_kinds())

@route('/platform/machine')
def platform_machine():
    """
        get info on local machine
    """
    return to_json(platform_information("machine"))

#TODO : l'url /platform/<kind> renvoie kind , modifier la fonction pour obtenir l'information
@route('/platform/<kind>')
def platform_element(kind):
    """
        modifier la fonction pour retourner l'info designée par kind (machine,node)

        la valeur retournée doit etre au format json

    """
    return kind



run(host='localhost', port=8088, debug=True, reloader=True)
