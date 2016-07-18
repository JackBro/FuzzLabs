import os
import cmd
import sys
import pprint
import inspect
from classes.State import State
from classes.Job import Job

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class CliJob(cmd.Cmd):
    ruler = '-'
    prompt = 'fuzzlabs > '

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, config, job, completekey='tab', stdin = None, stdout = None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        self.config = config
        self.job    = job
        self.pp     = pprint.PrettyPrinter(indent=2, width=80)
        self.prompt = 'fuzzlabs (%s) > ' % self.job.name

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_save(self, args):
        'Save current job configuration.'
        self.pp.pprint(self.job)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_shell(self, args):
        'Execute operating system command.'
        os.system(args)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_exit(self, args):
        return True

