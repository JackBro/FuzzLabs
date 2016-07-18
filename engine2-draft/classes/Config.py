from classes.Utils import Utils

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Config(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, root, filename):
        self.root = root
        self.config = Utils.read_json(root + filename)

