import unittest

from urilib.uri import URI

class SchemeParsing(unittest.TestCase):
    def test_abs_url_with_port(self):
        uri = URI('http://example.com:80')
        assert uri.scheme == 'http'

    def test_relative_url_with_port(self):
        uri = URI('//example.com:80')
        assert uri.scheme is None

    def test_invalid_url(self):
        uri = URI('example.com:80')
        assert uri.scheme == 'example.com'

    def test_urn(self):
        uri = URI('urn:example:monkey:toes')
        assert uri.scheme == 'urn'

    def test_magnet_uri(self):
        uri = URI('magnet:?xt=urn:md5:ABCDEACNDE')
        assert uri.scheme == 'magnet'

    def test_scheme_name_with_dash(self):
        uri = URI('scheme-name://example.com')
        assert uri.scheme == 'scheme-name'

    def test_scheme_name_with_plus(self):
        uri = URI('scheme+name://example.com')
        assert uri.scheme == 'scheme+name'

    def test_scheme_name_with_dot(self):
        uri = URI('scheme.name://example.com')
        assert uri.scheme == 'scheme.name'

class FragmentParsing(unittest.TestCase):
    def test_fragment(self):
        uri = URI('http://example.com?var1=value&var2=Value2#var3=$value')
        assert uri.fragment == 'var3=$value'

    def test_fragment_double_hash(self):
        uri = URI('http://example.com?var1=value&var2=Value2#me-and-my-#fragment')
        assert uri.fragment == 'me-and-my-#fragment'

class QueryParsing(unittest.TestCase):
    def test_query(self):
        uri = URI('http://example.com?q=how+do+i+program+my+vcr')
        assert str(uri.query) == 'q=how+do+i+program+my+vcr'

    def test_query_qmark_in_query(self):
        uri = URI('http://example.com?q=how+do+i+program+my+vcr?')
        assert str(uri.query) == 'q=how+do+i+program+my+vcr?'

    def test_query_qmark_in_fragment(self):
        uri = URI('http://example.com?q=how+do+i+program+my+vcr?#why-do-i-care?')
        assert str(uri.query) == 'q=how+do+i+program+my+vcr?'
