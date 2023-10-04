from pyappi.document.lock import global_appi_mutex
from pyappi.document import Document


volatile_documents = {}


def volatile_enter(self):
    global_appi_mutex.acquire()

    self.__dict__['__lock'] = True
    self.__dict__['__document'] = volatile_documents.get(self.__dict__['name'],{})
    self.__dict__['__tsx'] = self.__dict__['__document'].get("_cmt",0) + 1

    return self

def volatile_sync(self):
    if self.__dict__['__lock'] != True:
        raise "Document not locked"
    
    if len(self.__dict__['__delta']):
        volatile_flush(self)

    # Optional: must readback only if multi threaded access is implemented


def volatile_delete(self):
    try:
        del volatile_documents[self.__dict__['name']]
        return True
    except Exception as _:
        return False


def volatile_flush(self):
    if not self.__dict__['__mutated'] or self.__dict__["__read_only"]:
        return
    
    volatile_documents[self.__dict__['name']] = self.__dict__['__document']
    self.__dict__['__delta'] = {}


def volatile_exit(self, type, value, traceback):
    volatile_flush(self)

    self.__dict__['__lock'] = False
    global_appi_mutex.release()


class VolatileDocument(Document):
    def __init__(self, name, who = "volatile_document",session = {}):
        super().__init__(name, who, io={"enter":volatile_enter,"delete":volatile_delete,"exit":volatile_exit,"flush":volatile_flush,"sync":volatile_sync}, session=session)