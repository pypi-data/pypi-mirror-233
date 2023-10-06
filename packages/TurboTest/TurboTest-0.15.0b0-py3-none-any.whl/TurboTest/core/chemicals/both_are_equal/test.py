import unittest
from . import both_are_equal

from TurboTest.core.error_tt import ErrorTT
from TurboTest.core.chemicals import Container


class Test__both_are_equal(unittest.TestCase):

    def test_increase_nChemical(self):

        n0 = Container.nChemical
        both_are_equal(0, 0)
        n1 = Container.nChemical
        self.assertEqual(n1-n0, 1)

    def test_passes(self):
        
        ## integers
        both_are_equal(0, 0)
        both_are_equal(1, 1)
        both_are_equal(1000, 1000)
        both_are_equal(12131312314141231, 12131312314141231)

        ## floats
        both_are_equal(0.0, 0.0)
        both_are_equal(0.001, 0.001)
        both_are_equal(1.234567890, 1.234567890)
        both_are_equal(123123.12312313123, 123123.12312313123)

        ## tuples
        both_are_equal((1, 2), (1, 2))
        both_are_equal(('a', 'b'), ('a', 'b'))
        both_are_equal((), ())

        ## lists
        both_are_equal([1, 2, 3], [1, 2, 3])
        both_are_equal(['a', 'b', 'c'], ['a', 'b', 'c'])
        both_are_equal([], [])

        ## strings
        both_are_equal('hello', 'hello')
        both_are_equal('world', 'world')
        both_are_equal('', '')

        ## dicts
        both_are_equal({'k1': 'v1', 'k2': 'v2'}, {'k1': 'v1', 'k2': 'v2'})
        both_are_equal({}, {})

        ## bools
        both_are_equal(True, True)
        both_are_equal(False, False)
        both_are_equal(1 == 1, 3 == 3)
        both_are_equal(1 == 0, 3 == 9)

    def test_fails(self):

        x = 1
        y = 2
        with self.assertRaises(ErrorTT) as ctx: both_are_equal(x, y)
        self.assertEqual(str(ctx.exception), f"X should be equal to Y, but they aren't.\n  X: {repr(x)}\n  Y: {repr(y)}")

        x = 'hi 123'
        y = 1
        with self.assertRaises(ErrorTT) as ctx: both_are_equal(x, y)
        self.assertEqual(str(ctx.exception), f"X should be equal to Y, but they aren't.\n  X: {repr(x)}\n  Y: {repr(y)}")

        x = []
        y = [1]
        with self.assertRaises(ErrorTT) as ctx: both_are_equal(x, y)
        self.assertEqual(str(ctx.exception), f"X should be equal to Y, but they aren't.\n  X: {repr(x)}\n  Y: {repr(y)}")


if __name__ == '__main__':
    unittest.main()
