from hashlib import sha256,sha512
from pyappi.encoding.url import encode_url, decode_url
import json


def secure_user(user):
    h256 = sha256()
    h256.update((user + 'APPI-DOMAIN-06036F34-78A8-45A7-B96D-646BE001039C').encode())

    return encode_url(h256.digest())

def secure_challenge(challenge, user):
    h512 = sha512()
    h512.update((challenge + user + 'APPI-DOMAIN-C3A09828-1AEB-4486-9BDE-010A035FE92C').encode())

    return encode_url(h512.digest())

def session_challenge(_user="", _challenge="", params = {}):
    user = secure_user(_user) if _user else ""
    challenge = secure_challenge(_challenge, user) if _challenge else ""
    session = {}
    session.update({"user": user, "challenge": challenge})
    session.update(params)
    bin = json.dumps(session).encode()

    return encode_url(bin)

def make_session(_user="", _challenge="", params = {}):
    user = secure_user(_user) if _user else ""
    challenge = secure_challenge(_challenge, user) if _challenge else ""
    session = {}
    session.update({"user": user, "challenge": challenge})
    session.update(params)
    
    return session

def encode_session(session):
    bin = json.dumps(session).encode()

    return encode_url(bin)

def decode_session(session):
    return json.loads(decode_url(session).decode())