import re
import unittest
import urilib

try:
    from urlparse import urlparse
except ImportError:
    from urllib import urlparse

class TestBasicProcessing(unittest.TestCase):
    """A few basic tests on operating conditions that don't fit anywhere else"""

    def testStripsWhitespace(self):
        uri = urilib.URI('  http://example.com \t')
        assert str(uri) == 'http://example.com'

    def testRepr(self):
        uri = urilib.URI('http://example.com')
        assert uri.__repr__() == "<URI('http://example.com')>"

    def testUriReconstruction(self):
        uri = urilib.URI('http://example.com/blog?id=12#Section-2')
        assert str(uri) == 'http://example.com/blog?id=12#Section-2'

        uri.scheme   = 'ftp'
        uri.fragment = 'Section-3'
        assert str(uri) == 'ftp://example.com/blog?id=12#Section-3'

class TestCompareAgainstUrlParse(unittest.TestCase):

    def testAgainstUrlParsePathOnly(self):
        test_url = "/usr/local/etc/ssh_config"
        url_parse_result = urlparse(test_url)
        uri_result       = urilib.URI(test_url)

        assert url_parse_result.scheme   == uri_result.scheme
        assert url_parse_result.netloc   == uri_result.authority
        assert url_parse_result.path     == uri_result.path
        assert url_parse_result.query    == uri_result.query
        assert url_parse_result.fragment == uri_result.fragment

    def testAgainstUrlParseSchemeless(self):
        test_url = '://example.com/'
        url_parse_result = urlparse(test_url)
        uri_result       = urilib.URI(test_url)

        assert url_parse_result.scheme   == uri_result.scheme
        assert url_parse_result.netloc   == uri_result.authority
        assert url_parse_result.path     == uri_result.path
        assert url_parse_result.query    == uri_result.query
        assert url_parse_result.fragment == uri_result.fragment

    def testAgainstUrlParseHttp(self):
        test_url = 'http://user:password@yahoo.com:8080/path/to/blog/?postid=20#Body'
        url_parse_result = urlparse(test_url)
        uri_result       = urilib.URI(test_url)

        assert url_parse_result.scheme   == uri_result.scheme
        assert url_parse_result.netloc   == uri_result.authority
        assert url_parse_result.path     == uri_result.path
        assert url_parse_result.query    == uri_result.query
        assert url_parse_result.fragment == uri_result.fragment

    def testAgainstUrlParseUrn(self):
        test_urn = 'urn:example:monkey:toes'
        url_parse_result = urlparse(test_urn)
        uri_result       = urilib.URI(test_urn)

        assert url_parse_result.scheme   == uri_result.scheme
        assert url_parse_result.netloc   == uri_result.authority
        assert url_parse_result.path     == uri_result.path
        assert url_parse_result.query    == uri_result.query
        assert url_parse_result.fragment == uri_result.fragment

class TestSchemeProcessing(unittest.TestCase):
    """ Test the processing of the URI scheme """

    def testSchemeHttp(self):
        uri = urilib.URI('http://example.com')
        assert uri.scheme == 'http'

    def testSchemeUrn(self):
        uri = urilib.URI('urn:isbn:000123134325')
        assert uri.scheme == 'urn'

    def testSchemeSpecialChars(self):
        uri = urilib.URI('test-scheme+more://example.com')
        assert uri.scheme == 'test-scheme+more'

        uri = urilib.URI('test.scheme.more://example.com')
        assert uri.scheme == 'test.scheme.more'

        uri = urilib.URI('-test-scheme://example.com')
        assert uri.scheme == ""

class TestHierPartProcessing(unittest.TestCase):
    """ Test that the hier part (authority + path) is processed correctly """

    def testHierPartUrn(self):
        uri = urilib.URI('urn:isbn:0123456789012')
        assert uri.hier_part == 'isbn:0123456789012'

    def testHierPartHttp(self):
        uri = urilib.URI('http://user:password@example.com/blog/')
        assert uri.hier_part == '//user:password@example.com/blog/'

        uri = urilib.URI('http://user:password@example.com/blog/?key=value')
        assert uri.hier_part == '//user:password@example.com/blog/'

        uri = urilib.URI('http://user:password@example.com/blog/#section-2.2')
        assert uri.hier_part == '//user:password@example.com/blog/'

        uri = urilib.URI('http://user:password@example.com/blog/?key=value#section-2.2')
        assert uri.hier_part == '//user:password@example.com/blog/'

