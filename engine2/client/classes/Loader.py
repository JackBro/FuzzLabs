import os
import glob
import importlib
from stat import *

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Loader(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, config):
        self.root    = config.get('root')
        self.config  = config.get('data').get('modules')
        self.modules = {}

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def getModules(self):
        m = []
        for module in os.listdir(self.root + "/modules"):
            mode = os.stat(self.root + "/modules/" + module).st_mode
            if not S_ISDIR(mode): continue
            m.append(module)
        return m

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def loadModule(self, module):
        mentry = None
        if module in list(self.modules):
            print "[e] module '%s' already loaded" % module
            return False

        try:
            mentry = importlib.import_module("modules." + module + ".module")
        except Exception, ex:
            print ("[e] failed to import module '%s': %s" %\
                  (module, str(ex)))
            return False

        try:
            minst = getattr(mentry, "module")()
        except Exception, ex:
            print ("[e] failed to load module '%s': %s" %\
                  (module, str(ex)))
            return False

        self.modules[module] = minst
        return self.modules

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def loadModules(self):
        for module in self.getModules():
            self.loadModule(module)
        return self.modules

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def unloadModule(self, module):
        rc = True
        if len(module) == 0:
            print "[e] not module specified"
            return False
        try:
            um = self.modules.pop(module)
            if um.shutdown():
                del um
            else:
                self.modules[module] = um
                print "[e] failed to shut down module '%s'" %\
                      (module)
                rc = False
        except Exception, ex:
            print "[e] failed to unload module '%s': %s" %\
                  (module, str(ex))
            self.modules[module] = um
            rc = False
        return self.modules

