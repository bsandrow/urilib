import re

scheme_re = re.compile(r'[a-z][a-z0-9+\-.]*', re.I)

class URI(object):

    def __init__(self, uri, scheme=None):
        self.uri = uri

        # Initially decompose via:
        #   <scheme>:<scheme-specific-part>
        self.scheme = scheme
        self._decompose_uri()
        if self.scheme is None:
            raise URIParseError('Could not determine scheme for URI')

    @classmethod
    def verify_scheme(cls, scheme):
        '''
        Verify that the scheme meets the following spec (from RFC 2396):
            scheme   = alpha *( alpha | digit | "+" | "-" | "." )

            digit    = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" |
                       "8" | "9"

            alpha    = lowalpha | upalpha

            lowalpha = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" |
                       "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" |
                       "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"

            upalpha  = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" |
                       "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" |
                       "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"

        '''
        return scheme_re.match(scheme) is not None

    def _decompose_uri(self):
        ''' Decompose a URI into its most basic top-level components via the
        following definition in RFC 2396:
            <scheme>:<scheme-specific-part> '''
        parts = self.uri.split(':', 1)
        if len(parts) > 1 and URI.verify_scheme(parts[0]):
            (self.scheme, self.scheme_specific_part) = parts
        else:
            self.scheme_specific_part = self.uri

    def __str__(self):
        ''' Return the full URI '''
        return self.scheme + ':' + self.scheme_specific_part

class URIParseError(Exception):
    ''' An exception during processing of a URI '''
