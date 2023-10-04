def type_lookup(name, object = {}):
    type = ""

    if name.find('~') != -1:
        type = name.split("~")[-1]

    return type or object.get("_~","")

def base_key(name):
    return name.split("~")[0]

def split_key(name, object = {}):
    return base_key(name), type_lookup(name, object)