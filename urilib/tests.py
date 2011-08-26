import re
import unittest
import urilib

def assert_query_eq(q1,q2):
    assert len(q1.keys()) == len(q2.keys()),\
            'Expected %d params, Got %d.' % (len(q2.keys()), len(q1.keys()))
    for k,v in q1.iteritems():
        assert k in q2, 'Got unexpected param: %s' % k
        assert_lists_eq(q1[k], q2[k])

def assert_lists_eq(l1, l2, strict=True):
    if strict:
        assert type(l1) == list, 'Expected a list for arg 0, got %s.' % str(type(l1))
        assert type(l2) == list, 'Expected a list for arg 1, got %s.' % str(type(l2))
    assert len(l1) == len(l2), 'Expected %d elements, Got %d elements' % (len(l2), len(l1))
    for i, element in enumerate(l1):
        assert element == l2[i], 'At index %d, Expected \'%s\', Got \'%s\'' % (i, l2[i], element)

def assert_dicts_eq(d1,d2):
    assert type(d1) == dict, 'First argument is not a dict()'
    assert type(d2) == dict, 'Second argument is not a dict()'
    assert len(d1.keys()) == len(d2.keys()),\
            'Got %d keys. Expected %d keys.' % (len(d1.keys()), len(d2.keys()))
    for k,v in d1.iteritems():
        assert k in d2, 'Got unexpected key %s' % k
        assert d1[k] == d2[k], "'%s' != '%s'" % (d1[k], d2[k])

class TestStandalones(unittest.TestCase):
    def testIsValidFragment(self):
        ''' Testing URI.is_valid_fragment()
        returns a boolean verifying that the string passed in is valid as the
        fragment part of the URI '''

        assert urilib.tools.is_valid_fragment('#abc') == False,\
            'Asserting that a preceeding # is invalid'

        assert urilib.tools.is_valid_fragment('abc#') == False,\
            'Asserting that a trailing # is invalid'

        assert urilib.tools.is_valid_fragment('ab#c') == False,\
            'Asserting that a # in the middle is invalid'

        assert urilib.tools.is_valid_fragment('abcdefg') == True,\
            'Asserting the base case of alphabet chars'

        assert urilib.tools.is_valid_fragment("a.a_a~a!a$a&a'a(a)a*a+a,a;a=a/a?a:a@a") == True,\
            'Asserting that \'._~!$&\'()*+,;=/?:@\' are valid characters'

        assert urilib.tools.is_valid_fragment('%AF%20') == True,\
            'Asserting that uri-escaped characters are valid.'

        assert urilib.tools.is_valid_fragment("a_a'%AFa(a)a*a+a,a;%AF=a/aa") == True,\
            'Asserting that uri-escaped characters are valid mixed with other chars.'

        assert urilib.tools.is_valid_fragment('%%') == False,\
            'Asserting that escaped % is invalid.'

    def testIsValidScheme(self):
        ''' Testing URI.is_valid_scheme()
        returns a boolean verifying that the string passed in is valid as the
        scheme part of the URI '''

        assert urilib.tools.is_valid_scheme('http')  == True

        assert urilib.tools.is_valid_scheme('ftp1')  == True
        assert urilib.tools.is_valid_scheme('f1tp')  == True
        assert urilib.tools.is_valid_scheme('ftp2')  == True
        assert urilib.tools.is_valid_scheme('0http') == False
        assert urilib.tools.is_valid_scheme('f9tp')  == True

        assert urilib.tools.is_valid_scheme('http.') == True
        assert urilib.tools.is_valid_scheme('http+') == True
        assert urilib.tools.is_valid_scheme('http-') == True

        assert urilib.tools.is_valid_scheme('ht.tp') == True
        assert urilib.tools.is_valid_scheme('ht+tp') == True
        assert urilib.tools.is_valid_scheme('ht-tp') == True

        assert urilib.tools.is_valid_scheme('.http') == False
        assert urilib.tools.is_valid_scheme('-http') == False
        assert urilib.tools.is_valid_scheme('+http') == False

        assert urilib.tools.is_valid_scheme('htt_p') == False

