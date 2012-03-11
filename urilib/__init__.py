import re

# Character Classes
sub_delims  = "[!$&'()*+,;=]"
pct_encoded = "%[a-fA-F0-9]{2}"
unreserved  = "[a-zA-Z0-9._~-]"

# Parts
scheme_re    = re.compile(r'[^\W0-9_]([^\W_]|[+.-])*')
hier_part_re = re.compile(r'(%s|%s|%s|/)*' % (sub_delims, pct_encoded, unreserved))

class URI(object):

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
            else:
                self.scheme = None

        # Fragment
        parts = uri.rsplit('#', 1)
        if len(parts) == 2:
            rest, fragment = parts
            self.fragment = fragment
            uri = rest
        else:
            self.fragment = None

        # Hier Part
        parts = uri.split('?', 1)
        if len(parts) == 2:
            hier_part, query = parts
        else:
            hier_part = uri
            query = None

        match = hier_part_re.match(hier_part)
        if match:
            self.hier_part = hier_part
            uri = rest
        else:
            self.hier_part = None

        self.query = query

    @property
    def uri(self):
        if self.scheme:
            uri = "%s:" % self.scheme
        else:
            uri = ""

        if self.hier_part:
            uri += self.hier_part

        if self.query:
            uri += '?' + self.query

        if self.fragment:
            uri += '#' + self.fragment

        return uri

    @classmethod
    def parse_uri(cls, uri):
        uri = cls(uri)
        return {
            'scheme'  : uri.scheme,
            'hier'    : uri.hier_part,
            'params'  : uri.query,
            'fragment': uri.fragment,
        }
