import unittest
from pyappi.client import use_test_client, RealtimeHttpClient
from pyappi.service.service import RawService, ServiceTail
from pyappi.service.session import lookup_service_key
import time


class TestEvents(unittest.TestCase):
    def setUp(self):
        use_test_client()

        self.key = lookup_service_key()
        RealtimeHttpClient("test_events").delete()

    def test_tail(self):
        with ServiceTail(session={"user":"default","challenge":self.key}, interval=.3):

            time.sleep(1)

            with RealtimeHttpClient("test_events") as doc:
                u = doc.update

                u.nested.value = "CAsfawojgaw"
                u.name = "TEST"
                u.here = "HERE"

            time.sleep(1)

            self.assertTrue(True)
 
    def test_events(self):
        update = None
        def handler(_update):
            nonlocal update
            update = _update["events"]

        service = RawService(handler,session={"user":"default","challenge":self.key}, interval=.3)

        time.sleep(1)

        with RealtimeHttpClient("test_events") as doc:
            u = doc.update

            u.nested.value = "CAsfawojgaw"
            u.name = "TEST"
            u.here = "HERE"

        while update is None:
            time.sleep(.3)

        key = list(update)[-1]

        self.assertEqual(update[key]["id"],"test_events")
        self.assertEqual(update[key]["updates"]["update.nested.value"],"set")
        self.assertEqual(update[key]["updates"]["update.name"],"set")
        self.assertEqual(update[key]["updates"]["update.here"],"set")

        service.stop()


if __name__ == "__main__":
    unittest.main()
