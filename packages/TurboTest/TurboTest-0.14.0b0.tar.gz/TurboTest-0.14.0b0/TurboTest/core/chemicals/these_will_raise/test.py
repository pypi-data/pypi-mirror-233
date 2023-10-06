import unittest
from . import these_will_raise

import sys

from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


## Just a mere wrapper so VSCode doesn't mistakenly think that the
## line below `with these_will_raise(ValueError): raise ValueError` will never be executed.
def raise_ValueError(): raise ValueError
def raise_ValueError2(msg): raise ValueError(msg)
def sys_exit(): sys.exit()
def sys_exit2(code): sys.exit(code)
def raise_AssertionError(): raise AssertionError
def raise_AssertionError2(*x): raise AssertionError(*x)


class Test__these_will_raise(unittest.TestCase):

    def test_increase_nChemical(self):
        n0 = Container.nChemical
        with these_will_raise(ValueError): raise_ValueError()
        n1 = Container.nChemical
        self.assertEqual(n1-n0, 1)
        print("DEBUG: it's here")

    def test_passes(self):

        with these_will_raise(ValueError): raise_ValueError()
        with these_will_raise(ValueError) as its: raise_ValueError2('abc')
        self.assertEqual(its.exception_msg, 'abc')

        with these_will_raise(SystemExit): sys_exit()
        with these_will_raise(SystemExit) as its: sys_exit2(3)
        self.assertEqual(its.exit_code, 3)

        with these_will_raise(AssertionError): raise_AssertionError()
        with these_will_raise(AssertionError) as its: raise_AssertionError2(1, '2', [3, 4])
        self.assertEqual(its.exception_value, (1, '2', [3, 4]))

        print("DEBUG: it's here (2)")

    def test_direct(self):

        with these_will_raise(ValueError) as its: raise ValueError('foo123')
        self.assertEqual(its.exception_msg, 'foo123')

        with these_will_raise(Exception) as its: raise Exception('abc')
        self.assertEqual(its.exception_msg, 'abc')

        with these_will_raise(SystemExit) as its: sys.exit(21)
        self.assertEqual(its.exit_code, 21)

        with these_will_raise(AssertionError) as its: raise AssertionError('hi', 123, [1, 2, 3])
        self.assertEqual(its.exception_value, ('hi', 123, [1, 2, 3]))

        with these_will_raise(ValueError): raise ValueError
        with these_will_raise(Exception): raise Exception
        with these_will_raise(SystemExit): sys.exit()

        print("DEBUG: it's here (3)")

    def test_no_exceptions_were_raised(self):

        with self.assertRaises(ErrorTT) as ctx:
            with these_will_raise(AssertionError): pass
        self.assertEqual(str(ctx.exception), "No exceptions were raised; expecting AssertionError.")

        with self.assertRaises(ErrorTT) as ctx:
            with these_will_raise(SystemExit) as its: pass
        self.assertEqual(str(ctx.exception), "No exceptions were raised; expecting SystemExit.")
        
    def test_raising_a_wrong_exception(self):

        with self.assertRaises(ErrorTT) as ctx:
            with these_will_raise(AssertionError): raise ValueError
        self.assertEqual(str(ctx.exception), "Oops! Wrong exception. Expected AssertionError, got ValueError.")

        with self.assertRaises(ErrorTT) as ctx:
            with these_will_raise(AssertionError): sys.exit()
        self.assertEqual(str(ctx.exception), "Oops! Wrong exception. Expected AssertionError, got SystemExit.")

        with self.assertRaises(ErrorTT) as ctx:
            with these_will_raise(SystemExit): raise ValueError
        self.assertEqual(str(ctx.exception), "Oops! Wrong exception. Expected SystemExit, got ValueError.")

        with self.assertRaises(ErrorTT) as ctx:
            with these_will_raise(ValueError): raise TypeError('foo')
        self.assertEqual(str(ctx.exception), "Oops! Wrong exception. Expected ValueError, got TypeError.")


if __name__ == '__main__':
    unittest.main()
