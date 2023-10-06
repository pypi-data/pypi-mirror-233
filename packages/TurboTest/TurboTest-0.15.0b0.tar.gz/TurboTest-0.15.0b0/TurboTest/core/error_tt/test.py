import unittest
from . import ErrorTT

import sys


class Test__ErrorTT(unittest.TestCase):

    def test_I(self):
        def f(): raise ErrorTT
        with self.assertRaises(ErrorTT) as ctx: f()

    def test_II(self):
        def f(): raise ErrorTT('foo')
        with self.assertRaises(ErrorTT) as ctx: f()
        self.assertEqual(str(ctx.exception), "foo")

    def test_III(self):
        def f(): raise ErrorTT('foo bar')
        try: f()
        except ErrorTT as e: self.assertEqual(str(e), "foo bar")

    def test_IV(self):
        def f(): raise ErrorTT('foo bar baz')
        try: f()
        except Exception as e: self.assertEqual(str(e), 'foo bar baz')

    def test_V(self):
        try:
            try:
                raise ErrorTT('hi 123')
            except ValueError:
                raise AssertionError("this exception should never rise")
        except ErrorTT as e:
            self.assertEqual(str(e), 'hi 123')

    def test_to_ensure_ErrorTT_accepts_only_1_arg(self):

        # raise NotImplementedError('Testing purposes')

        with self.assertRaises(TypeError) as ctx: raise ErrorTT('foo', 123)
        if (sys.version_info.major == 3) and (sys.version_info.minor in [8, 9]):
            self.assertEqual(str(ctx.exception), "__init__() takes from 1 to 2 positional arguments but 3 were given")
        elif (sys.version_info.major == 3) and (sys.version_info.minor in [10, 11]):
            self.assertEqual(str(ctx.exception), "ErrorTT.__init__() takes from 1 to 2 positional arguments but 3 were given")
        else: raise NotImplementedError('review me')

        def f(): raise ErrorTT(1, 2)
        with self.assertRaises(TypeError) as ctx: f()
        if (sys.version_info.major == 3) and (sys.version_info.minor in [8, 9]):
            self.assertEqual(str(ctx.exception), "__init__() takes from 1 to 2 positional arguments but 3 were given")
        elif (sys.version_info.major == 3) and (sys.version_info.minor in [10, 11]):
            self.assertEqual(str(ctx.exception), "ErrorTT.__init__() takes from 1 to 2 positional arguments but 3 were given")
        else: raise NotImplementedError('review me')

        print('DEBUG: end - test_to_ensure_ErrorTT_accepts_only_1_arg')


if __name__ == '__main__':
    unittest.main()
