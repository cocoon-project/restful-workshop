"""

    tools for iterfacing with system


"""


import sys
import platform
import os
import json
from pprint import PrettyPrinter



# my os environment var
def get_environ_variables():
    """
        return the environments variables (list)

    """
    return os.environ.data



kinds = ['machine','node','platform','processor','python_build','python_compiler','python_version',
         'python_implementation','release','system','version','uname']

def platform_kinds():
    """
        return the kinds of information available with platform_information()
    """
    return kinds

def platform_information(kind='all'):
    """
        return platform information
    """
    if hasattr(platform,kind):
        return getattr(platform,kind)()
    elif kind == 'all' :

        a_dict = {}
        for kind in kinds :
            a_dict[kind] = getattr(platform,kind)()
        return a_dict
    else:
        return None



# to json conversion
def to_json(element):
    """
        convert a python element to json

    """
    return json.dumps(element)

def from_json(json_string):
    """
       convert a json string to a python element
    """
    return json.loads(json_string)

# html conversion

def list_to_html(a_list):
    """
        transform a list in html snippet

    """
    html = "<ul>"
    for item in a_list:
        html+= "<li>%s</li>" % item
    html+= "</ul>"
    return html

def dict_to_html(a_dict):
    """
        transform a dict in html snippet

    """
    html = "<ul>"
    for k,v in a_dict.iteritems():
        html+= "<li>%s = %s</li>" % (k,v)
    html+= "</ul>"
    return html


if __name__ == "__main__":

    def test():
        v = get_environ_variables()
        PrettyPrinter().pprint(v)

        h = dict_to_html(v)
        print PrettyPrinter().pprint(h)


        print PrettyPrinter().pprint( platform_kinds())


        info = platform_information()
        PrettyPrinter().pprint(info)




        #env = os.environ.data
        #print env
        #PrettyPrinter().pprint(env)
        #print
        #print PrettyPrinter().pprint(json.dumps(env))
        #
        #return


    test()
    print