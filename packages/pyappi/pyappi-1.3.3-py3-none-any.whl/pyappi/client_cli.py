import pyappi
from colorama import Fore, Style
import httpx
import click
import json
import os

from pyappi.util.login import session_challenge


def resolve_session(user, password):
    if user and password:
        return session_challenge(user, password)
    
    if os.path.exists("appi_session.b64"):
        with open("appi_session.b64","r") as file:
            return file.read()
        
    return ""

def resolve_config(host, proto):
    if host and proto:
        return (host, proto)

    try:
        with open("appi_config.json","r") as file:
            cfg = json.load(file)

            return (cfg["host"], cfg["proto"])
    except Exception as e:
        pass


@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="http", help="Protocol string, usually http or https")
@click.option("--host", default="127.0.0.1:8099", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def read(cmd, id, proto, host, user, password, data):
    (host, proto) = resolve_config(host,config)

    result = httpx.get(f"{proto}://{host}/document/{id}?{resolve_session(user,password)}")
    print(cmd, id, result,result.status_code)


@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="https", help="Protocol string, usually http or https")
@click.option("--host", default="appi.host/api", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def write(cmd, id, proto, host, user, password, data):
    (host, proto) = resolve_config(host,config)

    write = json.parse(data)
    result = httpx.put(f"{proto}://{host}/document/{id}?{resolve_session(user,password)}", json=write)
    print(cmd, id, result,result.status_code)


@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="https", help="Protocol string, usually http or https")
@click.option("--host", default="appi.host/api", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def utail(cmd, id, proto, host, user, password, data):
    from pyappi.client.sync import UserTail
    import time

    session = resolve_session(user,password)
    (host, proto) = resolve_config(host,config)
    
    tail = UserTail(session=session,config={"host":host,"protocol":proto})
    time.sleep(9999999)


@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="https", help="Protocol string, usually http or https")
@click.option("--host", default="appi.host/api", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def stail(cmd, id, proto, host, user, password, data):
    print("TODO")


@click.command()
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
def login(user, password):
    session = session_challenge(user, password)

    with open("appi_session.b64","w") as file:
        file.write(session)

@click.command()
@click.option("--proto", default="https", help="Protocol string, usually http or https")
@click.option("--host", default="appi.host/api", help="Host name or ip address with optional port after a :")
def config(host, proto):
    with open("appi_config.json","w") as file:
        file.write(json.dumps({
            "host": host,
            "proto": proto
        }))

@click.command()
def logout():
    try:
        os.remove("appi_session.b64")
    except Exception as _e:
        pass

@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="http", help="Protocol string, usually http or https")
@click.option("--host", default="", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def main(cmd, id, proto, host, user, password):
    match cmd:
        case "read":
            return read()
        case "utail":
            return utail()
        case "stail":
            return stail()
        case "write":
            return write()
        case "login":
            return login()
        case "config":
            return config()
        case "logout":
            return logout()
        case "about":
            print(f"{Fore.GREEN}PYAPPI-CLIENT {pyappi.__version__}{Style.RESET_ALL}")

if __name__ == "__main__":

    
    main()