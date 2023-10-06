import unittest
from . import this_is_True

import os
import tempfile

from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


class Test__this_is_True(unittest.TestCase):

    def test_increase_nChemical(self):

        n0 = Container.nChemical
        this_is_True('hi' == 'hi')
        n1 = Container.nChemical
        self.assertEqual(n1-n0, 1)

    def test_passes(self):
        
        this_is_True(True)
        this_is_True(not False)
        this_is_True(0 == 0)
        this_is_True(1.5 == 1.5)
        this_is_True([1, 2, 3] == [1, 2, 3])

        def f(): return True
        this_is_True(f())

        x = 'hi'
        this_is_True(type(x) is str)

        x = 'hi'
        this_is_True(x == 'hi')

        this_is_True(5 > 2)
        this_is_True(len([1, 2, 3]) > 0)
        this_is_True('hi' != 'mom')
        this_is_True([] == [])
        this_is_True('art' in 'heart')

    def test_fails(self):

        with self.assertRaises(ErrorTT) as ctx: this_is_True(False)
        self.assertEqual(str(ctx.exception), "The given condition is `False`, expected `True`.")

        with self.assertRaises(ErrorTT) as ctx: this_is_True(not True)
        self.assertEqual(str(ctx.exception), "The given condition is `False`, expected `True`.")

        with self.assertRaises(ErrorTT) as ctx: this_is_True(1 == 2)
        self.assertEqual(str(ctx.exception), "The given condition is `False`, expected `True`.")
    
    def test_complex_scenario_I(self):

        d = tempfile.mkdtemp()
        pth = os.path.join(d, 'test_file.txt')

        self.assertEqual(os.path.isfile(pth), False)
        this_is_True(not os.path.isfile(pth))

        open(pth, 'w').close()

        self.assertEqual(os.path.isfile(pth), True)
        this_is_True(os.path.isfile(pth))


if __name__ == '__main__':
    unittest.main()
