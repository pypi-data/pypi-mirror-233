import os
import time
import json
from threading import RLock, Lock
from pyappi.util.filename import clean_filename
from pyappi.util.interval import Interval


stats_config = {
    "enable": True,
    "stats_root": "appidb/stats",
}

if stats_config["stats_root"]:
    os.makedirs(stats_config["stats_root"],exist_ok=True)


sessions = {}

stats_record_mutex = Lock()
session_lock = RLock()

def close_session(session_id):
    target_id, user_id = session_id.split("|")

    with StatsRecord(target_id) as record:
        record["viewers"] -= 1

    with session_lock:
        del sessions[session_id]

def session_cleanup():
    now = int(time.time())
    with session_lock:
        to_close = []
        for session_id, session in sessions.items():
            if session["last_live"] + 60 < now:
                to_close.append(session_id)

        for session_id in to_close:
            close_session(session_id)
            

session_cleanup_interval = None

def use_session_interval():
    global session_cleanup_interval
    session_cleanup_interval = Interval(60,session_cleanup)


def read_stats(name):
    filename = clean_filename(f'{stats_config["stats_root"] }/{name}.json')
    with open(filename) as document_handle:
        return json.load(document_handle)


class StatsRecord():
    def __init__(self, name):
        self.name = name
        self.record = {"views":0,"viewers":0,"likes":0,"followers": 0, "favorites":0,"time":0,"comments":0,"reviews":0, "subscribers": 0}

    def __enter__(self):
        stats_record_mutex.acquire()

        try:
            filename = clean_filename(f'{stats_config["stats_root"] }/{self.name}.json')
            with open(filename) as document_handle:
                self.record = json.load(document_handle)
        except Exception as e:
            pass

        return self.record
    
    def delete(self):
        filename = clean_filename(f'{stats_config["stats_root"] }/{self.name}.json')

        try:
            os.remove(filename)
        except OSError:
            pass
    
    def __exit__(self, type, value, traceback):
        filename = clean_filename(f'{stats_config["stats_root"] }/{self.name}.json')
        backup = clean_filename(f'{stats_config["stats_root"] }/{self.name}.backup.json')

        try:
            os.remove(backup)
        except OSError:
            pass

        try:
            os.rename(filename, backup)
        except OSError:
            pass
        
        try:
            with open(filename, "w") as doc:
                doc.write(json.dumps(self.record , indent=4))
        except Exception as e:
            pass

        stats_record_mutex.release()



def start_viewing_session(target_id,user_id):
    session_id = f"{target_id}|{user_id}"

    if session_id in sessions:
        return update_viewing_sesison(target_id,user_id)
    
    with StatsRecord(target_id) as record:
        record["views"] += 1
        record["viewers"] += 1

    now = int(time.time())
    
    sessions[session_id] = {
        "started": now,
        "last_live": now
    }

    return record

def update_viewing_sesison(target_id,user_id):
    with session_lock:
        session_id = f"{target_id}|{user_id}"

        if not session_id in sessions:
            return start_viewing_session(target_id,user_id)
        
        now = int(time.time())
        
        sessions[session_id] = {
            "last_live": now
        }
    
    with StatsRecord(target_id) as record:
        return record