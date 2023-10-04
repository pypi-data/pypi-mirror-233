config = {}

def use_test_config():
    global config
    config = {
        "protocol":"",
        "host":""
    }

    return config

def use_local_config():
    global config
    config = {
        "protocol":"http://",
        "host":"127.0.0.1"
    }

    return config

def set_config(_config):
    global config
    config = _config

    return config

def get_config():
    return config