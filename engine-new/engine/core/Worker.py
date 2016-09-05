#!/usr/bin/env python
import os
import time
import inspect
import threading
from classes.Utils import Utils
from classes.Config import Config
from classes.Logger import Logger
from classes.Scenario import Scenario

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Worker(threading.Thread):

    def __init__(self, logger, config, uuid, job):
        threading.Thread.__init__(self)
        self.logger    = logger
        self.config    = config
        self.id      = uuid
        self.job       = None
        self.scenarios = []

        try:
            self.job = Utils.read_json(job)
        except Exception, ex:
            msg = self.logger.log("failed to initialize job", "error",
                            str(ex),
                            self.id,
                            self.job.get('id'))
            raise Exception(msg)

        t_scenarios = self.job.get('scenarios')

        if not t_scenarios:
            msg = self.logger.log("failed to initialize job", "error",
                            "no scenarios defined",
                            self.id,
                            self.job.get('id'))
            raise Exception(msg)

        for scenario_id in range(0, len(t_scenarios)):
            try:
                self.scenarios.append(Scenario(scenario_id, 
                                               self.job, 
                                               self.config))
            except Exception, ex:
                msg = self.logger.log("failed to initialize scenarios", "error",
                                str(ex),
                                self.id,
                                self.job.get('id'))
                raise Exception(msg)
            scenario_id += 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        for scenario in self.scenarios:
            print "[i] %s/%s" % (self.id, scenario.get('name'))
            try:
                scenario.run()
            except Exception, ex:
                msg = self.logger.log("failed to execute scenarios", "error",
                                str(ex),
                                self.id,
                                self.job.get('id'),
                                scenario.get('name'))
                raise Exception(msg)

# -----------------------------------------------------------------------------
# This is just to be able to easily test the mutation engine
# -----------------------------------------------------------------------------

ROOT = os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe()
            )))
config = Config(ROOT, "/../config/config.json")
logger = Logger()

w = Worker(
        logger,
        config,
        Utils.generate_name(), 
        "../jobs/9b2ee5b0384d2cfe9698cc1a5d310702.job")
w.start()

