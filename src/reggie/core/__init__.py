# coding: utf-8
'''Reggie, the BEL resource generator.

reggie.core
'''
import os


def modules_at_path(file):
    '''Get all modules other than __init__ at the path rooting *file*.'''
    root = os.path.dirname(os.path.abspath(file))
    modules = []
    for entry in os.listdir(root):
        # skip __init__ and non-Python (.py) modules
        # (skips pyx, pyc, etc. modules intentionally)
        if entry == '__init__.py':
            continue
        if not entry.endswith('.py'):
            continue

        entry = entry.replace('.py', '')
        modules.append(entry)
    return modules
