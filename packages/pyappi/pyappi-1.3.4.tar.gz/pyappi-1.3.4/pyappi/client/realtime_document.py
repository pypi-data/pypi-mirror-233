from pyappi.client.client_handle import get_connection_details
from pyappi.client.session import get_session
from pyappi.client.lock import client_appi_mutex
from pyappi.encoding.url import decode_url
from pyappi.document import Document
from pyappi.util.login import encode_session, decode_session
from pyappi.client.config import set_config

import json


def _resolve_session(self):
    return get_session() if not len(self.__dict__["__session"]) else encode_session(self.__dict__["__session"])

def http_enter(self):
    client_appi_mutex.acquire()

    client, config = get_connection_details()
    session = _resolve_session(self)

    match self.name:
        # TODO Move to helper function
        case "@user":
            self.__dict__["name"] = f'user.{decode_session(session)["user"]}'
        case _: pass

    self.__dict__['__lock'] = True
    try:
        response = client.get(f'{config["protocol"]}{config["host"]}/document/{self.name}?{session}')

        self.__dict__["status_code"] = response.status_code
        if response.status_code != 200:
            raise Exception()
        self.__dict__['__document'] = response.json()
    except Exception as e:
        if self.__dict__['__read_only']:
            self.__dict__['__lock'] = False
            client_appi_mutex.release()
            raise e
        
        self.__dict__['__document'] = {}

    self.__dict__['__tsx'] = self.__dict__['__document'].get("_cmt",0) + 1

    return self


def http_sync(self):
    if self.__dict__['__lock'] != True:
        raise "Document not locked"
    
    if len(self.__dict__['__delta']):
        http_flush(self)

    client, config = get_connection_details()
    session = _resolve_session(self)

    try:
        response = client.get(f'{config["protocol"]}{config["host"]}/document/{self.name}?{session}')
        self.__dict__["status_code"] = response.status_code
        self.__dict__['__document'] = response.json()
    except Exception as e:
        pass


def http_delete(self):
    client, config = get_connection_details()
    session = _resolve_session(self)

    response = client.delete(f'{config["protocol"]}{config["host"]}/document/{self.name}?{session}')
    self.__dict__["status_code"] = response.status_code


def http_flush(self):
    if not self.__dict__['__mutated'] or self.__dict__["__read_only"]:
        return
    
    client, config = get_connection_details()
    session = _resolve_session(self)

    self.__dict__['__delta']["_bmt"] = -1
    response = client.put(f'{config["protocol"]}{config["host"]}/document/{self.name}?{session}', json=self.__dict__['__delta'])
    self.__dict__['__delta'] = {}
    self.__dict__['__mutated'] = False
    self.__dict__["status_code"] = response.status_code


def http_exit(self, type, value, traceback):
    http_flush(self)

    self.__dict__['__lock'] = False
    client_appi_mutex.release()


class RealtimeHttpClient(Document):
    def __init__(self, name, who = "realtime_http_client",session = {}, config = None):
        if config:
            set_config(config)
        super().__init__(name, who, io={"enter":http_enter,"delete":http_delete,"exit":http_exit,"flush":http_flush,"sync":http_sync}, client=True, session=session)