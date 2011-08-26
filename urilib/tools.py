import urilib.regex
import re

def is_valid_scheme(scheme):
    ''' Verify that the scheme meets the spec from RFC 3986 '''
    scheme_re = re.compile(r'^%s$' % urilib.regex.scheme, re.I | re.U)
    return scheme_re.match(scheme) is not None

def is_valid_fragment(fragment):
    ''' Verify that the fragment meets the spec from RFC 3986 '''
    fragment_re = re.compile(r'^%s$' % urilib.regex.fragment, re.I | re.U)
    return fragment_re.match(fragment) is not None

def is_valid_query(query):
    ''' Verify that the query meets the spec from RFC 3986 '''
    query_re = re.compile(r'^%s$' % urilib.regex.query, re.I | re.U)
    return query_re.match(query) is not None

def is_valid_userinfo(userinfo):
    ''' Verify that the userinfo meets the spec from RFC 3986 '''
    userinfo_re = re.compile(r'^%s$' % urilib.regex.userinfo, re.I | re.U)
    return userinfo_re.match(userinfo) is not None
