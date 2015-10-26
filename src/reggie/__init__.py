'''Reggie, the BEL resource generator.

See https://github.com/OpenBEL/resource-generator.
'''
__author__ = 'OpenBEL'
__copyright__ = 'Copyright (C) 2015, OpenBEL Committers'
__credits__ = [
    'Natalie Catlett',
    'Jordan Hourani',
    'James F. McMahon',
    'Tony Bargnesi',
    'William Hayes',
    'Nick Bargnesi',
]
__license__ = 'Apache License 2.0'
__version__ = '0.1'
__maintainer__ = 'Nick Bargnesi'
__email__ = 'nbargnesi@selventa.com'
__status__ = 'alpha'

__all__ = [
    'gen',
    'core',
    'converters'
]


def main():
    print('reggie main')
    import reggie.converters
