"""

    tools for interfacing with system


"""


import sys
import platform
import os
import json
import psutil
from pprint import PrettyPrinter



# my os environment var
def get_environ_variables():
    """
        return the environments variables (list)

    """
    return os.environ.data



# tools for platform info

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

# tools for psutil
psutil_commands = ["cpu_times_percent","virtual_memory","swap_memory","disk_partitions","disk_usage","disk_io_counters",
                   "net_io_counters","get_boot_time","get_users"]

def psutil_information(command,arg=None):
    """
        psutil information

    """
    if command == "disk_usage" :
        if not arg:
            arg = '/'
        return psutil.disk_usage(arg)
    elif command == "disk_io_counters":
        if not arg:
            arg=False
        return psutil.disk_io_counters(arg)
    else:
        return getattr(psutil,command)()


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

        for command in psutil_commands:
            print psutil_information(command)
            continue




        #env = os.environ.data
        #print env
        #PrettyPrinter().pprint(env)
        #print
        #print PrettyPrinter().pprint(json.dumps(env))
        #
        #return


    test()
    print