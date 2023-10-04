import json
import os


enumeration_config = {
    "enable": True,
    "enumeration_root": "appidb/document_enumeration"
}


if enumeration_config["enumeration_root"]:
    os.makedirs(enumeration_config["enumeration_root"],exist_ok=True)

filename = f'{enumeration_config["enumeration_root"] }/serial_to_unique.json'
backup = f'{enumeration_config["enumeration_root"] }/serial_to_unique.backup.json'

def _get_lookup():
    lookup = {}
    try:
        with open(filename) as fh:
            lookup = json.load(fh)
    except Exception as e:
        pass

    return lookup

def lookup_document_id(serial):
    lookup = _get_lookup()

    return lookup.get(str(serial),"")

def is_new_document(document):
    return not len(document["auth"])

def enumerate_document_id(document_id):

    lookup = _get_lookup()

    try:
        os.remove(backup)
    except OSError:
        pass

    try:
        os.rename(filename, backup)
    except OSError:
        pass

    enumerator = len(lookup)
    lookup[enumerator] = document_id

    with open(filename, "w") as doc:
        doc.write(json.dumps(lookup, indent=4))

    return enumerator


def prepare_new_document(document, document_id):
    if not enumeration_config["enable"]:
        return
    
    document["$id"].serial = enumerate_document_id(document_id)
    document["$id"].unique = document_id