from threading import RLock

class SuperRLock:
    def __init__(self, p=100):
        self.locks = []

        for i in range(p):
            self.locks.append(RLock())

    @staticmethod
    def handler(update, parent):
        print(update)

    def __enter__(self):
        self.client = RawClientEvents(UserTail.handler,self.interval,self.config,self.session)

        return self
    
    def __exit__(self, type, value, traceback):
        self.client.stop()