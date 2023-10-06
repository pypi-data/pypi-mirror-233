import unittest
from . import these_two_must_be_different

from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


class Test__these_two_must_be_different(unittest.TestCase):

    def test_increase_nChemical(self):

        n0 = Container.nChemical
        these_two_must_be_different(0, 1)
        n1 = Container.nChemical
        self.assertEqual(n1-n0, 1)

    def test_passes(self):
        
        ## integers
        these_two_must_be_different(0, 1)
        these_two_must_be_different(1000, 2000)
        these_two_must_be_different(12131312314141231, 99999999999999999999)

        ## floats
        these_two_must_be_different(0.0, 0.01)
        these_two_must_be_different(0.001, 0.0012)
        these_two_must_be_different(1.234567890, .2)
        these_two_must_be_different(123123.12312313123, 0.123)

        ## tuples
        these_two_must_be_different((1, 2), (1, 2, 3))
        these_two_must_be_different(('a', 'b'), ('a', 2))
        these_two_must_be_different((), [])

        ## lists
        these_two_must_be_different([1, 2, 3], [1, 2, 3, 4])
        these_two_must_be_different(['a', 'b', 'c'], ['c', 'b', 'a'])
        these_two_must_be_different([], {})

        ## strings
        these_two_must_be_different('hello', 'mom')
        these_two_must_be_different('you', 'cool')
        these_two_must_be_different('', 1)

        ## dicts
        these_two_must_be_different({'k1': 'v1', 'k2': 'v2'}, {'0': '0', '1': '1'})
        these_two_must_be_different({}, {1: 2})

        ## bools
        these_two_must_be_different(True, False)
        these_two_must_be_different(1 == 1, 3 == 9)
        these_two_must_be_different(1 == 0, 3 == 3)
        these_two_must_be_different([] == [], {} != {})

    def test_fails(self):

        x = 1
        y = 1
        with self.assertRaises(ErrorTT) as ctx: these_two_must_be_different(x, y)
        self.assertEqual(str(ctx.exception), f"X and Y should be different, but they are the same.\n  X: {repr(x)}\n  Y: {repr(y)}")

        x = 'hi 123'
        y = 'hi 123'
        with self.assertRaises(ErrorTT) as ctx: these_two_must_be_different(x, y)
        self.assertEqual(str(ctx.exception), f"X and Y should be different, but they are the same.\n  X: {repr(x)}\n  Y: {repr(y)}")

        x = [1]
        y = [1]
        with self.assertRaises(ErrorTT) as ctx: these_two_must_be_different(x, y)
        self.assertEqual(str(ctx.exception), f"X and Y should be different, but they are the same.\n  X: {repr(x)}\n  Y: {repr(y)}")


if __name__ == '__main__':
    unittest.main()
