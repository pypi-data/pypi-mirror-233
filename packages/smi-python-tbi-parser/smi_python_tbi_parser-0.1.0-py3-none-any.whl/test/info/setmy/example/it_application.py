import unittest


class ITExample(unittest.TestCase):

    def setUp(self):
        pass

    def test_example(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
