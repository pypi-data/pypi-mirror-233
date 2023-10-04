from hashlib import sha256
from pyappi.encoding import encode_url
import os.path

def read1(type, id):
    try:
        with open(f'blocks/{type}/{id}', mode='rb') as file:
            return file.read()
    except Exception as e:
        return

def write1(type, content):
    h256 = sha256()
    h256.update(content)

    id = encode_url(h256.digest())
    
    with open(f'blocks/{type}/{id}', mode='wb') as file:
        file.write(content)
    
    return id

def is1(type,id):
    return {"id": 1 if os.path.isfile(f'blocks/{type}/{id}') else 0 }

def read2(type, id):
    return read1(type, id)

def write2(type, id, content):
    with open(f'blocks/{type}/{id}', mode='wb') as file:
            return file.write(content)

def is2(type,id):
    return is1(type,id)