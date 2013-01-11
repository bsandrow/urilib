""" Unit Tests for QueryDict """

import unittest

from urilib import QueryDict

# TODO test url_unquote()

class QueryDictTesting(unittest.TestCase):
    def setUp(self):
        self.simple_query = 'a=1&b=2&c=3&d=4&a=12&b=23&a=23'
        self.pct_encoded_query = 'complex%20key=value&lang=en&q=my%20search%20terms&en=utf8'

    def test_repr(self):
        """ Check that QueryDict produces decent repr output """
        q = QueryDict(self.simple_query)
        self.assertEquals( repr(q), "QueryDict('a=1&a=12&a=23&c=3&b=2&b=23&d=4')" )

    def test_repr_empty_query(self):
        q = QueryDict('')
        self.assertEquals(repr(q), "QueryDict('')")

    def test_stringify(self):
        """ Check that QueryDict stringifies correctly """
        q = QueryDict(self.simple_query)
        self.assertEquals(str(q), 'a=1&a=12&a=23&c=3&b=2&b=23&d=4')

    def test_stringify_encoded_chars(self):
        """ Check to make sure that correct characters are %-encoded """
        q = QueryDict(self.pct_encoded_query)
        self.assertEquals(str(q), 'lang=en&q=my%20search%20terms&complex%20key=value&en=utf8')

    def test_stringify_empty_query(self):
        q = QueryDict('')
        self.assertEquals(str(q), '')

    def test_querydict_setlist(self):
        """ Check that setlist() replaces the list of values """
        q = QueryDict(self.simple_query)
        self.assertEquals(q.getlist('a'), ['1', '12', '23'])
        q.setlist('a', [2, 3])
        self.assertEquals(q.getlist('a'), [2, 3])

    def test_querydict_getlist(self):
        """ Check that getlist() returns the full list of values for a key """
        q = QueryDict(self.simple_query)
        self.assertEquals(q.getlist('a'), ['1','12','23'])
        self.assertEquals(q.getlist('b'), ['2','23'])
        self.assertEquals(q.getlist('c'), ['3'])
        self.assertEquals(q.getlist('d'), ['4'])

    def test_querydict_appendlist(self):
        """ Assert that QueryDict.appendlist() adds values to the list of values for a key """
        q = QueryDict(self.simple_query)
        self.assertEquals(q.getlist('d'), ['4'])

        q.appendlist('d', '123')
        self.assertEquals(q.getlist('d'), ['4', '123'])

    def test_querydict_setdefault__key_doesnt_exist(self):
        """ Assert QueryDict.setdefault() works when key doesn't exist """
        q = QueryDict('b=2&c=2')

        key_does_not_exist = False
        try:
            dict.__getitem__(q, 'a')
        except KeyError:
            key_does_not_exist = True

        assert key_does_not_exist, "Key 'a' exists!"

        q.setdefault('a', 1)

        self.assertEquals(q.getlist('a'), [1])

    def test_querydict_setdefault__key_does_exist(self):
        """ Assert QueryDict.setdefault() works when key does exist """
        q = QueryDict('a=1&b=2&c=2')
        self.assertEquals(q.getlist('a'), ['1'])

        q.setdefault('a', '123')
        self.assertEquals(q.getlist('a'), ['1'])

    def test_querydict_contains(self):
        """ Assert that "key in QueryDict" works correctly """
        q = QueryDict(self.pct_encoded_query)

        assert 'complex key' in q, "Could not find key 'complex key' in: %s" % repr(q)
        assert        'lang' in q, "Could not find key 'lang' in: %s" % repr(q)
        assert           'q' in q, "Could not find key 'q' in: %s" % repr(q)
        assert          'en' in q, "Could not find key 'en' in: %s" % repr(q)

    def test_querydict_getitem_for_single_value_keys(self):
        """ Assert that QueryDict[key] works when key only has a single value """
        q = QueryDict(self.simple_query)
        self.assertEquals(q['d'], "4")
        self.assertEquals(q['c'], "3")

    def test_querydict_getitem_for_multi_value_keys(self):
        """ Assert that QueryDict[key] works when key has multiple values """
        q = QueryDict(self.simple_query)
        self.assertEquals(q['a'], '23')
        self.assertEquals(q['b'], '23')

    def test_querydict_getitem_for_missing_keys(self):
        """ Assert that QueryDicy[key] works when key does not exist """
        q = QueryDict(self.simple_query)

        try:
            q['does_not_exist']
            key_error = False
        except KeyError:
            key_error = True

        assert key_error, "Accessing non-existent key did *not* raise a KeyError!"

    def test_querydict_construct_from_scratch(self):
        """ Assert that I can construct a query from an empty QueryDict() """
        q = QueryDict('')
        self.assertEquals(str(q), '')

        q['a'] = '1'
        q['complex key'] = 'value'
        self.assertEquals(str(q), 'a=1&complex%20key=value')

    def test_querydict_setitem_works_on_unused_key(self):
        """ Assert that "QueryDict[key] = value" appends the value to the list for key when key does not exist """
        q = QueryDict('')
        q['a'] = 1
        q['a'] = 2
        self.assertEquals(q.getlist('a'), [1,2])

    def test_querydict_setitem_works_on_existing_key(self):
        """ Assert that "QueryDict[key] = value" appends the value to the list for key when key does exist """
        q = QueryDict(self.simple_query)
        q['a'] = 'new_value'
        self.assertEquals(q.getlist('a'), ['1', '12', '23', 'new_value'])

    def test_querydict_setitem_appends(self):
        """ Assert that 'QueryDict[key] = value' appends value to the list for key """
        q = QueryDict(self.simple_query)
        q['a'] = 'new_value'
        self.assertEquals(q['a'], 'new_value')

    def test_querydict_url_quote_safe_chars(self):
        """ Assert that QueryDict.url_quote() correctly leaves safe characters alone """
        q = QueryDict('')

        for char in q.safe_chars:
            self.assertEquals(q.url_quote(char), char)

    def test_querydict_url_quote_unsafe_chars(self):
        """ Assert that some unsafe characters are correctly encoded """
        q = QueryDict('')

        for char in "#[]":
            expected = "%%%X" % ord(char)
            self.assertEquals(q.url_quote(char), expected)

    def test_querydict_url_quote_plus_is_space(self):
        """\
        Assert that QueryDict.url_quote() handles plus_is_space=True correctly
        """
        q = QueryDict('', plus_is_space=True)

        self.assertEquals(q.url_quote('nova scotia'), 'nova+scotia')
        self.assertEquals(q.url_quote('nova+scotia'), 'nova%2Bscotia')

    def test_querydict_url_quote_plus_is_not_space(self):
        """\
        Assert that QueryDict.url_quote() handles plus_is_space=False correctly
        """
        q = QueryDict('', plus_is_space=False)

        self.assertEquals(q.url_quote('nova scotia'), 'nova%20scotia')
        self.assertEquals(q.url_quote('nova+scotia'), 'nova+scotia')

    def test_querydict_items(self):
        """\
        Assert that QueryDict.items() returns a list of tuples of (key,
        last-value) pairs 
        """
        q = QueryDict(self.simple_query)

        # don't care about order so much as contents, so use sets for
        # comparison
        self.assertEquals(
            set(q.items()),
            set([ ('a', '23'), ('b', '23'), ('c', '3'), ('d', '4') ]),
        )

    def test_querydict_iteritems(self):
        """\
        Assert that QueryDict.iteritems() return an iterator for a list of
        (key,value) tuples
        """
        q = QueryDict(self.simple_query)

        iterator = q.iteritems()
        assert hasattr(iterator, '__iter__'), "iteritems() did not return an iteratable."

        self.assertEquals(
            set( q.iteritems() ),
            set([ ('a', '23'), ('b', '23'), ('c', '3'), ('d', '4') ]),
        )

    def test_querydict_values(self):
        """\
        Assert that QueryDict.values() returns a list of values for each
        key (using __getitem__ logic).
        """
        q = QueryDict(self.simple_query)
        self.assertEquals(q.values(), [ '23', '3', '23', '4' ])

    def test_querydict_itervalues(self):
        """\
        Assert that QueryDict.values() returns an iterator over all the values
        for each key (using __getitem__ logic).
        """
        q = QueryDict(self.simple_query)

        iterator = q.itervalues()
        assert hasattr(iterator, '__iter__'), "itervalues() did not return an iterator."

        self.assertEquals( [ v for v in q.itervalues() ], [ '23', '3', '23', '4' ])

    def test_querydict_iterlists_has_same_order_as_iterkeys(self):
        """\
        Assert that QueryDict.iterlists() returns value lists in the same order
        as iterkeys returns keys.
        """
        q = QueryDict(self.simple_query)

        iterator = q.iterlists()
        assert hasattr(iterator, '__iter__'), "iterlists() did not return an iterator."

        self.assertEquals(
            list( iterator ),
            [ q.getlist(key) for key in q.iterkeys() ]
        )

    def test_querydict_iterlists(self):
        """\
        Assert that QueryDict.iterlists() returns an iterator over all values
        lists for each key.
        """
        q = QueryDict(self.simple_query)

        iterator = q.iterlists()
        assert hasattr(iterator, '__iter__'), "iterlists() did not return an iterator."

        self.assertEquals(
            list(iterator),
            [ ['1', '12', '23'], ['3'], ['2', '23'], ['4'] ]
        )

    def test_querydict_lists(self):
        """\
        Assert that QueryDict.lists() returns a list of all values lists in an
        order the corresponds with keys()
        """
        q = QueryDict(self.simple_query)
        self.assertEquals(
            q.lists(),
            [ ['1', '12', '23'], ['3'], ['2', '23'], ['4'] ]
        )

    def test_querydict_setlistdefault_key_exists(self):
        """\
        Assert that QueryDict.setlistdefault(:key:) returns the list for :key:
        and does *not* set :key: to and empty list.
        """
        q = QueryDict(self.simple_query)

        assert 'a' in q, "Key 'a' should exist in QueryDict."

        return_value = q.setlistdefault('a')

        self.assertEquals(return_value, ['1', '12', '23'])
        self.assertEquals(q.getlist('a'), ['1', '12', '23'])

    def test_querydict_setlistdefault_key_exists_with_default(self):
        """\
        Assert that QueryDict.setlistdefault(:key:, default=:value:) returns
        the list for :key: and does *not* set :key: to :value:
        """
        q = QueryDict(self.simple_query)

        assert 'a' in q, "Key 'a' should exist in QueryDict."

        return_value = q.setlistdefault('a', default=['123'])

        self.assertEquals(return_value, ['1', '12', '23'])
        self.assertEquals(q.getlist('a'), ['1', '12', '23'])

    def test_querydict_setlistdefault_key_does_not_exist(self):
        """\
        Assert that QueryDict.setlistdefault(:key:) returns the default list
        when :key: does not exist.
        """
        q = QueryDict(self.simple_query)

        assert 'z' not in q, "Key 'z' is not supposed to exist."

        return_value = q.setlistdefault('z')

        self.assertEquals(return_value, [])
        self.assertEquals(q.getlist('z'), [])

    def test_querydict_setlistdefault_key_does_not_exist_with_default(self):
        """\
        Assert that QueryDict.setlistdefault(:key:) returns the default list
        when :key: does not exist.
        """
        q = QueryDict(self.simple_query)

        assert 'z' not in q, "Key 'z' is not supposed to exist."

        return_value = q.setlistdefault('z', default=['123'])

        self.assertEquals(return_value, ['123'])
        self.assertEquals(q.getlist('z'), ['123'])

    def test_querydict_copy(self):
        """ Assert that QueryDict.copy() returns an equivalent copy """
        q1 = QueryDict(self.simple_query)
        q2 = q1.copy()
        self.assertEquals(q1, q2)

    def test_querydict_copy_is_deep(self):
        """\
        Assert that QueryDict.copy() returns a deep copy, so modifications to
        one don't affect the other.
        """
        q1 = QueryDict(self.simple_query)
        q2 = q1.copy()

        q2.appendlist('a', '1')
        self.assertNotEqual(q1, q2)

    def test_querydict_update_kwargs(self):
        """\
        Assert that key-value pairs passed in via kwargs get appended
        correctly
        """
        q1 = QueryDict(self.simple_query)
        q1.update(a='500', c='20')

        self.assertEqual(q1.items(), [
            ('a', '500'),
            ('c', '20'),
            ('b', '23'),
            ('d', '4')
        ])

        self.assertEqual(q1.getlist('a'), ['1', '12', '23', '500'])
        self.assertEqual(q1.getlist('c'), ['3', '20'])

    def test_querydict_update_from_dict(self):
        """\
        Assert that a dict passed into update() appends key-values according to
        __setitem__ rules.
        """
        q1 = QueryDict(self.simple_query)
        q1.update({'a': '500', 'c': '20'})

        self.assertEqual(q1.items(), [
            ('a', '500'),
            ('c', '20'),
            ('b', '23'),
            ('d', '4')
        ])

        self.assertEqual(q1.getlist('a'), ['1', '12', '23', '500'])
        self.assertEqual(q1.getlist('c'), ['3', '20'])

    def test_querydict_update_from_tuple_list(self):
        """\
        Assert that a dict passed into update() appends key-values according to
        __setitem__ rules.
        """
        q1 = QueryDict(self.simple_query)
        q1.update([ ('a', '500'), ('c', '20') ])

        self.assertEqual(q1.items(), [
            ('a', '500'),
            ('c', '20'),
            ('b', '23'),
            ('d', '4')
        ])

        self.assertEqual(q1.getlist('a'), ['1', '12', '23', '500'])
        self.assertEqual(q1.getlist('c'), ['3', '20'])

    def test_querydict_update_blows_up_on_no_args(self):
        """ Assert that update() raises TypeError when there are no args """
        q = QueryDict(self.simple_query)

        try:
            q.update()
            caught_type_error = False
        except TypeError as e:
            caught_type_error = True

        self.assertTrue(caught_type_error)

    def test_querydict_update_blows_up_on_multiple_args(self):
        """ Assert that update() raises TypeError when len(args) > 1 """
        q = QueryDict(self.simple_query)

        try:
            q.update((1,1), (1,1))
            caught_type_error = False
        except TypeError as e:
            caught_type_error = True

        self.assertTrue(caught_type_error)

    def test_querydict_update_blows_up_if_arg_isnt_correct(self):
        """ Assert that update() raises TypeError if len(arg) == 1 and type(arg[0]) not in (dict, list) """
        q = QueryDict(self.simple_query)

        try:
            q.update(set('a','b'))
            caught_type_error = False
        except TypeError as e:
            caught_type_error = True

        self.assertTrue(caught_type_error)

    def test_querydict_dict_returns_a_flattened_dict(self):
        """ """
        q = QueryDict(self.simple_query)
        self.assertEqual(q.dict(), { 'a': '23', 'c': '3', 'b': '23', 'd': '4' })

__all__ = [ "QueryDictTesting" ]
