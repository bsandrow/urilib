
try:
    from setuptools import setup
except ImportError:
    print "Falling back to distutils. Functionality may be limited."
    from distutils.core import setup

requires = []
long_description = open('README.rst').read() + "\n\n" + open("Changelog.rst").read()

config = {
    'name'            : 'urilib',
    'description'     : 'Working with URIs should be easy.'
    'long_description': long_description,
    'author'          : 'Brandon Sandrowicz',
    'author_email'    : 'brandon@sandrowicz.org',
    'url'             : 'http://github.com/bsandrow/urilib',
    'version'         : 0.1,
    'packages'        : ['urilib'],
    'package_data'    : { '': ['LICENSE'] },
    'install_requires': requires,
    'license'         : open('LICENSE').read(),
    'test_suite'      : 'tests',
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

setup(**config)
