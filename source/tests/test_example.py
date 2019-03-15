import unittest

# import ..<name of module to be tested>


class TestExample(unittest.TestCase):
    def test_example_add_1_and_2(self):
        self.assertEqual(1 + 2, 3)