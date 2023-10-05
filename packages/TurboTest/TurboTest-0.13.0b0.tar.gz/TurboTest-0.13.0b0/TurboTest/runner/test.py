import unittest

import os


TEST_DATA = os.path.join(os.path.dirname(__file__), 'test_data')


class Test__dummy_project_20231004_1(unittest.TestCase):

    def test_dummy_project_20231004_1(self):
        
        CWD = os.path.join(TEST_DATA, 'dummy_project_20231004_1')

        result = 0
        expected = [
            0
        ]
        
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
