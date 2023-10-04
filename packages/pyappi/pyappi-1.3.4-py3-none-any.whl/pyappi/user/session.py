from pyappi.encoding.url import decode_url
from pyappi.api_base import get_document_type
import json
from fastapi import Response
from functools import wraps
import time


from Crypto.Cipher import AES
from Crypto import Random


from hashlib import sha512
from pyappi.encoding.url import encode_url, decode_url


class AESCipher:
    def __init__( self, challenge ):
        h512 = sha512()
        h512.update(challenge.encode())

        dg = h512.digest()

        self.key = dg[0:32]
        self.iv = dg[32:48]

    def encrypt( self, raw ):
        cipher = AES.new( self.key, AES.MODE_OFB, self.iv )
        return cipher.encrypt( raw )

    def decrypt( self, enc ):
        cipher = AES.new(self.key, AES.MODE_OFB, self.iv )
        return cipher.decrypt( enc )


def generate_token(session):
    if not session["challenge"]:
        return ""

    pw = AESCipher(session["challenge"])

    b64random = encode_url(Random.new().read( 64 ))

    payload = f'{b64random}|{int(time.time())}|UserToken|{session["user"]}|{session["device"]}'

    return encode_url(pw.encrypt(payload.encode()))


def verify_token(session, challenge):
    pw = AESCipher(challenge)
    bin = decode_url(session["token"])

    s = pw.decrypt(bin).decode()

    parts = s.split("|")

    return parts[3] == session.get("user","")


def verify_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs["request"]
        _session = get_user_session(request)
        if not _session:
            return Response(status_code=403)
    
        session, user = _session
        request.state.session = session
        request.state.user = user

        return await func(*args, **kwargs)

    return wrapper

def parse_session(blob):
    return json.loads(decode_url(blob).decode())

def validate_user_session(request):
    raw_session = request.query_params._list[0][0]
    session = parse_session(raw_session)
    
    with get_document_type()(f'user.{session["user"]}', session["user"], read_only=True) as doc:
        return session["challenge"] == doc.auth.challenge
    
    return False

def get_user_session(request):
    raw_session = request.query_params._list[0][0]
    session = parse_session(raw_session)
    
    try:
        with get_document_type()(f'user.{session["user"]}', session["user"], read_only=True) as doc:
            session["id"] = doc._server_id.serial

            if not session["challenge"]:
                return (session,doc) if verify_token(session, doc.auth.challenge) else None
            else:
                return (session,doc) if session["challenge"] == doc.auth.challenge else None
    except Exception as _e:
        pass
    
    return None