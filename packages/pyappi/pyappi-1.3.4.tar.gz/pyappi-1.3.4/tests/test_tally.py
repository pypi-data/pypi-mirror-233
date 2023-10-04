import unittest
from pyappi.client import RealtimeHttpClient, use_test_client
from pyappi.util.login import make_session
from pyappi.document import VolatileDocument, Document


test_documents = [(RealtimeHttpClient,"tally")] #, (VolatileDocument,"vd_tally"), (Document,"d_tally")]


class TestAppiTally(unittest.TestCase):
    def setUp(self):
        use_test_client()
 
        [doc(name).delete() for (doc,name) in test_documents]

    def _test_tally_base(self,_doc_type, _doc_name):
        serial = None
        with _doc_type(_doc_name) as doc:
            doc._perm.stats = "enable"
            doc.obj = {
                "count~tally":17,
                "other~tally":3
            }
            
            doc.obj2_type_tally = {
                "count": 13,
                "other": 1
            }

        with _doc_type(_doc_name) as doc:
            serial = doc["$id"].serial

            self.assertEqual(doc._server_tally.count, 30)
            self.assertEqual(doc._server_tally.other, 4)

            doc.obj = {
                "count~tally":7,
                "other~tally":4,
                "new~tally":2
            }

            doc.obj2_type_tally = {
                "count": 13,
                "other": 1
            }

        with _doc_type(_doc_name) as doc:

            self.assertEqual(doc._server_tally.count, 20)
            self.assertEqual(doc._server_tally.other, 5)
            self.assertEqual(doc._server_tally.new, 2)

            doc.test_type_log = {"_depth":5}

            for i in range(10):
                doc.test_type_log[f'x{i}'] = {"internal~ltally": 1,"message": "message", "index":i}
                doc.flush()

            doc.sync()

            #std::string serial;serial = std::string("!") + std::string(root("$id")["serial"]);
            self.assertEqual(doc._server_ltally.test, 10)
            self.assertEqual(doc._server_ltally.internal, 10)

            doc.subscribers_type_log.x = {
                "content": "I subscribed",
            }

            doc.flush()

            with _doc_type(_doc_name,session=make_session("TESTUSER", "TESTPASSWORD", params={"type":"stats"})) as stats:
                self.assertEqual(stats["subscribers"], 1)

            with _doc_type("@user") as user:
                user.subscriptions_type_glog.x = serial
                user.following_type_glog.x = serial


            with _doc_type(_doc_name,session=make_session("TESTUSER", "TESTPASSWORD", params={"type":"stats"})) as stats:
                self.assertEqual(stats["followers"], 1)
                self.assertEqual(stats["subscribers"], 2)

            with _doc_type(_doc_name,session=make_session("TESTUSER2", "TESTPASSWORD2", params={"type":"comments"})) as comment:
                comment.x = {"message": "Access Denied"}

            self.assertEqual(comment.status_code,403)

            doc._perm.comments = "enable"
            doc.sync()

            with _doc_type(_doc_name,session=make_session("TESTUSER2", "TESTPASSWORD2", params={"type":"comments"})) as comment:
                comment.x = {"message": "Allow Access"}

            self.assertEqual(comment.status_code,202)

            with _doc_type("@user") as user:
                id = user._server_id.serial

            self.assertEqual(user.status_code,200)

            with _doc_type("@user",session=make_session("TESTUSER2", "TESTPASSWORD2")) as user2:
                id2 = user2._server_id.serial

            self.assertEqual(user2.status_code,200)

            with _doc_type(_doc_name,session=make_session("TESTUSER2", "TESTPASSWORD2", params={"type":"comments"})) as comment:
                comment.x = {"message": "message", "~owner": id2}

            self.assertEqual(comment.status_code,202)

            with _doc_type(_doc_name,session=make_session("TESTUSER", "TESTPASSWORD", params={"type":"comments"})) as comment:
                comment.x = {"message": "message", "~owner": id}

            self.assertEqual(comment.status_code,202)

            with _doc_type(_doc_name) as doc:
                for k,v  in doc.comments_type_log.unwrap().items():
                    if k.startswith("_"):
                        continue

                    if v.get("~owner", "") == id:
                        owner_key = k
                    if v.get("~owner", "") == id2:
                        guest_key = k

            with _doc_type(_doc_name,session=make_session("TESTUSER2", "TESTPASSWORD2", params={"type":"comments"})) as comment:
                comment[owner_key] = {"message": "Cant update someone else's message."}

            self.assertEqual(comment.status_code,422)

            with _doc_type(_doc_name,session=make_session("TESTUSER2", "TESTPASSWORD2", params={"type":"comments"})) as comment:
                comment[guest_key] = {"message": "Can update own message"}

            self.assertEqual(comment.status_code,202)

            with _doc_type(_doc_name,session=make_session("TESTUSER", "TESTPASSWORD", params={"type":"comments"})) as comment:
                comment[guest_key] = {"message": "Can update message as owner"}

            self.assertEqual(comment.status_code,202)

            # TODO VALIDATE IO TO HISTORY BUCKETS
            # You should only be able to update log history you own

            """
            // TODO TEST reader interaction permissions
            // readers are people with the _perm: read
            result = client.Upsert(qid, R"J(
            {
                "_perm":{
                    "comments":"readers"
                }
            })J");
            REQUIRE(result == tdb::appi::NoError);"""

    def test_tally(self):
        [self._test_tally_base(doc,name) for (doc,name) in test_documents]


if __name__ == "__main__":
    unittest.main()
