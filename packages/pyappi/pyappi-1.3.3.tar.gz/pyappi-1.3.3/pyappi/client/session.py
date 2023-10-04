from pyappi.util.login import session_challenge

session = {}

def get_session():
    global session
    return session

def set_session(user, password, more={}):
    global session
    session = session_challenge(user, password, more)

    return session