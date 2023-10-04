from pyappi.client.client_handle import get_connection_details
from pyappi.util.login import encode_session
from pyappi.client.session import get_session
from pyappi.client.config import set_config
import threading
import time


class RawService:
    def __init__(self, handler, name="default", interval=3, config=None, session={}):
        self.name = name
        self.handler = handler
        self.interval = interval

        if config:
            set_config(config)

        self.session = get_session() if not len(session) else encode_session(session)

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        client, config = get_connection_details()

        res = client.get(f'{config["protocol"]}{config["host"]}/service/cursor?{self.session}').json()
        
        tsx = res["cursor"]

        while self.running:
            time.sleep(self.interval)

            res = client.get(f'{config["protocol"]}{config["host"]}/service/read_events/{tsx}?{self.session}').json()

            if res["events"]:
                tsx += len(res["events"])
                self.handler(res)

    
class ServiceTail:
    def __init__(self, config=None, session={}, interval=1):
        self.config = config
        self.session = session
        self.interval = interval

    @staticmethod
    def handler(update):
        print(update)

    def __enter__(self):
        self.service = RawService(ServiceTail.handler,session=self.session, interval=self.interval, config=self.config)

        return self
    
    def __exit__(self, type, value, traceback):
        self.service.stop()
    