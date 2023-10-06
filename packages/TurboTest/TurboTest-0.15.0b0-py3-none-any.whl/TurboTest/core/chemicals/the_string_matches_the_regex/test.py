import unittest
from . import the_string_matches_the_regex

from TurboTest.constants import C
from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


class Test__the_string_matches_the_regex(unittest.TestCase):

    def test_increase_nChemical(self):

        n0 = Container.nChemical
        the_string_matches_the_regex('1.2.3', r'^\d+\.\d+\.\d+$')
        n1 = Container.nChemical
        self.assertEqual(n1-n0, 1)

    def test_passes(self):
        
        the_string_matches_the_regex('1.2.3', r'^\d+\.\d+\.\d+$')
        the_string_matches_the_regex('12.34.567', r'^\d+\.\d+\.\d+$')
        
        the_string_matches_the_regex('aaa', r'\w{3}')
        the_string_matches_the_regex('a', r'\w{1,3}')
        the_string_matches_the_regex('aa', r'\w{1,3}')
        the_string_matches_the_regex('aaa', r'\w{1,3}')

        the_string_matches_the_regex('abcd', r'abc.')
        the_string_matches_the_regex('abcx', r'abc.')
        the_string_matches_the_regex('abcy', r'abc.')

        ## Date
        the_string_matches_the_regex('2023-01-01', r'^\d{4}-\d{2}-\d{2}$')

        ## URLs
        regex_pattern = r'^https?://(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        url = "https://www.example.com"
        the_string_matches_the_regex(url, regex_pattern)
        url = "http://example.co"
        the_string_matches_the_regex(url, regex_pattern)

    def test_fails(self):

        the_string = ''
        the_regex = r'^\d+\.\d+\.\d+$'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")

        the_string = '1.2'
        the_regex = r'^\d+\.\d+\.\d+$'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")

        the_string = '1-2-3'
        the_regex = r'^\d+\.\d+\.\d+$'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")


        the_string = 'a'
        the_regex = r'\w{3}'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")

        the_string = '123'
        the_regex = r'\w{3}'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")


        the_string = ''
        the_regex = r'\w{1,3}'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")

        the_string = 'abcd'
        the_regex = r'\w{1,3}'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")


        the_string = 'abc'
        the_regex = r'abc.'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")

        the_string = 'abcde'
        the_regex = r'abc.'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")


        ## Date
        the_string = 'abc'
        the_regex = r'^\d{4}-\d{2}-\d{2}$'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")


        ## <URLs>
        the_string = 'https://'
        the_regex = r'^https?://(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")
        
        the_string = 'abc://foo.com'
        the_regex = r'^https?://(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {repr(the_string)}")
        ## </URLs>

        ## Really long input string
        the_string = 'a'*(C.REPORT_LEN//2) + 'b'*123 + 'c'*(C.REPORT_LEN//2)
        the_regex = r'^\w{10}$'
        with self.assertRaises(ErrorTT) as ctx: the_string_matches_the_regex(the_string, the_regex)
        str_report = "'" + 'a'*(C.REPORT_LEN//2 - 1) + '...\n\n   [125 more chars]\n\n...' + 'c'**(C.REPORT_LEN//2 - 1) + "'"
        self.assertEqual(str(ctx.exception), f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n  the_string: {str_report}")


if __name__ == '__main__':
    unittest.main()