class Query(unittest.TestCase):

    def testAlternateSeparator(self):
        ''' Test non-default separator '''
        query = urilib.Query('param=val1;param2=val3;param=val2', separator=';')
        assert_query_eq(query, {'param': ['val1', 'val2'], 'param2': ['val3'], })

    def testNonStringSeparator(self):
        ''' Test non-string separator error-handling '''
        try:
            urilib.Query(separator=dict())
        except ValueError as e:
            assert str(e) == 'Expected separator to be a string, got <type \'dict\'>'

    def testAddingSimpleQueryString(self):
        ''' Adding a simple query string '''
        query = urilib.Query('q=a&param=value')
        assert_query_eq(query, { 'q': ['a'], 'param': ['value'], })

    def testCreatingMultiValuedKey(self):
        ''' Creating a multi-valued key '''
        query = urilib.Query('param=val1&param2=val3&param=val2')
        assert_query_eq(query, {'param': ['val1', 'val2'], 'param2': ['val3'], })

    def testClearingAParam(self):
        ''' Removing all params for a specific name '''
        query = urilib.Query('param=val1&param=val2&param2=val3')
        del query['param']
        assert_query_eq(query, {'param2': ['val3']})

    def testRemovingMultipleParamsByNameAndValue(self):
        ''' Removing parameters by name-value '''
        query = urilib.Query('param=val1&param=val2&param2=val3&param=val4&param=val2')
        assert_query_eq(query, {'param':['val1', 'val2', 'val4', 'val2'], 'param2':['val3']})
        query.del_by_name_value('param', 'val2')
        assert_query_eq(query, {'param':['val1', 'val4'], 'param2':['val3']})

    def testRemovingASingleParamByNameAndValue(self):
        ''' Removing a specific name-value pair '''
        query = urilib.Query('param=val1&param=val2&param2=val3&param=val4&param=val2')
        assert_query_eq(query, {'param':['val1', 'val2', 'val4', 'val2'], 'param2':['val3']})
        query.del_by_name_value('param', 'val2', max=1)
        assert_query_eq(query, {'param':['val1', 'val4', 'val2'], 'param2':['val3']})

    def testEmptyQueryString(self):
        ''' Instantiating an empty query '''
        query = urilib.Query()
        assert len(query.keys()) == 0

        query = urilib.Query('')
        assert len(query.keys()) == 0

class URLQueryFunctions(unittest.TestCase):
    pass

class URIParsing(unittest.TestCase):
    def testURIBaseCase(self):
        ''' Test a base case URI that has most of the parts in it '''
        uri = urilib.URI('http://www.example.com/?q=test#header1')
        assert uri.scheme == 'http'
        assert uri.fragment == 'header1'
        assert str(uri.query) == 'q=test'
        assert uri.hier_part == '//www.example.com/'
        assert uri.path == '/'
        assert uri.authority == 'www.example.com'
        assert str(uri)      == 'http://www.example.com/?q=test#header1'

    def testURIWithFullyLoadedAuthority(self):
        ''' Test a URI with a fully-loaded authority section '''
        uri = urilib.URI('http://username:password@www.example.com:80/admin')
        assert uri.scheme    == 'http'
        assert uri.fragment  is None
        assert uri.query     is None
        assert uri.hier_part == '//username:password@www.example.com:80/admin'
        assert uri.path      == '/admin'
        assert uri.authority == 'username:password@www.example.com:80'
        assert str(uri)      == 'http://username:password@www.example.com:80/admin'

    def testURIBlankAuthorityFileScheme(self):
        ''' Parsing a file URI with an empty authority section '''
        uri = urilib.URI('file:///my/relative/file/uri')
        assert uri.scheme    == 'file'
        assert uri.fragment  is None
        assert uri.query     is None
        assert uri.hier_part == '///my/relative/file/uri'
        assert uri.path      == '/my/relative/file/uri'
        assert uri.authority == ''
        assert str(uri)      == 'file:///my/relative/file/uri'

    def testURINoAuthorityFileScheme(self):
        ''' Test parsing a file URI with no authority section '''
        uri = urilib.URI('file:my/relative/file/uri')
        assert uri.scheme    == 'file'
        assert uri.fragment  is None
        assert uri.query     is None
        assert uri.hier_part == 'my/relative/file/uri'
        assert uri.path      == 'my/relative/file/uri'
        assert uri.authority is None
        assert str(uri)      == 'file:my/relative/file/uri'

    def testURIOnlyPathAndScheme(self):
        ''' Test a uri that only has a path and scheme '''
        uri = urilib.URI('urn:example:animal:ferret:nose')
        assert uri.scheme    == 'urn'
        assert uri.fragment  is None
        assert uri.query     is None
        assert uri.hier_part == 'example:animal:ferret:nose'
        assert uri.path      == 'example:animal:ferret:nose'
        assert uri.authority is None
        assert str(uri)      == 'urn:example:animal:ferret:nose'

    def testURINoauthrityLoaded(self):
        ''' Test a URI with no authority section but otherwise fully loaded '''
        uri = urilib.URI('urn:example:animal:ferret:nose?sources=true#10')
        assert uri.scheme    == 'urn'
        assert uri.fragment  == '10'
        assert str(uri.query)== 'sources=true'
        assert uri.hier_part == 'example:animal:ferret:nose'
        assert uri.path      == 'example:animal:ferret:nose'
        assert uri.authority is None
        assert str(uri)      == 'urn:example:animal:ferret:nose?sources=true#10'
