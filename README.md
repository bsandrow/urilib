urilib
======

A Python library for handling URIs and URLs. It is based off of my experience
with Perl's URI and URI::URL, which I find infinitely more usable than what
Python currently has to offer.

This is also a response to the fact that there isn't much along the lines of
processing URIs/URLs in Python, and it took all the way until 2.7 for Python to
get a function in the standard library for breaking apart a URL into it's
component parts.

Example
=======

    import urilib

    uri = urilib.URI('http://www.example.com/?q=value')

    assert uri.scheme == 'http'
    assert uri.authority == 'www.example.com'
    assert uri.query == 'q=value'
    assert uri.fragment == ''

    url = urilib.URL('http://www.example.com/?q=value')

    query = url.get_query_as_dict()
    query['test'] = 'val'
    url.set_query_from_dict(query)
    assert url.query == 'q=value&test=val'

    url = urilib.URL('http://www.example.com/?q=value')

    query = url.get_query_as_dict()
    url.param_separator = ';'
    query['test'] = 'val'
    url.set_query_from_dict(query)
    assert url.query == 'q=value;test=val'
