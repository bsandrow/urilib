import re

uri_scheme_re   = r'[^\W_0-9]([^\W_]|[+\-.])*'
uri_fragment_re = r"([\w\d\-._~!$&'()*+,;=/?:@]|%[a-z0-9]{2})*"
uri_query_re    = r"([\w\d\-._~!$&'()*+,;=/?:@]|%[a-z0-9]{2})*"
uri_userinfo_re = r"([\w\-._~]|%[a-z0-9]{2}|%{2}|[!$&'()*+,;=]|:)*" # unreserved | pct-encoded | sub-delmins | :

def is_valid_scheme(scheme):
    '''
    Verify that the scheme meets the following spec (from RFC 3986):
        scheme      = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
    '''
    valid_scheme_re = re.compile(r'^%s$' % uri_scheme_re, re.I | re.U)
    return valid_scheme_re.match(scheme) is not None

def is_valid_fragment(fragment):
    '''
    Verify that the fragment meets the following spec (from RFC 3986):
        fragment      = *( pchar / "/" / "?" )
        pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
        pct-encoded   = "%" HEXDIG HEXDIG
        unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
        sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                      / "*" / "+" / "," / ";" / "="
    '''
    valid_fragment_re = re.compile(r'^%s$' % uri_fragment_re, re.I | re.U)
    return valid_fragment_re.match(fragment) is not None

def is_valid_query(query):
    valid_query_re = re.compile(r'^%s$' % uri_query_re, re.I | re.U)
    return valid_query_re.match(query) is not None

def is_valid_userinfo(cls, userinfo):
    ''' Verify that the userinfo meets the spec laid out in RFC 3986:
        userinfo      = unreserved / pct-encoded / sub-delims / ":"
        pct-encoded   = "%" HEXDIG HEXDIG
        unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
        sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                      / "*" / "+" / "," / ";" / "="
    '''
    return re.compile(r'^%s$' % uri_userinfo_re, re.I | re.U).match(userinfo) is not None

class URI(object):
    scheme   = None
    hier_part= None
    query    = None
    fragment = None
    path     = None
    authority= None

    def __init__(self, uri, scheme=None):
        self.uri = uri
        self._decompose_uri(scheme=scheme)

    def _decompose_uri(self, scheme=None):
        ''' Decompose the URI into it's component parts according to RFC 3986:
                URI           = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
                hier-part     = "//" authority path-abempty
                              / path-absolute
                              / path-rootless
                              / path-empty
                path          = path-abempty    ; begins with "/" or is empty
                              / path-absolute   ; begins with "/" but not "//"
                              / path-noscheme   ; begins with a non-colon segment
                              / path-rootless   ; begins with a segment
                              / path-empty      ; zero characters
                path-abempty  = *( "/" segment )
                path-absolute = "/" [ segment-nz *( "/" segment ) ]
                path-noscheme = segment-nz-nc *( "/" segment )
                path-rootless = segment-nz *( "/" segment )
                path-empty    = 0<pchar>
                segment       = *pchar
                segment-nz    = 1*pchar
                segment-nz-nc = 1*( unreserved / pct-encoded / sub-delims / "@" )
                              ; non-zero-length segment without any colon ":"

                pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
        '''
        buffer = self.uri
        if scheme is None:
            parts = buffer.split(u':', 1)
            if len(parts) > 1 and is_valid_scheme(parts[0]):
                (self.scheme, buffer) = parts
        else:
            self.scheme = scheme

        parts = buffer.split('#', 1)
        if len(parts) > 1 and is_valid_fragment(parts[1]):
            self.fragment = parts[1]
            buffer        = parts[0]

        parts = buffer.split('?', 1)
        if len(parts) > 1 and is_valid_query(parts[1]):
            self.query  = parts[1]
            buffer      = parts[0]

        self.hier_part = buffer

        if buffer.startswith('//'):
            buffer = buffer[2:]
            parts = buffer.split('/', 1)
            self.authority = parts[0]
            if len(parts) > 1:
                self.path = '/' + parts[1]
        else:
            self.path = buffer

    def __str__(self):
        ''' Return the full URI '''
        return self.scheme + ':' + self.scheme_specific_part

class URIParseError(Exception):
    ''' An exception during processing of a URI '''
