import httpx
from fastapi.testclient import TestClient
from pyappi.client.config import use_test_config, get_config
from pyappi.client.session import set_session
from pyappi.util.login import session_challenge
from pyappi.util.login import secure_user


client_handle = httpx


def create_user(user, password, body={}):
    client, config = get_connection_details()
    session = session_challenge(user,password)
    response = client.post(f'{config["protocol"]}{config["host"]}/user/create/{secure_user(user)}?{session}', json=body)


def use_test_client():
    global client_handle
    use_test_config()

    import pyappi.endpoints # This line is required to load the FastAPI enpoints
    from pyappi.api_base import app, set_document_type
    from pyappi.document import Document

    set_document_type(Document)

    client_handle = TestClient(app)
    default_session = set_session("TESTUSER","TESTPASSWORD")
    
    client, config = get_connection_details()
    body = {
        "profile":{}
    }

    create_user("TESTUSER2", "TESTPASSWORD2", body)
    create_user("TESTUSER3", "TESTPASSWORD3", body)
    create_user("TESTUSER","TESTPASSWORD", body)

    return client_handle

def set_client(_client):
    global client_handle
    client_handle = _client

    return client_handle

def get_client():
    global client_handle
    return client_handle

def get_connection_details():
    global client_handle
    return client_handle, get_config()