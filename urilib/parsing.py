""" urilib.parsing - Pay no attention to the man behind the curtain

This is where the magic happens. I want to play with various implementations,
so I'm abstracting the parsing portion away into here and creating machinery
the allow switching between parsing methods.

Switching between methods shouldn't be too useful in day-to-day usage, but it
will make it easier for me to run performance tests against various methods.

All parsing methods should implement the API of taking a single parameter --
the URI -- and outputing a UriParts tuple.
"""

import collections
import re

# -------------
# API Machinery
# -------------
UriParts = collections.namedtuple('UriParts', 'scheme authority path query fragment')

current_parser = 'basic'
parsers = {
    'basic': lambda x: basic_parser(x),
    'rfc'  : lambda x: rfc_parser(x),
}

def parse_uri(uri):
    return parsers[current_parser](uri)

# ------------
# Basic Parser
# ------------
scheme_re = re.compile(r'[^\W0-9_]([^\W_]|[+.-])*')

def scheme_is_valid(scheme):
    """ Return True/False result of SCHEME validation. """
    m = scheme_re.match(scheme)
    return m is not None

def basic_parser(uri):
    """ A very basic URI parser

    Done with smoke and mirrors^W^W^W strategic string splitting.
    """
    scheme    = None
    authority = None
    path      = None
    query     = None
    fragment  = None
    unparsed  = uri

    parts = unparsed.partition(':')
    if parts[2] is not None and scheme_is_valid(parts[0]):
        scheme, unparsed = parts[::2]

    parts = unparsed.partition('#')
    unparsed, fragment = parts[::2]

    parts = unparsed.partition('?')
    if parts[1]:
        unparsed, query = parts[::2]

    if unparsed.startswith('//'):
        unparsed = unparsed[2:]
        parts = unparsed.partition('/')
        if parts[2] is not None:
            authority = parts[0]
            path = ''.join(parts[1:])
        else:
            path = parts[0]
    else:
        path = unparsed

    return UriParts(scheme, authority, path, query, fragment)

# ----------
# RFC Parser
# ----------
rfc_re = re.compile(r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')

def rfc_parser(uri):
    """ Using a basic regex referenced in RFC-3986 Page 51. """
    m = rfc_re.match(uri)
    if m is None:
        return UriParts(None, None, None, None, None)
    else:
        return UriParts(m.group(2), m.group(4), m.group(5), m.group(7), m.group(9))

