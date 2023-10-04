from pyappi.document.transaction import Transaction

def server_merge(document, write):
    for k, _ in write.items():
        o = document.get(k,None)
        if isinstance(write[k], dict) and (not isinstance(document,Transaction) or (isinstance(o, Transaction) or isinstance(o, dict))): 
            server_merge(document[k], write[k])
        else:
            document[k] = write[k]
    