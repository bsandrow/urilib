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
