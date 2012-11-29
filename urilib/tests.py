import unittest

from urilib.uri import URI

class UriParsing(unittest.TestCase):
    def test_scheme_abs_url_with_port(self):
        uri = URI('http://example.com:80')
        self.assertEquals(uri.scheme, 'http')

    def test_scheme_relative_url_with_port(self):
        uri = URI('//example.com:80')
        self.assertEquals(uri.scheme, None)

    def test_scheme_invalid_url(self):
        uri = URI('example.com:80')
        self.assertEquals(uri.scheme, 'example.com')

    def test_scheme_urn(self):
        uri = URI('urn:example:monkey:toes')
        self.assertEquals(uri.scheme, 'urn')

    def test_scheme_magnet_uri(self):
        uri = URI('magnet:?xt=urn:md5:ABCDEACNDE')
        self.assertEquals(uri.scheme, 'magnet')

    def test_scheme_name_with_dash(self):
        uri = URI('scheme-name://example.com')
        self.assertEquals(uri.scheme, 'scheme-name')

    def test_scheme_name_with_plus(self):
        uri = URI('scheme+name://example.com')
        self.assertEquals(uri.scheme, 'scheme+name')

    def test_scheme_name_with_dot(self):
        uri = URI('scheme.name://example.com')
        self.assertEquals(uri.scheme, 'scheme.name')

    def test_fragment(self):
        uri = URI('http://example.com?var1=value&var2=Value2#var3=$value')
        self.assertEquals(uri.fragment, 'var3=$value')

    def test_fragment_double_hash(self):
        uri = URI('http://example.com?var1=value&var2=Value2#me-and-my-#fragment')
        self.assertEquals(uri.fragment, 'me-and-my-#fragment')

    def test_query(self):
        uri = URI('http://example.com?q=how+do+i+program+my+vcr')
        self.assertEquals(str(uri.query), 'q=how+do+i+program+my+vcr')

    def test_query_qmark_in_query(self):
        uri = URI('http://example.com?q=how+do+i+program+my+vcr?')
        self.assertEquals(str(uri.query), 'q=how+do+i+program+my+vcr?')

    def test_query_qmark_in_fragment(self):
        uri = URI('http://example.com?q=how+do+i+program+my+vcr?#why-do-i-care?')
        self.assertEquals(str(uri.query), 'q=how+do+i+program+my+vcr?')

    def test_query_no_query(self):
        uri = URI('http://example.com/#Fragment')
        self.assertEquals(uri.query, None)

    def test_query_empty_query(self):
        uri = URI('http://example.com/?#Fragment')
        self.assertEquals(str(uri.query), '')

    def test_full_uri_rfc_example(self):
        uri = URI('http://www.ics.uci.edu/pub/ietf/uri/#Related')
        self.assertEquals(uri.scheme, 'http')
        self.assertEquals(uri.authority, 'www.ics.uci.edu')
        self.assertEquals(uri.path, '/pub/ietf/uri/')
        self.assertEquals(uri.fragment, 'Related')
        self.assertEquals(uri.query, None)
