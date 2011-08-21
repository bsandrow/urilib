import re

scheme_re   = re.compile(r'\w[\w0-9+\-.]*', re.IGNORECASE | re.UNICODE)
fragment_re = re.compile(r'''([\w\d\-._~!$&'()*+,;=/?:@]|%[a-z0-9]{2})*''', re.IGNORECASE | re.UNICODE)
query_re    = re.compile(r'''([\w\d\-._~!$&'()*+,;=/?:@]|%[a-z0-9]{2})*''', re.IGNORECASE | re.UNICODE)

class URI(object):

    def __init__(self, uri, scheme=None):
        self.uri = uri
        self._decompose_uri(scheme=scheme)

    @classmethod
    def is_valid_scheme(cls, scheme):
        '''
        Verify that the scheme meets the following spec (from RFC 3986):
            scheme      = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
        '''
        return scheme_re.match(scheme) is not None

    @classmethod
    def is_valid_fragment(cls, fragment):
        '''
        Verify that the fragment meets the following spec (from RFC 3986):
            fragment      = *( pchar / "/" / "?" )
            pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
            pct-encoded   = "%" HEXDIG HEXDIG
            unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
            sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                          / "*" / "+" / "," / ";" / "="
        '''
        return fragment_re.match(fragment) is not None

    @classmethod
    def is_valid_query(cls, query):
        return query_re.match(query) is not None

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
            if len(parts) > 1 and URI.is_valid_scheme(parts[0]):
                (self.scheme, buffer) = parts
        else:
            self.scheme = scheme

        if buffer.startswith('//'):
            # extract the authority part

        parts = buffer.split('?', 1)
        if len(parts)> 1 and URI.is_valid_query(parts[1]):
            pass

        # deal with the path part

        parts = buffer.split('#', 1)
        if len(parts) > 1 and URI.is_valid_fragment(parts[1]):
            (self.fragment, buffer) = parts





    def __str__(self):
        ''' Return the full URI '''
        return self.scheme + ':' + self.scheme_specific_part

class URIParseError(Exception):
    ''' An exception during processing of a URI '''
