import unittest
import urilib

class TestStandalones(unittest.TestCase):
    def testIsValidFragment(self):
        ''' Testing URI.is_valid_fragment()
        returns a boolean verifying that the string passed in is valid as the
        fragment part of the URI '''

        assert urilib.is_valid_fragment('#abc') == False,\
            'Asserting that a preceeding # is invalid'

        assert urilib.is_valid_fragment('abc#') == False,\
            'Asserting that a trailing # is invalid'

        assert urilib.is_valid_fragment('ab#c') == False,\
            'Asserting that a # in the middle is invalid'

        assert urilib.is_valid_fragment('abcdefg') == True,\
            'Asserting the base case of alphabet chars'

        assert urilib.is_valid_fragment("a.a_a~a!a$a&a'a(a)a*a+a,a;a=a/a?a:a@a") == True,\
            'Asserting that \'._~!$&\'()*+,;=/?:@\' are valid characters'

        assert urilib.is_valid_fragment('%AF%20') == True,\
            'Asserting that uri-escaped characters are valid.'

        assert urilib.is_valid_fragment("a_a'%AFa(a)a*a+a,a;%AF=a/aa") == True,\
            'Asserting that uri-escaped characters are valid mixed with other chars.'

        assert urilib.is_valid_fragment('%%') == False,\
            'Asserting that escaped % is invalid.'

    def testIsValidScheme(self):
        ''' Testing URI.is_valid_scheme()
        returns a boolean verifying that the string passed in is valid as the
        scheme part of the URI '''

        assert urilib.is_valid_scheme('http')  == True

        assert urilib.is_valid_scheme('ftp1')  == True
        assert urilib.is_valid_scheme('f1tp')  == True
        assert urilib.is_valid_scheme('ftp2')  == True
        assert urilib.is_valid_scheme('0http') == False
        assert urilib.is_valid_scheme('f9tp')  == True

        assert urilib.is_valid_scheme('http.') == True
        assert urilib.is_valid_scheme('http+') == True
        assert urilib.is_valid_scheme('http-') == True

        assert urilib.is_valid_scheme('ht.tp') == True
        assert urilib.is_valid_scheme('ht+tp') == True
        assert urilib.is_valid_scheme('ht-tp') == True

        assert urilib.is_valid_scheme('.http') == False
        assert urilib.is_valid_scheme('-http') == False
        assert urilib.is_valid_scheme('+http') == False

        assert urilib.is_valid_scheme('htt_p') == False

class TestURIParsing(unittest.TestCase):
    def testURIBaseCase(self):
        ''' Test a base case URI that has most of the parts in it '''
        uri = urilib.URI('http://www.example.com/?q=test#header1')
        assert uri.scheme == 'http'
        assert uri.fragment == 'header1'
        assert uri.query == 'q=test'
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
        assert uri.query     == 'sources=true'
        assert uri.hier_part == 'example:animal:ferret:nose'
        assert uri.path      == 'example:animal:ferret:nose'
        assert uri.authority is None
        assert str(uri)      == 'urn:example:animal:ferret:nose?sources=true#10'
