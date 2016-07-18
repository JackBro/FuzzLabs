#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cmd
import sys
import pprint
import inspect
from classes.Config import Config
from classes.Loader import Loader
from classes.State import State
from classes.Job import Job
from classes.CliJob import CliJob

__VERSION__ = "0.0.1"
INTRO="""
                                                                                 
 _|_|_|_|                                _|                  _|                  
 _|        _|    _|  _|_|_|_|  _|_|_|_|  _|          _|_|_|  _|_|_|      _|_|_|  
 _|_|_|    _|    _|      _|        _|    _|        _|    _|  _|    _|  _|_|      
 _|        _|    _|    _|        _|      _|        _|    _|  _|    _|      _|_|  
 _|          _|_|_|  _|_|_|_|  _|_|_|_|  _|_|_|_|    _|_|_|  _|_|_|    _|_|_|    
                                                                                 
"""

ROOT_DIR = os.path.dirname(
                os.path.abspath(
                    inspect.getfile(inspect.currentframe()
                )))

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Cli(cmd.Cmd):
    intro  = INTRO + 'FuzzLabs Fuzzing Framework ' + __VERSION__
    ruler = '-'
    prompt = 'fuzzlabs > '

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, completekey='tab', stdin = None, stdout = None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        self.modules = []

        self.pp = pprint.PrettyPrinter(indent=2, width=80)
        self.config = Config(ROOT_DIR, "/config/config.json")
        self.state = State()
        self.loader = Loader(self.config)
        if self.config.get('config').get('modules').get('auto_load'):
            self.modules = self.loader.loadModules()

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_exit(self, arg):
        'Exit FuzzLabs.'
        sys.exit(0)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_quit(self, arg):
        'Exit FuzzLabs.'
        sys.exit(0)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_use(self, args):
        'Set the active job.'
        argsp = args.split(" ")
        if argsp[0] == "job":
            name = str("".join(argsp[1:]))
            if len(name) == 0:
                print "[e] invalid job name specified"
                return
            if name not in list(self.state.jobs):
                print "[e] job '%s' does not exist" % str(name)
                return
            self.state.active = str(name)
            CliJob(self.config, self.state.jobs[self.state.active]).cmdloop()
        else:
            print "[e] type '%s' not supported" % str(argsp[0])
            return

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_use(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_new(self, args):
        'Add a new job'
        argsp = args.split(" ")
        if argsp[0] == "job":
            name = str("".join(argsp[1:]))
            if len(name) == 0:
                print "[e] invalid job name specified"
                return
            self.state.jobs[name] = Job(name)
        else:
            print "[e] type '%s' not supported" % str(argsp[0])
            self.help_new()
            return

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_new(self):
        print "\nThe new command can be used to create new items such as jobs and grammars.\n\n" +\
              "Syntax: new [ job <name> | grammar <name> ]\n\n" +\
              "job:     create a new job identified by <name>\n" +\
              "grammar: create a new grammar identified by <name>\n"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_modules(self, args):
        'Manage framework modules.'
        argsp = args.split(" ")
        if argsp[0] == "load":
            rc = self.loader.loadModule(argsp[1])
        elif argsp[0] == "unload":
            rc = self.loader.unloadModule(argsp[1])
            if not rc:
                print "[e] failed to unload module '%s'" %\
                      (argsp[1])
        elif argsp[0] == "reload":
            rc = self.loader.unloadModule(argsp[1])
            if rc: rc = self.loader.loadModule(argsp[1])
            if not rc:
                print "[e] failed to reload module '%s'" %\
                      (argsp[1])
        elif argsp[0] == "list":
            print
            for m in self.loader.getModules():
                print m
            print
        else:
            print "[e] unsupported operation '%s'" % str(argsp[0])
            self.help_modules()
            return

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_modules(self):
        print "\nThe modules command can be used to manage framework modules.\n\n" +\
              "Syntax: modules [ list | load <name> | unload <name> | reload <name> ]\n\n" +\
              "list:    lists all available modules\n" +\
              "         To see the loaded modules use: show modules\n" +\
              "load:    load module specified by <name>\n" +\
              "unload:  unload module specified by <name>\n" +\
              "reload:  reload module specified by <name>\n"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_show(self, args):
        'List or inspect items.'

        argsp = args.split(" ")
        if argsp[0] == "jobs":
            print
            print "%-35s\t%-40s" % ("Name", "UUID")
            print "-" * 80
            for k, v in self.state.jobs.iteritems():
                print "%-35s\t%-40s" % (k[:30], self.state.jobs[k].id)
            print
        elif argsp[0] == "job":
            name = str("".join(argsp[1:]))
            if len(name) == 0 and not self.state.active:
                print "[e] invalid job name specified"
                return
            elif len(name) == 0 and self.state.active:
                job = self.state.jobs.get(self.state.active)
                self.pp.pprint(job)
            else:
                job = self.state.jobs.get(name)
                if job:
                    self.pp.pprint(job)
                else:
                    print "[e] job does not exist"
        elif argsp[0] == "modules":
            print
            print "%-15s\t%-6s\t%s" % ("Name", "Status", "Description")
            print "-" * 80
            for module in self.modules:
                state = "loaded"
                if self.modules[module].service:
                    state = "active"
                print "%-15s\t%-6s\t%s" % (module, state, self.modules[module].desc)
            print
        else:
            print "[e] type '%s' not supported" % str(argsp[0])
            self.help_show()
            return

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_shell(self, args):
        'Execute operating system command.'
        os.system(args)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_show(self):
        print "\nThe show command can be used to list or inspect elements.\n\n" +\
              "Syntax: show [ jobs | jobs <name> | modules ]\n\n" +\
              "jobs:    lists all registered jobs\n" +\
              "job:     prints properties of job identified by <name>\n" +\
              "modules: list loaded modules\n"

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    Cli().cmdloop()

