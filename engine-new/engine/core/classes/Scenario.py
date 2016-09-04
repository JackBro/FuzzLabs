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

    def __init__(self, uuid, job, config, scenario):
        self.worker_id  = uuid
        self.sleep_time = 0
        self.completed  = False
        self.job        = job
        self.config     = config
        self.name       = scenario.get('name')
        if not self.name:
            self.name  = Utils.generate_name()
        self.units     = []

        if self.job.get('session').get('sleep_time'):
            self.sleep_time = self.job.get('session').get('sleep_time')

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
                m_hdr = "[i] %s/%s/%s" % (self.worker_id, self.name, unit.get('name'))
                print m_hdr + ": connect()"
                for r_unit in self.units:
                    print m_hdr + ": send(" + r_unit.render() + ")"
                    print m_hdr + ": recv()"
                    time.sleep(self.sleep_time)
                print m_hdr + ": close()"
        self.completed = True

