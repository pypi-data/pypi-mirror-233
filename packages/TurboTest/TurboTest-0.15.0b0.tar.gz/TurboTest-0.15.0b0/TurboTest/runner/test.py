import unittest
from . import concluder

import os


TEST_DATA = os.path.join(os.path.dirname(__file__), 'test_data')


class Test__dummy_project_20231004_1(unittest.TestCase):

    def test_dummy_project_20231004_1(self):

        return
        
        CWD = os.path.join(TEST_DATA, 'dummy_project_20231004_1')

        result = concluder(CWD)
        expected = [
            0
        ]
        
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
