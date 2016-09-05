#!/usr/bin/env python
import os
import time
import inspect
import threading
from classes.Utils import Utils
from classes.Config import Config
from classes.Logger import Logger
from classes.Scenario import Scenario
from classes.MutationsExhaustedException import MutationsExhaustedException

# -----------------------------------------------------------------------------
# A mock media class for testing. To be removed once media drivers are ready
# to use.
# -----------------------------------------------------------------------------

class mock_media:

    def __init__(self):
        pass

    def connect(self):
        print "CONNECT"

    def disconnect(self):
        print "DISCONNECT"

    def send(self, data):
        print "SEND: " + data

    def receive(self):
        print "RECEIVE"

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
                self.scenarios.append(Scenario(self.config,
                                               scenario_id, 
                                               self.job))
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
        media = mock_media()
        for scenario in self.scenarios:
            print "[i] %s/%s" % (self.id, scenario.get('name'))
            try:
                for iteration in scenario.run():
                    if iteration.get('state') == "connect":
                        media.connect()
                        scenario.stateConnected()
                        continue
                    if iteration.get('state') == "disconnect":
                        media.disconnect()
                        scenario.stateDisconnected()
                        continue
                    media.send(iteration.get('data'))
                    data = media.receive()
            except MutationsExhaustedException, mex:
                pass
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

