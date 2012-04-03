#!/usr/bin/env python
"""A library for building/decomposing URIs
"""

__author__     = 'Brandon Sandrowicz'
__version__    = '0.2'
__copyright__  = 'Copyright 2012, Brandon Sandrowicz'
__license__    = 'MIT'
__maintainer__ = 'Brandon Sandrowicz'
__email__      = 'brandon@sandrowicz.org'
__status__     = 'Development'

import re
import urllib

# Character Classes
sub_delims  = "[!$&'()*+,;=]"
pct_encoded = "%[a-fA-F0-9]{2}"
unreserved  = "[a-zA-Z0-9._~-]"

# Parts
scheme_re    = re.compile(r'[^\W0-9_]([^\W_]|[+.-])*')
hier_part_re = re.compile(r'(%s|%s|%s|/)*' % (sub_delims, pct_encoded, unreserved))

def join_if_exists(join_string, iterable):
    return join_string.join(item for item in iterable if item)

class URI(object):
    orig_uri  = ""
    scheme    = ""
    hier_part = ""
    query     = ""
    fragment  = ""
    authority = ""
    path      = ""

    def __init__(self, uri):
        self.orig_uri = uri.strip()
        self._process_uri()

    def __str__(self):
        return self.uri

    def __repr__(self):
        return "<URI('%s')>" % self.uri

    def _process_uri(self):
        uri = self.orig_uri

        # Scheme
        parts = uri.split(':', 1)
        if len(parts) == 2:
            scheme, rest = parts
            match = scheme_re.match(scheme)
            if match:
                self.scheme = scheme
                uri = rest

        # Fragment
        parts = uri.rsplit('#', 1)
        if len(parts) == 2:
            rest, fragment = parts
            self.fragment = fragment
            uri = rest

        # Hier Part
        parts = uri.split('?', 1)
        if len(parts) == 2:
            hier_part, query = parts
        else:
            hier_part = uri
            query = ""

        match = hier_part_re.match(hier_part)
        if match:
            self.hier_part = hier_part
        else:
            self.hier_part = None

        self.query = query

        self._process_hier_part()

    def _process_hier_part(self):
        if self.hier_part.startswith('//'):
            parts = (self.hier_part[2:]).split('/', 1)
            if len(parts) == 2:
                self.authority, self.path = parts
                self.path = '/' + self.path
            else:
                self.authority = self.hier_part[2:]
        else:
            self.path = self.hier_part

    @property
    def uri(self):
        uri = join_if_exists(':', [self.scheme, self.hier_part])
        uri = join_if_exists('?', [uri, self.query])
        uri = join_if_exists('#', [uri, self.fragment])
        return uri

    @classmethod
    def parse_uri(cls, uri):
        uri = cls(uri)
        return {
            'scheme'  : uri.scheme,
            'netloc'  : uri.authority,
            'path'    : uri.path,
            'params'  : uri.query,
            'fragment': uri.fragment,
        }

class QueryDict(object):
    """A dictionary object for dealing with URI query parameters"""

    def __init__(self, query_string):
        self.params = self._str_to_params(query_string)

    def _str_to_params(self, string):
        """Convert a query string into a list of tuples"""
        params      = [ param.split('=') for param in string.split('&') ]
        return [ (urllib.unquote(k), urllib.unquote(v)) for k,v in params ]

    def _add_params(self, *args, **kwargs):
        """Internal implementation of append()

        The purpose of abstracting this is to possibly add QueryDict.update()
        later with the same interface.
        """
        if args:
            if len(args) > 1:
                raise TypeError("append() expected at most 1 arguments, got %d" % len(args))

            if isinstance(args[0], str):
                self.params += self._str_to_params(args[0])
            else:
                for k,v in args[0]:
                    self.params.append((k,v))

        for key in kwargs:
            self.params.append((key, kwargs[key]))

    def append(self, *args, **kwargs):
        """Take params in various forms of input. Append to param list."""
        self._add_params(*args, **kwargs)

    def list(self):
        """Return the params as a list of tuples."""
        return self.params

    def __delitem__(self, key):
        """When deleteing a key, remove all instances of a key"""
        self.params = [ param for param in self.params if param[0] != key ]

    def __contains__(self, key):
        for param in self.params:
            if param[0] == key:
                return True
        return False

    def __getitem__(self, key):
        for param in self.params:
            if param[0] == key:
                return param[1]
        raise KeyError

    # ???
    def __setitem__(self, key, value):
        self.params.append((key,value))

    def keys(self):
        return self.dict().keys()

    def values(self):
        return [ v for k,v in self.params ]

    def dict(self):
        d = {}
        for param in self.params:
            if param[0] not in d:
                d[param[0]] = param[1]
        return d

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def get_all(self, key):
        return [ param[1] for param in self.params if param[0] == key ]

    def __str__(self):
        quoted_params = [ (urllib.quote(k), urllib.quote(v)) for k,v in self.params ]
        joined_pairs  = [ '='.join(kvpair) for kvpair in quoted_params ]
        return '&'.join(joined_pairs)
