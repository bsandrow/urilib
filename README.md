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

Bugs
====

No known bugs, but this hasn't been extensively tested, and there are probably
unaccounted-for edge cases out there in the wild. If you encounter any, or can
think of any that were missed, please contact the maintainer:

Brandon Sandrowicz <brandon@sandrowicz.org>

Credits
=======

2012 (c) Brandon Sandrowicz <brandon@sandrowicz.org>

License
=======

See LICENSE
