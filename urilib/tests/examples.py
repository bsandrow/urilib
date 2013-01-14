"""\
Unit Testing the Documentation Examples

Let's make sure that the examples actually work, because first impressions mean
something.
"""

import unittest

import urilib

class ConstructingAUri(unittest.TestCase):
    def test(self):
        uri = urilib.uri()

        uri.scheme = 'https'
        uri.authority = 'www.google.com:443'
        uri.path = '/'

        self.assertEqual( str(uri), 'https://www.google.com:443/' )

        uri.query.update({'q': 'urilib', 'sourceid': 'chrome', 'ie': 'UTF-8' })

        self.assertEqual( str(uri), 'https://www.google.com:443/?q=urilib&sourceid=chrome&ie=UTF-8' )

class Deconstruction(unittest.TestCase):
    def test(self):
        uri = urilib.uri('http://www.google.ca/search?sourceid=chrome&client=ubuntu&channel=cs&ie=UTF-8&q=urilib')

        self.assertEquals(uri.scheme, 'http')
        self.assertEquals(uri.authority, 'www.google.ca')
        self.assertEquals(uri.path, '/search')
        self.assertEquals(uri.fragment, '')
        self.assertEquals(str(uri.query), 'sourceid=chrome&q=urilib&client=ubuntu&ie=UTF-8&channel=cs')

class AddQueryParam(unittest.TestCase):
    def test(self):
        uri = urilib.uri('http://www.example.com/?q=urilib')

        uri.query.update({'q': 'urlparse'})
        self.assertEquals(str(uri), 'http://www.example.com/?q=urilib&q=urlparse')

        uri.query['q'] = 'Bob'
        uri.query['q'] = 'Nancy'
        self.assertEquals(str(uri), 'http://www.example.com/?q=urilib&q=urlparse&q=Bob&q=Nancy')

class AccessQueryParams(unittest.TestCase):
    def test(self):
        uri = urilib.uri('http://www.example.com/?q=urilib&q=urlparse&lang=en')

        self.assertEquals(uri.query['lang'], 'en')
        self.assertEquals(uri.query['q'], 'urlparse')
        self.assertEquals(uri.query.getlist('q'), ['urilib', 'urlparse'])


