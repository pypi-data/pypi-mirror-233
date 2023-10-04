import unittest
from pyappi.client import use_test_client, RealtimeHttpClient
import time
from pyappi.util.login import session_challenge, make_session


class TestInherit(unittest.TestCase):
    def setUp(self):
        use_test_client()

        self.session2 = make_session("TESTUSER2", "TESTPASSWORD2")
        self.session3 = make_session("TESTUSER3", "TESTPASSWORD3")

        RealtimeHttpClient("test_inherit_perm").delete()
        RealtimeHttpClient("test_inherit_target").delete()
 
    def test_events(self):
        with RealtimeHttpClient("test_inherit_perm") as doc:
            doc._perm[self.session2["user"]] = "read"
            doc._perm[self.session3["user"]] = "write"

        self.assertEqual(doc.status_code, 202)

        with RealtimeHttpClient("test_inherit_target") as doc:
            doc._perm._inherit["test_inherit_perm"] = ""

            doc.data.value = 1

        self.assertEqual(doc.status_code, 202)

        with RealtimeHttpClient("test_inherit_target", session=self.session2) as doc:
            self.assertEqual(doc.data.value, 1)

        self.assertEqual(doc.status_code, 200)

        with RealtimeHttpClient("test_inherit_target", session=self.session3) as doc:
            self.assertEqual(doc.data.value, 1)

            doc.data.value = 2

        self.assertEqual(doc.status_code, 202)

        with RealtimeHttpClient("test_inherit_target", session=self.session2) as doc:
            self.assertEqual(doc.data.value, 2)

            doc.data.value = 3

        self.assertEqual(doc.status_code, 409)

        with RealtimeHttpClient("test_inherit_target", session=self.session3) as doc:
            self.assertEqual(doc.data.value, 2)

        self.assertEqual(doc.status_code, 200)

        with RealtimeHttpClient("test_inherit_target") as doc:
            self.assertEqual(doc.data.value, 2)

        self.assertEqual(doc.status_code, 200)

if __name__ == "__main__":
    unittest.main()
