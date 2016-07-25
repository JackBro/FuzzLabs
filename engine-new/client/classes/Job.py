from classes.Utils import Utils

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Job(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.grammar = None
        self.session = {
            "sleep_time": 0,
            "restart_sleep_time": 0,
            "timeout": 10,
            "skip": 0
        }
        self.target = {
            "transport": {
                "media": None,
                "protocol": None
            },
            "endpoint": {}
        }
        self.conditions = {
        }
        self.agent = {
        }
        self.graph = []

