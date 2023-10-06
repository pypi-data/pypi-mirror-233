import unittest
from . import this_is_False

from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


class Test__this_is_False(unittest.TestCase):

    def test_increase_nChemical(self):

        n0 = Container.nChemical
        this_is_False(1 == 0)
        n1 = Container.nChemical
        self.assertEqual(n1-n0, 1)

    def test_passes(self):
        
        this_is_False(False)
        this_is_False(not True)
        this_is_False(0 == 1)
        this_is_False(1.5 == 1000)
        this_is_False([1, 2, 3] == [0])

        def f(): return False
        this_is_False(f())

        x = 'hi'
        this_is_False(type(x) is int)

        x = 'hi'
        this_is_False(x == 'foo')

        this_is_False(5 > 20)
        this_is_False(len([1, 2, 3]) > 10)
        this_is_False('hi' == 'mom')
        this_is_False([] == [1])
        this_is_False('art' not in 'heart')

    def test_fails(self):

        with self.assertRaises(ErrorTT) as ctx: this_is_False(True)
        self.assertEqual(str(ctx.exception), "Expected False, but the given condition evaluated to True.")

        with self.assertRaises(ErrorTT) as ctx: this_is_False(not False)
        self.assertEqual(str(ctx.exception), "Expected False, but the given condition evaluated to True.")

        with self.assertRaises(ErrorTT) as ctx: this_is_False(1 == 1)
        self.assertEqual(str(ctx.exception), "Expected False, but the given condition evaluated to True.")


if __name__ == '__main__':
    unittest.main()
