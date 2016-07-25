#!/usr/bin/env python
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
        self.grammar = None
        try:
            grammar = Utils.read_grammar(self.job.get('grammar'))
        except Exception, ex:
            self.state = STATE_UNINIT
            raise Exception("worker '%s' failed to initialize job '%s': %s" %\
                  (self.uuid, self.job.get('id'), str(ex))
        self.state = STATE_INIT

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        if self.state != STATE_INIT:
            raise Exception("worker '%s' attempted to run uninitialized job '%s'" %\
                  (self.uuid, self.job.get('id'))

        self.state = STATE_RUNNING

        """
        for iteration in Linear(grammar).run():
            if iteration:
                print "".join(iteration)
        """

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def stop(self):
        if self.state != STATE_RUNNING:
            raise Exception("worker '%s' attempted to stop non-running job '%s'" %\
                  (self.uuid, self.job.get('id'))

        self.state = STATE_STOPPED

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def pause(self):
        if self.state != STATE_RUNNING:
            raise Exception("worker '%s' attempted to pause non-running job '%s'" %\
                  (self.uuid, self.job.get('id'))

        self.state = STATE_PAUSED

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def continue(self):
        if self.state not in [STATE_PAUSED, STATE_STOPPED]:
            raise Exception("worker '%s' attempted to resume job '%s' from invalid state: %d" %\
                  (self.uuid, self.job.get('id'), self.state)

        self.state = STATE_RUNNING

