import unittest

from arikedb_tools.exceptions import ArikedbClientError


class ArikedbClientErrorTests(unittest.TestCase):

    def test_exception(self):

        def raiser():
            raise ArikedbClientError
        self.assertRaises(ArikedbClientError, raiser)


if __name__ == '__main__':
    unittest.main()
