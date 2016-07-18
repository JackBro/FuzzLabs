NAME    = "api"
DESC    = "HTTP application programming interface"
VERSION = "0.0.1"

class module(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self):
        self.name     = NAME
        self.desc     = DESC
        self.version  = VERSION
        self.service  = None

    def shutdown(self):
        return True

