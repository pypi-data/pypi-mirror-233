from threading import RLock

import os
import json


event_config = {
    "root": "appidb/events",
}


if not os.path.exists(event_config["root"]):
    os.makedirs(event_config["root"],exist_ok=True)

    try:
        with open(event_config["root"] + "/events.json", "w") as doc:
            doc.write(json.dumps({
                "start": 0,
                "events": {}
            } , indent=4))
    except Exception as e:
        pass


event_lock = RLock()


def publish_event(event):
    MAX_EVENTS = 10000
    overflow = False
    with event_lock:
        head_file = event_config["root"] + "/events.json"
        with open(head_file, "r") as doc:
            db = json.load(doc)
            events = db["events"]
            current = len(events)

            current += 1

            events[str(current)] = event

            if current > MAX_EVENTS:
                overflow = True
                offset = db["start"] + MAX_EVENTS
                archive_file = f'{event_config["root"]}/events{db["start"]}.json'

        if overflow:
            with open(archive_file, "w") as doc:
                doc.write(json.dumps(db, indent=4))

            with open(head_file, "w") as doc:
                doc.write(json.dumps({
                    "start": offset,
                    "events":{}
                } , indent=4))
        else:
            with open(head_file, "w") as doc:
                doc.write(json.dumps(db , indent=4))

def read_cursor():
    head_file = event_config["root"] + "/events.json"
    with open(head_file, "r") as doc:
        db = json.load(doc)

        events = db["events"]
        current = len(events)

        return {"cursor": db["start"] + current + 1}


def read_events(start):
    MAX_EVENTS = 10000
    result = {"archive": False, "events": {}}
    events = result["events"]

    def copy_events(db, start):
        event = db["events"].get(str(start), None)
        while event:
            events[start] = event
            start += 1
            event = db["events"].get(str(start), None)

    with event_lock:
        head_file = event_config["root"] + "/events.json"
        with open(head_file, "r") as doc:
            db = json.load(doc)

            if db["start"] > start:
                result["archive"] = True
            else:
                copy_events(db, start)

        if result["archive"]:
            archive_file = f'{event_config["root"]}/events{start%MAX_EVENTS}.json'
            with open(archive_file, "r") as doc:
                db = json.load(doc)

                copy_events(db, start)

    return result