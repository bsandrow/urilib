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

        self.scheme, self.path, self.fragment = uri_parts[::2]
        self.authority, self.query = uri_parts[1::2]

    def __repr__(self):
        return "<URI(%s)>" % str(self)

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
