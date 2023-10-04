
from typing import Any
from .random_handler import random_handler
from .type import type_lookup
from .exceptions import *
from .file_handler import file_handler
from pyappi.document.lock import global_appi_mutex
from pyappi.document.transaction import Transaction
from pyappi.document.local import update_user_local_transaction
from pyappi.document.history import update_document_history
from pyappi.util.merge import dict_merge
from pyappi.util.filename import clean_filename
from pyappi.document.enumeration import prepare_new_document
from pyappi.stats.stats import read_stats
from pyappi.document.history import read_history
from pyappi.events.events import publish_event

import json
import os
import time


def fs_enter(self):
    global_appi_mutex.acquire()

    self.__dict__['__lock'] = True
    try:
        mode = self.__dict__['__session'].get("type", None)
        match mode:
            case "stats":
                self.__dict__['__document'] = read_stats(self.name)
            case "history":
                self.__dict__['__document'] = read_history(self.name)
            case "public":
                filename = clean_filename(f'{self.__dict__["__path"] }/{self.name}.json')
                with open(filename) as document_handle:
                    self.__dict__['__document'] = json.load(document_handle)["~public"]
            case _:
                filename = clean_filename(f'{self.__dict__["__path"] }/{self.name}.json')
                with open(filename) as document_handle:
                    self.__dict__['__document'] = json.load(document_handle)
    except Exception as e:
        if self.__dict__['__read_only']:
            self.__dict__['__lock'] = False
            global_appi_mutex.release()
            raise e
        
        self.__dict__['__document'] = {}
        if document_config["enumeration"]:
            prepare_new_document(self,self.name)

    self.__dict__['__tsx'] = self.__dict__['__document'].get("_cmt",0) + 1

    return self


def fs_delete(self):
    record = f'{self.__dict__["__path"]}/{self.__dict__["name"]}.json'
    backup = f'{self.__dict__["__path"]}/{self.__dict__["name"]}.backup.json'

    try:
        os.remove(backup)
    except OSError:
        pass

    try:
        os.remove(record)
    except OSError:
        pass


def fs_sync(self):
    # With the current implementation the read back is a no op.
    fs_flush(self)



def fs_flush(self):
    if not self.__dict__['__mutated'] or self.__dict__["__read_only"]:
        return
    
    record = clean_filename(f'{self.__dict__["__path"]}/{self.__dict__["name"]}.json')
    backup = clean_filename(f'{self.__dict__["__path"]}/{self.__dict__["name"]}.backup.json')

    try:
        os.remove(backup)
    except OSError:
        pass

    try:
        os.rename(record, backup)
    except OSError:
        pass
    
    with open(record, "w") as doc:
        doc.write(json.dumps(self.__dict__['__document'] , indent=4))

    tsx = self.__dict__['__tsx']
    self.__dict__['__tsx'] = self.__dict__['__document'].get("_cmt",0) + 1

    permissions = self.__dict__['__document'].get("_perm",{})
    is_public = permissions.get("public","") == "read"

    for user,level in permissions.items():

        if user == "public" or user[0] == '_' or level == "inherit":
            continue

        update_user_local_transaction(user, self.__dict__["name"], tsx, is_public)

    update_document_history(self.__dict__['__who'],self.__dict__['name'],tsx, is_public, self.__dict__['__delta'])
    self.__dict__['__delta'] = {}
    self.__dict__['__mutated'] = False

    publish_event({"id": self.__dict__["name"],"updates": self.__dict__['__events']})
    self.__dict__['__events'] = {}


def fs_exit(self, type, value, traceback):
    fs_flush(self)

    self.__dict__['__lock'] = False
    global_appi_mutex.release()

document_config = {
    "root": "appidb/documents",
    "enumeration": True,
}


if not os.path.exists(document_config["root"]):
    os.makedirs(document_config["root"],exist_ok=True)


