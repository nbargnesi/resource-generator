# coding: utf-8
'''Reggie, the BEL resource generator.

reggie.converters.third_party
'''
import reggie.core as core
_package = 'reggie.converters.third_party'
_package_modules = core.modules_at_path(__file__)
modules = [__import__(_package + '.' + x) for x in _package_modules]