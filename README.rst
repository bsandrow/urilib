urilib: URIs shouldn't be hard
==============================

Overview
--------

Dealing with URIs should be simple. Most of the time, the technical spec for
the URIs is not difficult, but there is not good API for composing them,
decomposing them, editing them, recomposing them. With this library I hope to
fix that.

Basic URIs can be broken down into 5 basic components: scheme, authority, path,
query, fragment. The URI parsing is kept to basics, with specific parsing for
handling URI schemes that need special handling to make them work right (i.e.
multiple params are implemented as name.1, name.2, etc. in magnet URIs).

Usage
-----

Composing a URL: ::

    >>> import urilib
    >>> uri = urilib.uri()
    >>> uri.scheme = 'https'
    >>> uri.authority = 'www.google.com:443'
    >>> uri.path = '/'
    >>> str(uri)
    'https://www.google.com:443/'
    >>> uri.query.update({ 'q': 'urilib', 'sourceid': 'chrome', 'ie': 'UTF-8' })
    >>> str(uri)
    'https://www.google.com:443/?q=urilib&sourceid=chrome&ie=UTF-8'

Decomposing an URL: ::

    >>> import urilib
    >>> uri = urilib.uri('http://www.google.ca/search?sourceid=chrome&client=ubuntu&channel=cs&ie=UTF-8&q=urilib')
    >>> uri.scheme
    'http'
    >>> uri.authority
    'www.google.ca'
    >>> uri.path
    '/search'
    >>> uri.fragment
    ''
    >>> str(uri.query)
    '?sourceid=chrome&client=ubuntu&channel=cs&ie=UTF-8&q=urilib'

Adding a query parameter to a URL: ::

    >>> import urilib
    >>> uri = urilib.uri('http://www.example.com?q=urilib')
    >>> uri.query['q'].append('urlparse')
    >>> str(uri)
    'http://www.example.com?q=urilib&q=urlparse'

Accessing query parameters: ::

    >>> import urilib
    >>> uri = urilib.uri('http://www.example.com/?q=urilib&q=urlparse&lang=en')
    >>> uri.query['lang']
    'en'
    >>> uri.query['q']
    ['urilib', 'urlparse']

Dealing with URI encoding: ::

    >>> import urilib
    >>> uri = urilib.uri('http://www.example.com/?q=urilib%20urlparse&lang=en')
    >>> uri.query['q']
    'urilib urlparse'
    >>> uri.query['q'] += ' extra data'
    >>> str(uri.query)
    'q=urilib%20urlparse%20extra%20data&lang=en'

Credits
-------

Copyright 2012 (c) Brandon Sandrowicz <brandon@sandrowicz.org>

