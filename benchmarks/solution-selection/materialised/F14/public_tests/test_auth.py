import logging
import unittest

from auth import service
from auth.user_import import import_users

NOW = 1_790_000_000


class AuthHappyPath(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("f14-public")
        self.store = {}
        service.register(self.store, "Akello", "correct horse battery")

    def test_login(self):
        self.assertTrue(service.login(self.store, "akello", "correct horse battery", self.logger))
        self.assertFalse(service.login(self.store, "akello", "wrong", self.logger))

    def test_token_round_trip(self):
        token = service.issue_token("akello", "exporter", now=NOW)
        claims = service.authorise(token, now=NOW + 10, required_role="viewer")
        self.assertEqual(claims["sub"], "akello")

    def test_import_simple_rows(self):
        rows, errors = import_users("username,display_name,role\nakello,Akello Stores,viewer\nmbabazi,Mbabazi,exporter\n")
        self.assertEqual(errors, [])
        self.assertEqual([r["username"] for r in rows], ["akello", "mbabazi"])


if __name__ == "__main__":
    unittest.main()
