import re

scheme_re = re.compile(r'[^\W0-9_]([^\W_]|[+.-])*')

def scheme_is_valid(scheme):
    """ Return True/False result of SCHEME validation. """
    m = scheme_re.match(scheme)
    return m is not None

class URI(object):
    scheme = None
    authority = None
    path = None
    query = None
    fragment = None

    def __init__(self, uri):
        self.original = uri
        self.parse()

    def parse(self):
        unparsed = self.original

        parts = unparsed.partition(':')
        if parts[2] is not None and scheme_is_valid(parts[0]):
            self.scheme, unparsed = parts[::2]

        parts = unparsed.partition('#')
        unparsed, self.fragment = parts[::2]

        parts = unparsed.partition('?')
        if parts[1]:
            unparsed, self.query = parts[::2]

        if unparsed.startswith('//'):
            unparsed = unparsed[2:]
            parts = unparsed.partition('/')
            if parts[2] is not None:
                self.authority = parts[0]
                self.path = ''.join(parts[1:])
            else:
                self.path = parts[0]
        else:
            self.path = unparsed

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
