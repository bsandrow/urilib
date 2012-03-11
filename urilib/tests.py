import re
import unittest
import urilib
import urlparse

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

    def testAgainstUrlParseHttp(self):
        test_url = 'http://user:password@yahoo.com:8080/path/to/blog/?postid=20#Body'
        url_parse_result = urlparse.urlparse(test_url)
        uri_result       = urilib.URI(test_url)

        assert url_parse_result.scheme   == uri_result.scheme
        assert url_parse_result.netloc   == uri_result.authority
        assert url_parse_result.path     == uri_result.path
        assert url_parse_result.query    == uri_result.query
        assert url_parse_result.fragment == uri_result.fragment

    def testAgainstUrlParseUrn(self):
        test_urn = 'urn:example:monkey:toes'
        url_parse_result = urlparse.urlparse(test_urn)
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

