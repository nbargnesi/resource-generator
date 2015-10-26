# coding: utf-8
'''Reggie, the BEL resource generator.

reggie.converters.private
'''
import reggie.core as core
_package = 'reggie.converters.private'
_package_modules = core.modules_at_path(__file__)
modules = [__import__(_package + '.' + x) for x in _package_modules]