class TestQueryDict(unittest.TestCase):
    """Test out the QueryDict class interface"""

    def testStringify(self):
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')
        assert str(d) == 'key1=value1&key2=value2&key1=value3'

        d.append(('key4=value6'))
        assert str(d) == 'key1=value1&key2=value2&key1=value3&key4=value6'

        d.append(('key%206=value7'))
        assert str(d) == 'key1=value1&key2=value2&key1=value3&key4=value6&key%206=value7'

        del d['key1']
        assert str(d) == 'key2=value2&key4=value6&key%206=value7'

    def testInOperator(self):
        d = urilib.QueryDict('key1=value1&key2=value2')
        assert 'key1' in d
        assert 'key2' in d

    def testListFunctionality(self):
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')
        assert d.list() == [ ('key1','value1'), ('key2','value2'), ('key1','value3') ]

    def testAppendFunctionality(self):
        """Assert QueryDict.append() works correctly"""
        d = urilib.QueryDict("key1=value1")
        assert d.list() == [ ('key1','value1') ]

        # Append via query string
        d.append("key2=value2&key3=value3")
        assert d.list() == [
            ('key1','value1'),
            ('key2','value2'),
            ('key3','value3'),
        ]

        # Append via list of tuples
        d.append([ ('key4','value4'), ('key6','value8') ])
        assert d.list() == [
            ('key1','value1'),
            ('key2','value2'),
            ('key3','value3'),
            ('key4','value4'),
            ('key6','value8'),
        ]

        # Append via keyword args
        d.append(key5="value3")
        assert d.list() == [
            ('key1','value1'),
            ('key2','value2'),
            ('key3','value3'),
            ('key4','value4'),
            ('key6','value8'),
            ('key5','value3'),
        ]

    def testDeleteFunctionality(self):
        """Testing 'del d[]' functionality"""
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')

        assert d.list() == [ ('key1','value1'), ('key2','value2'), ('key1','value3') ]

        del d['key1']

        assert d.list() == [ ('key2','value2') ]

    def testBracketAccess(self):
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')

        # Multi-value keys, return only the first value
        assert d['key1'] == 'value1'

        # KeyError thrown on non-existent key
        keyerror_was_thrown = False
        try:
            d['key3']
        except KeyError:
            keyerror_was_thrown = True

        assert keyerror_was_thrown

    def testKeysAndValuesAreUnquoted(self):
        """Assert that the query keys and values are URL decoded."""

        d = urilib.QueryDict("key%201=Value%201&key%202=Value%203")

        assert 'key 1' in d
        assert 'key 2' in d

        assert d['key 1'] == 'Value 1'
        assert d['key 2'] == 'Value 3'

    def testInitializesMultiValuedKeysCorrectly(self):
        d = urilib.QueryDict("key=1&key=2")
        assert 'key' in d
        assert d.get_all('key')[0] == "1"
        assert d.get_all('key')[1] == "2"

    def testGettingAllValuesForMultiValuedKey(self):
        d = urilib.QueryDict("key=1&key=2")
        assert 'key' in d
        assert d.get_all('key')[0] == "1"
        assert d.get_all('key')[1] == "2"

    def testKeys(self):
        """Assert keys() method"""
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')
        assert d.keys() == ['key2', 'key1']

    def testValues(self):
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')
        assert d.values() == ['value1','value2','value3']

    def testDict(self):
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')
        assert d.dict() == { 'key1': 'value1', 'key2': 'value2' }

    def testGet(self):
        d = urilib.QueryDict('key1=value1&key2=value2&key1=value3')
        assert d.get('key1', None) == 'value1'
        assert d.get('key1', 'value2') == 'value1'
        assert d.get('key1') == 'value1'
        assert d.get('key3', None) is None
        assert d.get('key3', 'value5') == 'value5'

    def testGetAll(self):
        pass
