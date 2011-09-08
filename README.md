urilib
======

A Python library for handling URIs and URLs. It is based off of my experience
with Perl's URI and URI::URL, which I find infinitely more usable than what
Python currently has to offer.

This is in response to (in my opinion) the lack of good URI processing in Python.

Example
=======

    import urilib

    uri = urilib.URI('http://www.example.com/?q=value')

    assert uri.scheme == 'http'
    assert uri.authority == 'www.example.com'
    assert uri.query == 'q=value'
    assert uri.fragment == ''

    url = urilib.URL('http://www.example.com/?q=value')

    query = urilib.Query(url.query)

    # Each value is a list (b/c it's possible to have multiple values for the # same key)
    query['test'].append('val')

    url.query = str(query)
    assert url.query == 'q=value&test=val'

    url = urilib.URL('http://www.example.com/?q=value')

    query = urilib.Query(url.query, separator=';')
    query['test'].append('val')
    url.query = str(query)
    assert url.query == 'q=value;test=val'

Requirements
============

 * Python 2.3+

Credits
=======

2011 (c) Brandon Sandrowicz <brandon@sandrowicz.org>

License
=======

See LICENSE
