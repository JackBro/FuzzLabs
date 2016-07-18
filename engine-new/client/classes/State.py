# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class State(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self):
        self.jobs = {}
        self.active = None

