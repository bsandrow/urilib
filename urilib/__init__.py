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

def is_valid_userinfo(userinfo):
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

    def __init__(self, uri):
        self.uri = uri
        self._parse()

    def _parse_regex(self):
        ''' Simple URI parser using a regex from the appendix of RFC 3986 '''
        uri_regex_str = r'^(([^:/?#]+):)?((//([^/?#]*))?([^?#]*))?(\?([^#]*))?(#(.*))?'
        uri_regex     = re.compile(uri_regex_str)
        match         = uri_regex.match(self.uri)
        if match is not None:
            self.scheme    = match.group(2)
            self.hier_part = match.group(3)
            self.authority = match.group(5)
            self.path      = match.group(6)
            self.query     = match.group(8)
            self.fragment  = match.group(10)

    def _parse_lexer(self):
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

    def __str__(self):
        ''' Return the full URI '''
        str = ''
        if self.scheme is not None:
            str += '%s:' % self.scheme
        if self.authority is not None:
            str += '//%s' % self.authority
        if self.path is not None:
            str += self.path
        if self.query is not None:
            str += '?%s' % self.query
        if self.fragment is not None:
            str += '#%s' % self.fragment
        return str

URI._parse = URI._parse_regex

class URIQuery(dict):
    def __init__(self, query=None, separator='&'):
        if type(separator) != str:
            raise ValueError('Expected separator to be a string, got %s' % str(type(separator)))
        self.separator = separator

        if query is None:
            dict.__init__(self)
        elif type(query) is dict:
            dict.__init__(self, query)
        else:
            dict.__init__(self)
            self.split_query_string(query)

    def __str__(self):
        self.separator.join([
            '='.join(param, value)
                for param,values in self.iteritems()
                    for value in values
        ])

    def del_by_name_value(self, name, value, max=None):
        count = 0
        for i, v in enumerate(self[name]):
            if v == value:
                del self[name][i]
                count += 1
                if max is not None and count >= max:
                    return

    def split_query_string(self, query):
        for pair in query.split(self.separator):
            if pair == '':
                continue
            k,v = pair.split('=')
            if k in self:
                self[k].append(v)
            else:
                self[k] = [v]

class URL(URI):
    query_separator = '&'

    def get_query_as_dict(self):
        return dict(
            kvpair.split('=')
                for kvpair in self.query.split(self.query_separator)
        )

    def set_query_from_dict(self, d):
        self.query = self.query_separator.join(
            [ '%s=%s' % (k,v) for k,v in d.iteritems() ]
        )

class URIParseError(Exception):
    ''' An exception during processing of a URI '''
