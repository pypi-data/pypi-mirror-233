# meta.py
#    Show meta info of code
#    By Johnny Cheng
#    Updated: 2 October 2023

import inspect
import pkgutil
from importlib import import_module

def get_module_info():
    modname = __name__.split('.')[:-1]
    module = import_module(modname)

    i = 0
    mod_info = "The list of sub-modules and their functions of Module '" + modname + "'\n"
    for _, submodname, ispkg in pkgutil.iter_modules(module.__path__):
        if not ispkg:
            i += 1
            mod_info += "%d. %s:" %(i, submodname) + "\n"
            submod = import_module(".."+submodname, modname+"."+submodname)
            for name, member in inspect.getmembers(submod):
                if inspect.isfunction(member) and name != 'files':
                    #mod_info += "\t", name, str(inspect.signature(member)) + "\n"
                    mod_info += "\t{} {}\n".format(name, inspect.signature(member))

    return mod_info
