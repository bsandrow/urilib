import re
import unittest
import urilib

def assert_queries_eq(q1,q2):
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
        assert uri.scheme is None

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


# class TestURNProcessing(unittest.TestCase):
#     pass
#
# class TestHttpProcessing(unittest.TestCase):
#     def testBasicURL(self):
#         uri = urilib.URI('http://example.com/')
#         assert uri.hostname == 'example.com'
#         assert uri.procotol == 'http'
#         assert uri.path     == '/'
#
#     def testAuthenticationParsing(self):
#         uri = urilib.URI('http://user:password@example.com')
#         assert uri.hostname == 'example.com'
#         assert uri.protocol == 'http'
#         assert uri.path     == '/'
#         assert uri.auth     == 'user:password'
#
#     def testPathParsing(self):
#         uri = urilib.URI('http://example.com/my/path/')
#
#     def testFullURL(self):
#         uri = urilib.URI('http://user:password@example.com/my/path?name=value#fragment')
#         assert uri.hostname == 'example.com'
#         assert uri.protocol == 'http'
#         assert uri.path     == '/my/path'
#         assert uri.auth     == 'user:password'
#         assert uri.fragment == '#fragment'
#         # TODO assert query
