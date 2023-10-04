from pyappi.document.delta import changes_since
from pyappi.api_base import get_document_type
import os
import json


local_config = {
    "enable": True,
    "user_local_tsx_root": "appidb/user_local_tsx",
}

if local_config["user_local_tsx_root"]:
    os.makedirs(local_config["user_local_tsx_root"],exist_ok=True)

def sync_user_local_transaction(tsx, user_id):
    with get_document_type()(f'local_tsx.{user_id}', user_id,local_config["user_local_tsx_root"]) as doc:
        return changes_since(doc,tsx)
    
def sync_user_local_transaction2(tsx, user_id):
    with get_document_type()(f'local_tsx.{user_id}', user_id,local_config["user_local_tsx_root"]) as doc:
        return changes_since(doc,tsx) if tsx != -1 else {}, doc._cmt

def sync_root(user_id):
    with get_document_type()(f'local_tsx.{user_id}', user_id,local_config["user_local_tsx_root"]) as doc:
        return doc.unwrap()


def update_user_local_transaction(user_id, document_id, new_tsx, is_public):
    name = f'{local_config["user_local_tsx_root"]}/local_tsx.{user_id}.json'
    current = {}
    try:
        with open(name) as document_handle:
            current = json.load(document_handle)
    except Exception as e:
        pass

    tsx = current.get("_cmt",0) + 1

    current[document_id] = {"tsx":new_tsx,"pub":int(is_public),"_vmt":tsx}

    current["_cmt"] = tsx

    try:
        with open(name, "w") as doc:
            doc.write(json.dumps(current , indent=4))
    except Exception as e:
        pass