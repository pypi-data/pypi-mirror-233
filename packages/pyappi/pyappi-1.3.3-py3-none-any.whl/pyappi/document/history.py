import json
import time
import os
from pyappi.util.filename import clean_filename


history_config = {
    "enable": True,
    "document_history_root": "appidb/document_history"
}


def read_history(name):
    print("tdo read history", name)

    return {}


if history_config["document_history_root"]:
    os.makedirs(history_config["document_history_root"],exist_ok=True)


def update_document_history(user_id, document_id, new_tsx, is_public,delta):
    if not history_config["enable"]:
        return

    name = clean_filename(f'{history_config["document_history_root"]}/history.{document_id}.json')

    current = {"time":int(time.time()),"user":user_id,"tsx":new_tsx,"pub":is_public,"delta":delta}

    with open(name, "a") as doc:
        doc.write(json.dumps(current , indent=4))