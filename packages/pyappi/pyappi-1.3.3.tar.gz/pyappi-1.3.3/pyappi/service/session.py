from functools import wraps
from fastapi import Response
from pyappi.user.session import parse_session
import os
import json
import base64

service_config = {
    "root": "appidb/service",
}

if not os.path.exists(service_config["root"]):
    os.makedirs(service_config["root"],exist_ok=True)

    try:
        with open(service_config["root"] + "/services.json", "w") as doc:
            key = base64.b64encode(os.urandom(32)).decode()
            doc.write(json.dumps({
                "services":{
                    "default":key
                }
            } , indent=4))
    except Exception as e:
        pass

def lookup_service_key(name="default"):
    try:
        with open(service_config["root"] + "/services.json", "r") as doc:
            services = json.load(doc)["services"]

            return services.get(name,None)
    except Exception as _e:
        return None

def get_service_session(request):
    raw_session = request.query_params._list[0][0]
    session = parse_session(raw_session)

    key = lookup_service_key(session["user"])
    
    return session, session["user"] if key == session["challenge"] else None


def verify_service(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs["request"]
        _session = get_service_session(request)
        if not _session:
            return Response(status_code=403)
    
        session, service = _session
        request.state.session = session
        request.state.user = service

        return await func(*args, **kwargs)

    return wrapper