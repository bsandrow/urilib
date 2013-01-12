from __future__ import print_function

from urilib import __version__ as urilib_version

try:
    from setuptools import setup
except ImportError:
    print("Falling back to distutils. Functionality may be limited.")
    from distutils.core import setup

requires = []
long_description = open('README.rst').read() + "\n\n" + open("Changelog.rst").read()

config = {
    'name'            : 'urilib',
    'description'     : 'Working with URIs should be easy.',
    'long_description': long_description,
    'author'          : 'Brandon Sandrowicz',
    'author_email'    : 'brandon@sandrowicz.org',
    'url'             : 'http://github.com/bsandrow/urilib',
    'version'         : '0.3',
    'packages'        : ['urilib'],
    'package_data'    : { '': ['LICENSE'] },
    'install_requires': requires,
    'license'         : open('LICENSE').read(),
    'test_suite'      : 'urilib.tests',
    'classifiers'     : (
        'Developerment Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
    ),
}

# I like having the version explicitly here, but let's make sure that we don't
# get out of sync.
assert config['version'] == urilib_version, "Version mis-match between urilib and setup.py"

setup(**config)
