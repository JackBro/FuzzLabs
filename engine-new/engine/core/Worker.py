#!/usr/bin/env python
import time
import threading
from classes.Utils import Utils
from logic.Linear import Linear
from primitives.block import block

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

STATE_UNINIT  = 0
STATE_INIT    = 1 
STATE_RUNNING = 2
STATE_PAUSED  = 3
STATE_STOPPED = 4

# -----------------------------------------------------------------------------
# NOTE: This is currently just a draft, not ready to be used and probably 
#       contains several bugs.
# -----------------------------------------------------------------------------

class Worker(threading.Thread):

    def __init__(self, config, uuid, job, grammar):
        threading.Thread.__init__(self)
        self.config  = config
        self.uuid    = uuid
        self.job     = job
        self.state   = STATE_UNINIT
        self.data    = None

        try:
            self.data = Utils.read_grammar(grammar)
            self.data = block(self.data)
        except Exception, ex:
            self.state = STATE_UNINIT
            """ TEMPORARILY COMMENTED
            raise Exception("worker '%s' failed to initialize job '%s': %s" %\
                  (self.uuid, self.job.get('id'), str(ex)))
            """

        self.state = STATE_INIT

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        if self.state != STATE_INIT:
            raise Exception("worker '%s' attempted to run uninitialized job '%s'" %\
                  (self.uuid, self.job.get('id')))

        self.state = STATE_RUNNING

        for iteration in Linear(self.data).run():
            if self.state == STATE_STOPPED: break
            while self.state == STATE_PAUSED: time.sleep(1)
            if iteration:
                print "".join(iteration)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def stop(self):
        if self.state != STATE_RUNNING:
            raise Exception("worker '%s' attempted to stop non-running job '%s'" %\
                  (self.uuid, self.job.get('id')))

        self.state = STATE_STOPPED

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def pause(self):
        if self.state != STATE_RUNNING:
            raise Exception("worker '%s' attempted to pause non-running job '%s'" %\
                  (self.uuid, self.job.get('id')))

        self.state = STATE_PAUSED

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def resume(self):
        if self.state not in [STATE_PAUSED, STATE_STOPPED]:
            raise Exception("worker '%s' attempted to resume job '%s' from invalid state: %d" %\
                  (self.uuid, self.job.get('id'), self.state))

        self.state = STATE_RUNNING


# This is just to be able to easily test the mutation engine

w = Worker(None, None, None, "./grammars/packet.json")
w.start()

