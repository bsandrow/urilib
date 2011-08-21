import unittest
import urilib

class TestURI(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testIsValidScheme(self):
        ''' Test that URI.is_valid_scheme() returns a boolean verifying that
        the string passed in is valid as the scheme part of the URI '''

        assert urilib.URI.is_valid_scheme('http')  == True

        assert urilib.URI.is_valid_scheme('ftp1')  == True
        assert urilib.URI.is_valid_scheme('f1tp')  == True
        assert urilib.URI.is_valid_scheme('ftp2')  == True
        assert urilib.URI.is_valid_scheme('0http') == False
        assert urilib.URI.is_valid_scheme('f9tp')  == True

        assert urilib.URI.is_valid_scheme('http.') == True
        assert urilib.URI.is_valid_scheme('http+') == True
        assert urilib.URI.is_valid_scheme('http-') == True

        assert urilib.URI.is_valid_scheme('ht.tp') == True
        assert urilib.URI.is_valid_scheme('ht+tp') == True
        assert urilib.URI.is_valid_scheme('ht-tp') == True

        assert urilib.URI.is_valid_scheme('.http') == False
        assert urilib.URI.is_valid_scheme('-http') == False
        assert urilib.URI.is_valid_scheme('+http') == False

        assert urilib.URI.is_valid_scheme('htt_p') == False
