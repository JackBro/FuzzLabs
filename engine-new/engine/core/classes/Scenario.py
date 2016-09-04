#!/usr/bin/env python
import os
import time
import inspect
import threading
from classes.Utils import Utils
from classes.Config import Config
from logic.Linear import Linear
from primitives.block import block

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Scenario(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, config, scenario):
        self.completed = False
        self.config    = config
        self.name      = scenario.get('name')
        if not self.name:
            self.name  = Utils.generate_name()
        self.units     = []

        for unit in scenario.get('units'):
            self.units.append(self.load_unit(unit))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def load_unit(self, unit):
        u_path = self.config.get('root') + "/../units/" + unit + ".json"
        try:
            data = Utils.read_json(u_path)
            return block(data)
        except Exception, ex:
            raise Exception("worker '%s' failed to load unit '%s': %s" %\
                  (self.uuid, unit, str(ex)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        for unit in self.units:
            while not unit.completed:
                unit.mutate()
                print "-"*80
                print "connect()"
                for r_unit in self.units:
                    print "send(" + r_unit.render() + ")"
                    print "recv()"
                print "close()"
        import time
        self.completed = True

