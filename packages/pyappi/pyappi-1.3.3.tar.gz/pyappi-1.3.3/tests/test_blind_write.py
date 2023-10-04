import unittest
from pyappi.client import use_test_client, RealtimeHttpClient
import time
from pyappi.util.login import session_challenge, make_session


class TestInherit(unittest.TestCase):
    def setUp(self):
        use_test_client()

        self.session2 = make_session("TESTUSER2", "TESTPASSWORD2")
        self.session3 = make_session("TESTUSER3", "TESTPASSWORD3")

        RealtimeHttpClient("test_mail").delete()
 
    def test_events(self):
        with RealtimeHttpClient("test_mail") as doc:
            doc._perm.public = "blind_write"

        self.assertEqual(doc.status_code, 202)

        with RealtimeHttpClient("test_mail", session=self.session2) as doc:
            doc.x = { "message": "HI", "from": self.session2["user"]}

        self.assertEqual(doc.status_code, 202)

        with RealtimeHttpClient("test_mail", session=self.session3) as doc:
            doc.x = { "message": "HI", "from": self.session3["user"]}

        self.assertEqual(doc.status_code, 202)

        with RealtimeHttpClient("test_mail", session=self.session2) as doc:
            self.assertTrue(True)

        self.assertEqual(doc.status_code, 404)

        with RealtimeHttpClient("test_mail", session=self.session3) as doc:
            self.assertTrue(True)

        self.assertEqual(doc.status_code, 404)

        with RealtimeHttpClient("test_mail") as doc:
            mail = doc["mail~log"].unwrap()
            self.assertEqual(mail["0"]["from"], self.session2["user"])

        self.assertEqual(doc.status_code, 200)

if __name__ == "__main__":
    unittest.main()
