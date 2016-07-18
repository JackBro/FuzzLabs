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

class CliConfigEngine(cmd.Cmd):
    ruler = '-'
    prompt = 'fuzzlabs(engines) > '

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, config, completekey='tab', stdin = None, stdout = None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        self.config = config
        self.pp     = pprint.PrettyPrinter(indent=2, width=80)

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

    def engine_request(self, address, port, robject):
        res = None
        headers = {}
        if robject.get('method') in ["PUT", "POST"]:
            headers = {
                "Content-Type": "application/json"
            }

        conn = httplib.HTTPConnection(address, port, True, 5)
        try:
            conn.request(robject.get('method'),
                         robject.get('uri'),
                         robject.get('data'),
                         headers)
            res = conn.getresponse()
        except Exception, ex:
            print "[e] failed to contact engine at %s:%d: %s" %\
                  (address, port, str(ex))
            return False
        callback = robject.get('callback')
        data = json.loads(res.read())
        if callback: callback(res.status, res.reason, data,
                              {"address": address, "port": port})
        return {
            "status": res.status,
            "data": data
        }

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def callback_acl_init(self, status, reason, data, engine):
        if (status != 200):
            print "[e] failed to add engine: %s" % data.get('message')

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def callback_get_api_key(self, status, reason, data, engine):
        if (status != 200):
            print "[e] failed to add engine: %s" % data.get('message')
        else:
            apikey = data.get('apikey')
            if not apikey:
                print "[e] failed to add engine: %s" %\
                      "no API key in response"
                return

            if not self.config.get('data').get('engines'):
                self.config.get('data')['engines'] = {}
            id = Utils.generate_name()
            self.config.get('data').get('engines')[id] = {
                "address": engine.get('address'),
                "port": engine.get('port'),
                "apikey": apikey
            }
            self.config.save()

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_add(self, args):
        initialization = [
            {"method": "GET", "uri": "/setup/acl",
             "callback": self.callback_acl_init},
            {"method": "GET", "uri": "/setup/apikey",
             "callback": self.callback_get_api_key}
        ]

        args = args.split(" ")
        if len(args) < 1:
            print "[e] invalid syntax"
            return
        address = args[0]
        port = 26000
        if len(args) == 2:
            try:
                port = int(args[1])
            except:
                print "[e] invalid port number"
                return

        for robject in initialization:
            rc = self.engine_request(address, port, robject).get('status')
            if rc != 200: break

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_add(self):
        print "\nThe add command can be used to add a new engine.\n\n" +\
              "Syntax: add <address> [ port ]\n\n" +\
              "address: the IP address of the engine\n" +\
              "port:    the port number the engine is listening on (default: 26000)\n\n" +\
              "For the command to be successful The engine has to be running at\n" +\
              "the time of issuing the command. The engine has to run with a stock\n" +\
              "configuration as adding the engine involves automatic, initial\n" +\
              "engine configuration.\n"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_list(self, args):
        'List registered engines.'
        engines = self.config.get('data').get('engines')
        if not engines or len(list(engines)) == 0:
            print "[i] no engines registered"
            return

        print
        for engine in engines:
            status = "unknown"
            engine_data = self.config.get('data').get('engines')[engine]

            rc = self.engine_request(engine_data['address'],
                                     engine_data['port'], 
            {
                "method": "GET",
                "uri": "/management/ping?apikey=" + engine_data['apikey'],
                "data": None
            })
            if rc:
                if rc.get('status') == 200 and \
                   rc.get('data').get('message') == "pong":
                    status = "active"

            print "id: " + engine
            print "  %-10s: %-40s" % ("Address", engine_data['address'])
            print "  %-10s: %-40s" % ("Port", str(engine_data['port']))
            print "  %-10s: %-40s" % ("Api key", str(engine_data['apikey']))
            print "  %-10s: %-40s" % ("Status", status)
            print

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_shutdown(self, args):
        engines = self.config.get('data').get('engines')
        if not engines or len(list(engines)) == 0:
            print "[i] no engines registered"
            return
        engine = engines.get(args)
        if not engine:
            print "[i] no engine registered with id '%s'" % args
            return

        rc = self.engine_request(engine['address'],
                                 engine['port'],
        {
            "method": "GET",
            "uri": "/management/shutdown?apikey=" + engine['apikey'],
            "data": None
        })
        if rc:
            if rc.get('status') == 200:
                print "[i] engine shut down"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_shutdown(self):
        print "\nThe shutdown command can be used to shut down the engine.\n\n" +\
              "Syntax: shutdown <engine id>\n"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_remove(self, args):
        args = args.split(" ")
        if len(args) != 2:
            print "[e] syntax error"
            return
        engines = self.config.get('data').get('engines')
        if not engines or len(list(engines)) == 0:
            print "[i] no engines registered"
            return
        engine = engines.get(args[1])
        if not engine:
            print "[i] no engine registered with id '%s'" % args[1]
            return

        uri = None
        if args[0] == "abandon":
            uri = "/management/remove?apikey=" + engine['apikey']
        elif args[0] == "terminate":
            uri = "/management/remove?terminate=true&apikey=" + engine['apikey']
        else:
            print "[e] invalid option '%s'" % args[0]
            return

        rc = self.engine_request(engine['address'],
                                 engine['port'],
        {
            "method": "GET",
            "uri": uri,
            "data": None
        })
        if rc:
            if rc.get('status') == 200:
                self.config.get('data').get('engines').pop(args[1])
                self.config.save()
                print "[i] engine removed"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_remove(self):
        print "\nUnregisters the engine.\n\n" +\
              "Syntax: remove [ abandon | terminate ] <engine id>\n\n" +\
              "abandon:   zeroes out the API key and ACL of the engine configuration,\n" +\
              "           removes the engine from the client database, but leaves\n" +\
              "           the engine running. In this state, other clients can take\n" +\
              "           over the engine.\n" +\
              "terminate: same as abandon, but instead of leaving the engine running\n" +\
              "           it will be completely shut down.\n"

