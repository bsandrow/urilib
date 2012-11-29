import re

import urilib.parsing

class URI(object):
    scheme = None
    authority = None
    path = None
    query = None
    fragment = None

    def __init__(self, uri):
        self.original = uri
        self._parse()

    def _parse(self):
        uri = self.original

        uri_parts = urilib.parsing.parse_uri(uri)

        self.scheme = uri_parts.scheme
        self.authority = uri_parts.authority
        self.path = uri_parts.path
        self.query = uri_parts.query
        self.fragment = uri_parts.fragment

    def __repr__(self):
        return "<URI(%s)>" % str(self)

    def __str__(self):
        uri = self.scheme
        if self.authority:
            uri += "://" + self.authority
        if self.path:
            uri += "/" + self.path
        if self.query:
            uri += '?' + str(self.query)
        if self.fragment:
            uri += "#" + self.fragment
        return uri
