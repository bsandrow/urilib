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
        if uri:
            self.original = uri
            self._parse()

    def _parse(self):
        uri = self.original

        uri_parts = parse_uri(uri)

        self.scheme, self.path, self.fragment = uri_parts[::2]
        self.authority, self.query = uri_parts[1::2]

        # if the query is None, then there wasn't *any* query component in the
        # uri, so we want to leave the query as None to preserve this, or else
        # we will get:
        #
        #   http://example.com/?#Chapter-1
        #
        # instead of:
        #
        #   http://example.com/#Chapter-1
        #
        # Technically, they are equivalent, but some people might care.
        if self.query is not None:
            self.query = QueryDict(self.query or '')

    def __repr__(self):
        return "URI('%s')" % str(self)

    def __str__(self):
        uri = ""

        if self.scheme:
            uri += self.scheme + ":"

        if self.authority is not None:
            uri += "//" + authority

        if self.path is not None:
            uri += self.path

        if self.query is not None:
            uri += "?" + str(self.query)

        if self.fragment is not None:
            uri += "#" + self.fragment

        return uri
