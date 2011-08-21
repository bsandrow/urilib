
try:
    from setuptools import setup
except ImportError:
    print "Falling back to distutils. Functionality may be limited."
    from distutils.core import setup

config = {
    'description'  : 'A library for managing URIs',
    'author'       : 'Brandon Sandrowicz',
    'url'          : 'http://github.com/bsandrow/urilib',
    'author_email' : 'brandon@sandrowicz.org',
    'version'      : 0.1,
    'packages'     : ['urilib'],
    'name'         : 'urilib',
    'test_suite'   : 'urilib.tests',
}

setup(**config)
