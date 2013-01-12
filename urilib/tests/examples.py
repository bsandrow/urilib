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
