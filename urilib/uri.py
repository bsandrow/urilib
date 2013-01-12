from .query   import QueryDict
from .parsing import parse_uri

class URI(object):
    original = None
    scheme = None
    authority = None
    path = None
    query = None
    fragment = None

    def __init__(self, uri=None):
        self.query = QueryDict('')

        if uri:
            self.original = uri
            self._parse()

    def _parse(self):
        uri = self.original

        uri_parts = parse_uri(uri)

        self.scheme, self.path, self.fragment = uri_parts[::2]
        self.authority, self.query = uri_parts[1::2]
        self.query = QueryDict(self.query or '')

    def __repr__(self):
        return "URI('%s')" % str(self)

    def __str__(self):
        uri = ""

        if self.scheme:
            uri += self.scheme + ":"

        if self.authority is not None:
            uri += "//" + self.authority

        if self.path is not None:
            uri += self.path

        if str(self.query):
            uri += "?" + str(self.query)

        if self.fragment:
            uri += "#" + self.fragment

        return uri
