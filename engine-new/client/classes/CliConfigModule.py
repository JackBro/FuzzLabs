import os
import cmd
import sys
import json
import pprint
import inspect
import httplib
from classes.Utils import Utils
from classes.State import State
from classes.Job import Job

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class CliConfigModule(cmd.Cmd):
    ruler = '-'
    prompt = 'fuzzlabs(modules) > '

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, config, loader, modules, completekey='tab', 
                 stdin = None, stdout = None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        self.config  = config
        self.loader  = loader
        self.modules = modules
        self.pp      = pprint.PrettyPrinter(indent=2, width=80)

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

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_load(self, args):
        self.loader.loadModule(args)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_unload(self, args):
        self.loader.unloadModule(args)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_reload(self, args):
        rc = self.loader.unloadModule(args)
        if rc:
            rc = self.loader.loadModule(args)
        if not rc:
            print "[e] failed to reload module '%s'" %\
                  (args)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_list(self, args):
        args = args.split(" ")
        available = self.loader.getModules()
        skip = []

        print
        print "%-15s\t%-6s\t\t%s" % ("Name", "Status", "Description")
        print "-" * 80

        for module in self.modules:
            state = "loaded"
            if self.modules[module].service:
                state = "active"
            print "%-15s\t%-6s\t\t%s" % (module, state, self.modules[module].desc)
            if module in available: skip.append(module)
        for module in available:
            if module not in skip:
                print "%-15s\t%-6s\t\t%s" % (module, "available", "")
        print

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_list(self):
        print "\nList all modules.\n"