class Document():
    def __init__(self, name, who="", path=None, read_only=False, auto_nav=True, io={"enter":fs_enter,"delete":fs_delete,"exit":fs_exit, "flush": fs_flush, "sync": fs_sync}, client=False, session={}, who_id=None):
        self.__dict__['__path'] = document_config["root"] if not path else path
        self.__dict__['__auto_nav'] = auto_nav
        self.__dict__['name'] = name
        self.__dict__['__io'] = io
        self.__dict__['__client'] = client
        self.__dict__['__who'] = who
        self.__dict__['__who_id'] = who_id
        self.__dict__['__tsx'] = 0
        self.__dict__['__lock'] = False
        self.__dict__['__mutated'] = False
        self.__dict__['__read_only'] = read_only
        self.__dict__['__document'] = {}
        self.__dict__['__delta'] = {}
        self.__dict__['__now'] = int(time.time() * 1000 * 1000)
        self.__dict__["__session"] = session
        self.__dict__["__events"] = {}

        mode = session.get("type", None)
        if mode:
            match mode:
                case "stats" | "history" | "public":
                    self.__dict__['__read_only'] = True
                    pass
                case _:
                    pass


    def __len__(self):
        return len(self.__dict__['__document'])
    
    def __contains__(self, key):
        return key in self.__dict__['__document']

    def unwrap(self):
        return self.__dict__['__document']
    
    def get_id(self):
        return self.__dict__['name']
    
    def get_user(self):
        return self.__dict__['__who']
    
    def get_user_id(self):
        return self.__dict__['__who_id']
    
    def get_document_type(self):
        return Document
    
    def get(self,key,default):
        if self.__dict__['__document'].get(key,None) is None:
            return default
        
        return self[key]

    def __update(self, tsx, key, delta, path, action):
        if delta and not (key.startswith("$") and self.__dict__['__client']):
            self.__dict__['__delta'][key] = self.__dict__['__delta'].get(key,{})
            dict_merge(self.__dict__['__delta'][key],delta)

        self.__dict__["__events"][(key+"."+path) if path else key] = action

        self.__dict__['__mutated'] = True
        self.__dict__['__document']["_cmt"] = tsx
        self.__dict__['__document']["_lmt"] = int(time.time())

    def __setattr__(self, _name: str, _value: Any) -> None:
        _name = _name.replace("_type_","~").replace("_server_","$")

        if self.__dict__['__read_only']:
            raise ReadOnlyDocument()

        if not self.__dict__['__lock']:
            raise DocumentNotLocked()

        if not isinstance(_value, dict):
            raise "Root values not allowed in Appi"
        
        if len(_value):
            t = self[_name]

            for k,v in _value.items():
                t[k] = v

            return

        self.__dict__['__document'][_name] = _value
        self.__update(self.__dict__['__tsx'],_name, self.__dict__['__document'][_name], _name, "set")

    def __getattr__(self, key):
        key = key.replace("_type_","~").replace("_server_","$")

        if not self.__dict__['__lock']:
            raise DocumentNotLocked()

        if key == '_Transaction__update':
            return self._Document__update
        doc = self.__dict__['__document'].get(key,None)
        if not doc:
            if self.__dict__['__auto_nav'] and not self.__dict__['__read_only']:
                if key.startswith("__") and key.endswith("__"):
                    return None
                self.__dict__['__document'][key] = {}
                doc = self.__dict__['__document'][key]
            else:
                raise PathDoesntExist()
            
        if isinstance(doc, dict):  
            return Transaction(doc, self.__dict__['__tsx'],key, self, type_lookup(key,doc), self)
        else:
            return doc

    def __setitem__(self, __name: str, __value: Any) -> None:
        return self.__setattr__(__name,__value)
    
    def __getitem__(self, _name: str):
        return self.__getattr__(_name)

    def __enter__(self):
        document = self.__dict__['__io']["enter"](self)

        if not self.__dict__["__client"]:
            self.__dict__["__is_owner"] = self.__dict__['__document'].get("_perm",{}).get(self.__dict__['__who'],"") == "owner"
        
            return document

        mode = self.__dict__['__session'].get("type", None)

        match mode:
            case "comment":
                return document.comments_type_log
            case _:
                return document
    
    def delete(self):
        return self.__dict__['__io']["delete"](self)
    
    def flush(self):
        return self.__dict__['__io']["flush"](self)
    
    def sync(self):
        return self.__dict__['__io']["sync"](self)
    
    def __exit__(self, type, value, traceback):
        return self.__dict__['__io']["exit"](self,type,value,traceback)




