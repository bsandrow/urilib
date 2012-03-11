urilib
======

A Python library for handling URIs. Based off of my experience with Perl's URI,
having a class to wrap URIs allows for quick editting of pieces of the URI
without the need to write code to decompose/recompose every time.

Synopsis
========

    import urilib

    uri = urilib.URI('http://www.example.com/?q=value')

    assert uri.scheme    == 'http'
    assert uri.authority == 'www.example.com'
    assert uri.path      == '/'
    assert uri.query     == 'q=value'
    assert uri.fragment  == ''

Requirements
============

 * Python 2.3+

Credits
=======

2012 (c) Brandon Sandrowicz <brandon@sandrowicz.org>

License
=======

See LICENSE
