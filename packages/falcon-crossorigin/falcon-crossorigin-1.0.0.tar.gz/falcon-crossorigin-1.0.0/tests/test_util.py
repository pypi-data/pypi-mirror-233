import unittest

from falcon_crossorigin.util import _match_sub_domain


class TestUtil(unittest.TestCase):
    def test_match_sub_domain(self):
        long_domain = "http://{}.com".format("a" * 254)

        # schemes are empty or do not match
        self.assertFalse(_match_sub_domain("", ""))
        self.assertFalse(_match_sub_domain("http://example.com", "https://example.com"))
        self.assertFalse(_match_sub_domain("https://example.com", "http://example.com"))

        # domain is empty
        self.assertFalse(_match_sub_domain("http://example.com", "http://"))
        self.assertFalse(_match_sub_domain("http://", "http://example.com"))

        # domain too long
        self.assertFalse(_match_sub_domain(long_domain, "http://example.com"))

        # domain does not match pattern
        self.assertFalse(
            _match_sub_domain("http://app.example.com", "http://app.test.example.com")
        )

        # invalid domain/pattern
        self.assertFalse(_match_sub_domain("http://app.", "http://app"))
        self.assertFalse(_match_sub_domain("http://app", "http://app."))
