'''Reggie, the BEL resource generator.

See https://github.com/OpenBEL/resource-generator.
'''
import reggie


def main():
    info = '''
    bel-resource-generator
    --
    {copyright}
    License: {license}
    Version: {version}
    URL: {url}

    Made possible by the help of %d contributors.
    '''
    kwargs = {
        'version': reggie.__version__,
        'url': 'https://github.com/OpenBEL/resource-generator',
        'license': reggie.__license__,
        'copyright': reggie.__copyright__
    }
    print(info.format(**kwargs) % (len(reggie.__credits__)))


if __name__ == '__main__':
    a = 'foo'
    main()
