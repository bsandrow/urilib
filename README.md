urilib
======

A Python library for handling URIs. Based off of my experience with Perl's URI,
having a class to wrap URIs allows for quick editting of pieces of the URI
without the need to write code to decompose/recompose every time.

Basic Usage
===========

    import urilib

    uri = urilib.URI('http://www.example.com/?q=value')

    assert uri.scheme     == 'http'
    assert uri.authority  == 'www.example.com'
    assert uri.path       == '/'
    assert str(uri.query) == 'q=value'
    assert uri.fragment   == ''

    uri.query.append('lang=en')

    assert str(uri) == 'http://www.example.com/?q=value&lang=en'

QueryDict
=========

QueryDict is a dict-like class created for the sole purpose of manipulating
sets of query parameters.

    q = QueryDict('user=jdoe&age=55&lang=en')

    assert q.keys() == ['user','age','lang']
    assert 'user' in q
    assert q['user'] == 'jdoe'

    del q['age']
    assert str(q) == 'user=jdoe&lang=en'

    q.append('email=bob@example.com&email=lisa@example.com')

    assert q['email'] == 'bob@example.com'
    assert q.get_all('email') == ['bob@example.com','lisa@example.com']

Requirements
============

 * Python 2.6+

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
