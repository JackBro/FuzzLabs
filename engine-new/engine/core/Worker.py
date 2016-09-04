#!/usr/bin/env python
import os
import time
import inspect
import threading
from classes.Utils import Utils
from classes.Config import Config
from classes.Scenario import Scenario
from logic.Linear import Linear
from primitives.block import block

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Worker(threading.Thread):

    def __init__(self, config, uuid, job):
        threading.Thread.__init__(self)
        self.config    = config
        self.uuid      = uuid
        self.job       = Utils.read_json(job)
        self.scenarios = []

        t_scenarios    = self.job.get('scenarios')

        if not t_scenarios:
            raise Exception("worker '%s' failed to initialize job '%s': %s" %\
                  (self.uuid, self.job.get('id'),
                  "no scenarios defined"))

        for scenario in t_scenarios:
            try:
                self.scenarios.append(Scenario(self.config, scenario))
            except Exception, ex:
                raise Exception("worker '%s' failed to initialize job '%s': %s (%s)" %\
                      (self.uuid, self.job.get('id'),
                      "failed to initialize scenario", str(ex)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        for scenario in self.scenarios:
            print "[i] running scenario: %s" % scenario.get('name')
            scenario.run()


# -----------------------------------------------------------------------------
# This is just to be able to easily test the mutation engine
# -----------------------------------------------------------------------------

ROOT = os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe()
            )))
config = Config(ROOT, "/../config/config.json")
w = Worker(config, None, "../jobs/9b2ee5b0384d2cfe9698cc1a5d310702.job")
w.start()

