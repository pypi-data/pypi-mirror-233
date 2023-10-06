import unittest
from . import Container


class Test__Container(unittest.TestCase):

    def test_add(self):
        
        ## <This is not the correct way to test it since nChemical might not be 0 due to previous tests modifying it>
        # Container.add_chemical()
        # self.assertEqual(Container.nChemical, 1)
        ## </This is not the correct way to test it since nChemical might not be 0 due to previous tests modifying it>

        n0 = Container.nChemical
        Container.add_chemical()
        n1 = Container.nChemical
        self.assertEqual(n1-n0, 1)

    def test_clear(self):
        Container.clear_chemical()
        self.assertEqual(Container.nChemical, 0)


if __name__ == '__main__':
    unittest.main()
