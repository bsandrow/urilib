"""\
QueryDict - A dict sub-class for dealing with the query part of the URI

I've chosen to implement a similar interface to Django's QueryDict. After much
internal struggle trying to figure out what the best interface is, someone
pointed me at Django's QueryDict. This seems to be much of what I want:

- Accessing `qd['key']` returns the last element rather than the list of all
  elements. If it always returned a list, then you would need to do things like
  check the length of the list prior to accessing it in the most common case
  (accessing a key with only a single value).

- There is a separate suite of methods just for access to the actual list of
  values under a key.

It's also missing things that I would want:

- Passing a list of 2-tuples to update() and have them all assigned correctly
  into their respective key-lists. It doesn't look like Django's QueryDict has
  a way to append multiple values under a key that currently has values. I'm
  thinking that Django's 'solution' to this would be to pull out the list with
  getlist(key), append the values to the list, and reset the list with
  setlist(key). Something like: ::

    qd.setlist(key, qd.getlist(key) + [ new_value_1, new_value_2 ])

  or: ::

    qd[key] = new_value_1
    qd[key] = new_value_2

  whereas something like: ::

    pairs = [ (key, v) for v in [ new_value_1, new_value_2 ] ]
    qd.update(pairs)

  might make more sense.

Disclaimer: Though this shares the same name as the Django data structure, I
take no shame in this as I independently thought of this name before I knew
about the Django structure (and the name isn't all that creative). Though, if
need be I could always name it QueryMeHarder as an homage to Richard Stallman's
hatred of POSIX (i.e. the POSIXLY_CORRECT variable was originally to be named
POSIX_ME_HARDER, but Stallman was desuaded ). ;-)
"""
# and now, the code...

import copy
import urllib

# XXX urlencode() ??

class QueryParseError(Exception):
    pass

class QueryDict(dict):
    """ QueryDict - """

    safe_chars = ':@!$&\'()*,;=~-._'

    def __init__(self, query_string, plus_is_space=False, separator='&'):
        dict.__init__(self)
        self.plus_is_space = plus_is_space

        pairs = query_string.split(separator)

        if query_string == '':
            return
        else:
            for pair in pairs:
                key, equals, value = pair.partition('=')

                if equals is None:
                    raise QueryParseError("Unable to parse key-value pair from: %s" % pair)

                key = self.url_unquote(key)
                value = self.url_unquote(value)

                self[key] = value

    def url_quote(self, string):
        """\
        url quote a string

        Turn specific values into percent-encoded hex values. Uses
        self.plus_is_space to determine if pluses should be spaces or not (as
        per HTML form data).
        """
        quote  = urllib.quote
        kwargs = { 'safe': self.safe_chars + '+' }

        if self.plus_is_space:
            quote = urllib.quote_plus
            kwargs['safe'] = self.safe_chars

        return quote(string, **kwargs)

    def url_unquote(self, string):
        """\
        url unquote a string

        Returns string with all of the precent-encoded hex values decoded back
        into their character values.  Uses self.plus_is_space to determine if
        pluses should be spaces or not (as per HTML form data).
        """
        unquote = urllib.unquote

        if self.plus_is_space:
            unquote = urllib.unquote_plus

        return unquote(string)

    def getlist(self, key):
        """ Return the list of values for :key: """
        return dict.__getitem__(self, key)

    def setlist(self, key, list):
        """ Replace all values for :key: with values in :list: """
        dict.__setitem__(self, key, list)

    def appendlist(self, key, value):
        """ Append :value: to the list of values for :key: """
        dict.__getitem__(self, key).append(value)

    def setdefault(self, key, default=None):
        if key not in self:
            self.__setitem__(key, default)

    def setlistdefault(self, key, default=None):
        """\
        Version of setdefaut that operates at the list level (default
        defaults to [])
        """
        if key not in self:
            self.setlist(key, default or [])

        return self.getlist(key)

    def items(self):
        """\
        Return a list of key-value tuples using the __getitem__() logic to
        determine which value to return.
        """
        return [ (key, self[key]) for key in self.keys() ]

    def iteritems(self):
        """ Iterator over all key,value pairs using __getitem__ logic """
        for key in self.iterkeys():
            yield (key, self[key])

    def values(self):
        """\
        Return a list of all values (using __getitem__ logic) in the same
        order as keys().
        """
        return [ self[key] for key in self.keys() ]

    def itervalues(self):
        """\
        Return an iterator over all values (using __getitem__ logic) in the
        same order as keys().
        """
        for key in self.keys():
            yield self[key]

    def lists(self):
        """ Return a list of all value lists """
        return list(self.iterlists())

    def iterlists(self):
        """\
        Return an iterable over the list of value lists.

        Keep the ordering the same as keys()/iterkeys() to mimic dict()
        functionality.
        """
        for key in self.iterkeys():
            yield self.getlist(key)

    def copy(self):
        """ Return a deepcopy of QueryDict """
        return self.__class__(str(self))

    def __contains__(self, key):
        """ Implement ':key: in QueryDict' """
        return dict.__contains__(self, key)

    def __getitem__(self, key):
        """ Implement QueryDict[:key:] """
        dict.setdefault(self, key, [])

        item = dict.__getitem__(self, key)
        if len(item) > 0:
            return item[-1]
        else:
            # XXX Raise an exception, or just return None?
            raise KeyError

    def __setitem__(self, key, value):
        """ Implement 'QueryDict[:key:] = :value:' """
        item = dict.setdefault(self, key, [])
        item.append(value)

    def __repr__(self):
        """ Return a string representation that is eval'able """
        return "%s(%s)" % (self.__class__.__name__, repr(str(self)))

    def __str__(self):
        """ Return the string representation """
        pairs = []
        for key in self:
            for value in self.getlist(key):
                pairs.append( self.url_quote(key) + "=" + self.url_quote(value) )

        return '&'.join(pairs)

    def update(self, *args, **kwargs):
        """\
        Amend the QueryDict

        Takes one of the following: a dict, a list of 2-tuples, or a set of
        kwargs. These key-value pairs will be amended to the current QueryDict
        according to __setitem__ rules.
        """
        is_dict_call  = len(args) == 1 and isinstance(args[0], dict)
        is_tuple_call = len(args) > 0 and isinstance(args[0], list)
        is_kwargs_call= len(args) < 1 and len(kwargs.keys())

        if is_dict_call and not (is_tuple_call or is_kwargs_call):
            iterable = args[0].iteritems()
        elif is_tuple_call and not (is_dict_call or is_kwargs_call):
            iterable = args[0]
        elif is_kwargs_call and not (is_tuple_call or is_dict_call):
            iterable = kwargs.iteritems()
        else:
            raise TypeError("%s.update() takes a dict, a list of 2-tuples, or keyword args" % self.__class__.__name__)

        for k,v in iterable:
            self[k] = v

    def dict(self):
        """ Return a 'flat' dict based on QueryDict """
        return dict((k,v) for k,v in self.iteritems())

if __name__ == '__main__':
    pass
