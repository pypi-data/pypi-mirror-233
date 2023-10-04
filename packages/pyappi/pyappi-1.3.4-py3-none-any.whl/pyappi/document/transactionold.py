from pyappi.document.type import *
from pyappi.document.random_handler import *
from pyappi.document.exceptions import *
from pyappi.logs import log_handler
from pyappi.stats import stats_handler
from typing import Any

import time
import os
import json


transaction_config = {
    "allow_bulk_assign": True
}
    

class Transaction:
    def __init__(self, document, tsx, key, parent=None, type="", root=None, owner=None):
        self.__dict__['__document'] = document
        self.__dict__['__parent'] = parent
        self.__dict__['__root'] = root
        self.__dict__['__tsx'] = tsx
        self.__dict__['__type'] = type
        self.__dict__['__key'] = key
        self.__dict__['__owner'] = owner

    def __len__(self):
        return len(self.__dict__['__document'])
    
    def __contains__(self, key):
        return key in self.__dict__['__document']
    
    def unwrap(self):
        return self.__dict__['__document']
    
    def get(self,key,default):
        if self.__dict__['__document'].get(key,None) is None:
            return default
        
        return self[key]

    def __update(self, tsx, key, _delta):
        self.__dict__['__document']["_cmt"] = self.__dict__['__tsx']

        # Keys that start with $ should not be sent to the server. They are computed for the benefit of the local object only
        delta = None if not _delta or (key.startswith("$") and self.__dict__["__root"].__dict__['__client']) else {key:_delta}

        self.__dict__['__parent'].__update(self.__dict__['__tsx'], self.__dict__['__key'],delta)

    def __setattr__(self, _name: str, _value: Any) -> None:
        _name = str(_name)
        _name = _name.replace("_type_","~").replace("_server_","$")

        if self.__dict__['__root'].__dict__['__read_only']:
            raise ReadOnlyDocument()
        
        if self.__dict__['__document'].get("~owner", None) != None and self.__dict__['__document']['~owner'] != self.__dict__['__root'].__dict__["__who_id"] and not self.__dict__['__root'].__dict__["__is_owner"]:
            raise UserWriteProtectedRegion()

        if isinstance(_value, list):
            raise ListsAreNotAllowed()
        
        if isinstance(self.__dict__['__document'].get(_name,None), dict):
            raise DictionaryReassignmentProhibited()
        
        def ltally(key, count):
            lt = self.__dict__['__root']["$ltally"]

            lt[key] = lt.get(key,0) + count

        def tally(key, count):
            lt = self.__dict__['__root']["$tally"]

            lt[key] = lt.get(key,0) + count
            
        is_client = self.__dict__["__root"].__dict__['__client']
        parent_type = self.__dict__['__type']

        if not is_client:
            match parent_type:
                case "log" | "glog":
                    now = self.__dict__["__root"].__dict__['__now']
                    self.__dict__["__root"].__dict__['__now'] += 1

                    if not self.__dict__['__document'].get("_frame",None):
                        self.__dict__['__document']["_frame"] = now
                    frame = self.__dict__['__document']["_frame"]

                    if not self.__dict__['__document'].get("_depth",None):
                        self.__dict__['__document']["_depth"] = 256
                    depth = self.__dict__['__document']["_depth"]

                    if not self.__dict__['__document'].get("_size",None):
                        self.__dict__['__document']["_size"] = 32*1024
                    size = self.__dict__['__document']["_size"]

                    if not self.__dict__['__document'].get("_interval",None):
                        self.__dict__['__document']["_interval"] = 60*60*24
                    interval = self.__dict__['__document']["_interval"]

                    if not self.__dict__['__document'].get("_mode",None):
                        self.__dict__['__document']["_mode"] = 1 # Enable server time mode
                    time_type = self.__dict__['__document']["_mode"]

                    if _name.startswith("_"):
                        self.__dict__['__document'][_name] = _value
                    else:
                        if isinstance(_value,dict):
                            _value["_size"] = len(json.dumps(_value))

                        if time_type == -1: # Client defined key
                            ikey = int(_name)
                            time_group = str(ikey - (ikey % interval))
                        else:
                            nowr = now - frame
                            _name = str(nowr)
                            time_group = str(nowr - (nowr % interval))
                            
                        base_key = self.__dict__['__key'].split("~")[0]
                        if parent_type == "glog":
                            stats_handler(self.__dict__['__root']["$id"]["unique"], base_key, _value)
                        else:
                            ltally(base_key, 1)
                            stats_handler(self.__dict__['__root']["$id"]["unique"], base_key)
                
                        log_handler(self.__dict__['__root']["$id"]["serial"], base_key, _name, time_group, _value, self.__dict__['__root'])
                    
                        self.__dict__['__type'] = ""
                        self[_name] = _value
                        self.__dict__['__type'] = parent_type

                        items = [k for (k,v) in self.__dict__['__document'].items() if not k.startswith("_")]
                        items.sort()

                        if len(items) > depth:
                            del self.__dict__['__document'][items.pop(0)]

                        current_size = 0
                        delete_index = 0
                        for item in items:
                            if not isinstance(self.__dict__['__document'][item],dict):
                                continue

                            current_size += self.__dict__['__document'][item]["_size"]
                            while current_size > size:
                                current_size -= self.__dict__['__document'][items[delete_index]]["_size"]
                                del self.__dict__['__document'][items[delete_index]]
                                delete_index += 1

                    self.__dict__['__document']["_vmt"] = self.__dict__['__tsx']
                    #self.__update(self.__dict__['__tsx'],_name, self.__dict__['__document'][_name])
                    self.__dict__['__parent'].__update(self.__dict__['__tsx'], self.__dict__['__key'],{_name:self.__dict__['__document'][_name]})

                    return
                case _:
                    pass
        
        if isinstance(_value,dict) and len(_value):
            if not transaction_config["allow_bulk_assign"]:
                raise BulkAssignmentProhibited()
            
            if not self.__dict__['__document'].get(_name,None):
                self.__dict__['__document'][_name] = {}
            elif not isinstance(self.__dict__['__document'][_name],dict):
                raise ValueReassignmentToDictProhibited()

            sub = self[_name]
            for k,v in _value.items():
                sub[k] = v

            return

        # Value Assignment:

        base_key, value_type = split_key(_name)

        match parent_type:
            case "tally" | "tly" | "ltally" | "lly" | "gly" | "gtally":
                value_type = parent_type
        
        match value_type:
            case "rng" | "random":
                self.__dict__['__document'][_name] = random_handler(_value)

            case "app" | "append":
                base = self.__dict__['__document'].get(_name,"")
                self.__dict__['__document'][_name] = base + _value
                
            case "pre" | "prepend":
                base = self.__dict__['__document'].get(_name,"")
                self.__dict__['__document'][_name] = _value + base
                
            case "flt" | "float":
                base = self.__dict__['__document'].get(_name,0)
                self.__dict__['__document'][_name] = base + _value
                
            case "cnt" | "counter":
                base = self.__dict__['__document'].get(_name,0)
                self.__dict__['__document'][_name] = base + int(_value)

            case "file" | "blocks" | "block" | "folder" | "tfile" | "tblocks" | "tblock" | "tfolder":
                file_handler()
            
            case "ltally" | "lly" | "local_tally":
                """
                    Collects all K:V tally over time by tracking and summing edits only.
                    Doesn't support deletion as it is only computed on mutation and accumulated.
                    Support logs.
                    Local tallys named "like","comments"... etc will automatically be propagated to the stats
                    {
                        something~log:{
                            25151:{files~lly:3}
                        }
                        else~ltally:{
                            files:4
                        },
                        $ltally:
                        {
                            files:7
                        }
                    }
                """

                ltally(base_key, _value - self.__dict__['__document'].get(_name,0))
                self.__dict__['__document'][_name] = _value


            case "tally" | "tly":
                """
                    Collects all current K:V spread throughout the file and sums them in a root key $tally.
                    Supports deletion as is recomputed completely every time.
                    Doesn't support logs as can't recompute the removed log items.
                    {
                        something:{
                            files~tly:3
                        }
                        else~tally:{
                            files:4
                        },
                        $tally:
                        {
                            files:7
                        }
                    }
                """

                # TODO, honor this concept when value is deleted.

                tally(base_key, _value - self.__dict__['__document'].get(_name,0))
                self.__dict__['__document'][_name] = _value
                
            case _:
                self.__dict__['__document'][_name] = _value
            
        self.__dict__['__document']["_vmt"] = self.__dict__['__tsx']
        self.__dict__['__parent'].__update(self.__dict__['__tsx'], self.__dict__['__key'],{_name:self.__dict__['__document'][_name]})
        #self.__update(self.__dict__['__tsx'],_name, self.__dict__['__document'][_name])

    def __getattr__(self, _name: str):
        _name = str(_name)
        _name = _name.replace("_type_","~").replace("_server_","$")
        _value = self.__dict__['__document'].get(_name,None)

        if _value is None and self.__dict__['__root'].__dict__['__auto_nav'] and not self.__dict__['__root'].__dict__['__read_only']:
            if _name.startswith("__") and _name.endswith("__"):
                return None
            self.__dict__['__document'][_name] = {}
            _value = self.__dict__['__document'][_name]

        if isinstance(_value, dict):
            return Transaction(_value, self.__dict__['__tsx'], _name, self, type_lookup(_name,_value), self.__dict__["__root"], self.__dict__["__owner"] if self.__dict__["__owner"] else self.__dict__["__document"].get("~owner", None))

        return _value
    
    def __setitem__(self, _name: str, _value: Any) -> None:
        return self.__setattr__(_name,_value)
    
    def __getitem__(self, _name: str):
        return self.__getattr__(_name)