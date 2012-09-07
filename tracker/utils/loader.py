"""
Plugin Loader

"""
from __future__ import print_function
from __future__ import absolute_import


import sys


def _resolve_name(name, package, level):
    """ Return the absolute name of the module to be imported. """
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level package.")
    return "{0}.{1}".format(package[:dot], name)


def _import_class(path):
    path_bits = path.split('.')
    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = import_module(module_path)

    if not hasattr(module_itself, class_name):
        raise ImportError("The Python module '{0}' has no '{1}' class.".format(
            module_path, class_name))

    return getattr(module_itself, class_name)


def import_module(name, package=None):
    """ Lazy import a module. """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument.")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


def import_class(full_backend_path):
    """ Lazy import a class. """
    path_bits = full_backend_path.split('.')

    if len(path_bits) < 2:
        raise ImportError(
            "The provided backend '{0}' is not a complete Python "
            "path to a BaseEngine subclass.".format(full_backend_path))

    return _import_class(full_backend_path)