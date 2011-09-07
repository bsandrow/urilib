import re
import urilib.regex
import urilib.tools

class URI(object):
    scheme   = None
    hier_part= None
    query    = None
    fragment = None
    path     = None
    authority= None

    def __init__(self, uri, query_separator='&'):
        self.query_separator = query_separator
        self.uri = uri
        self._parse()

    def _parse_regex(self):
        ''' Use a simple regex to parse the uri. Borrowed from the appendix of RFC 3986 '''
        uri_regex     = re.compile(urilib.regex.simple_uri_regex)
        match         = uri_regex.match(self.uri)
        if match is not None:
            self.scheme    = match.group(2)
            self.hier_part = match.group(3)
            self.authority = match.group(5)
            self.path      = match.group(6)
            if match.group(8) is None:
                self.query = None
            else:
                self.query = Query(match.group(8), separator=self.query_separator)
            self.fragment  = match.group(10)

    def _parse_lexer(self):
        ''' Use a lexer to parse the uri. Coming soon to a parser near you... '''

    def __str__(self):
        ''' Join the full URI back together an return it. '''
        str = ''
        if self.scheme is not None:
            str += '%s:' % self.scheme
        if self.authority is not None:
            str += '//%s' % self.authority
        if self.path is not None:
            str += self.path
        if self.query is not None:
            str += '?%s' % self.query.__str__()
        if self.fragment is not None:
            str += '#%s' % self.fragment
        return str

URI._parse = URI._parse_regex

class Query(dict):
    ''' A way to handle queries in a dict-like manner. Rather than just using a couple of functions
    to join/split dicts into query strings, I created a customizable object to deal with them. Since
    it is sub-classed right off of dict() it should be functionally equivalent. This is especially
    useful for dealing with the fact that query strings can have multiple values for the same key.
    This is a use-case that plain dict()'s don't handle well without the additional handling that
    I've added here. '''

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
        ''' Convert back into a query string. '''
        pairs = [ 
            '='.join([param, value])
                for param,values in self.iteritems()
                    for value in values
        ]

        return self.separator.join(pairs)

    def del_by_name_value(self, name, value, max=None):
        ''' Delete all entries under the param `name` where the value is equal to `value`. The
        optional `max` parameter controls how many value matches to remove. '''
        count = 0
        for i, v in enumerate(self[name]):
            if v == value:
                del self[name][i]
                count += 1
                if max is not None and count >= max:
                    return

    def split_query_string(self, query):
        ''' Set the query string directly. This will append all key-value pairs from the query to
        the current key-value pairs in the Query's dict. '''
        for pair in query.split(self.separator):
            if pair == '':
                continue
            k,v = pair.split('=')
            if k in self:
                self[k].append(v)
            else:
                self[k] = [v]

class URL(URI):
    pass

class URIParseError(Exception):
    ''' An exception during processing of a URI '''
