import os
import cmd
import sys
import json
import pprint
import inspect
import httplib

from OpenSSL import crypto, SSL
from socket import gethostname
from time import gmtime, mktime
from os.path import exists, join

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

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def check_local_certificates(self):
        has_certs = True
        if not self.config.get('data').get('security'):
            self.config.get('data')['security'] = {}
            has_certs = False

        if not self.config.get('data').get('security').get('ssl'):
            self.config.get('data').get('security')['ssl'] = {}
            has_certs = False

        if not self.config.get('data').get('security').get('ssl').get('certificate_file'):
            self.config.get('data').get('security').get('ssl')['certificate_file'] = "client.crt"
            has_certs = False

        if not self.config.get('data').get('security').get('ssl').get('key_file'):
            self.config.get('data').get('security').get('ssl')['certificate_file'] = "client.key"
            has_certs = False

        if not self.config.get('root'):
            print "[e] could not determine FuzzLabs client root path, aborting."
            return

        cf = self.config.get('root') + "/config/certificates/" +\
             self.config.get('data').get('security').get('ssl').get('certificate_file')

        kf = self.config.get('root') + "/config/certificates/" +\
             self.config.get('data').get('security').get('ssl').get('key_file')

        self.config.save()

        if not exists(cf) or not exists(kf):
            has_certs = False
        return has_certs

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def create_certificate(self, engine_id, cf, kf):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        c = crypto.X509()
        c.get_subject().C = "UK"
        c.get_subject().ST = "London"
        c.get_subject().L = "London"
        c.get_subject().O = "DCNWS"
        c.get_subject().OU = "DCNWS"
        c.get_subject().CN = engine_id
        c.set_serial_number(1000)
        c.gmtime_adj_notBefore(0)
        c.gmtime_adj_notAfter(10*365*24*60*60)
        c.set_issuer(c.get_subject())
        c.set_pubkey(k)
        c.sign(k, 'sha1')

        try:
            open(cf, 'w').write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, c))
            open(kf, 'w').write(
                crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        except Exception, ex:
            print "[e] failed to create local key file: %s" % str(ex)
            return False

        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def create_local_certificates(self):
        cf = self.config.get('root') + "/config/certificates/" +\
             self.config.get('data').get('security').get('ssl').get('certificate_file')

        kf = self.config.get('root') + "/config/certificates/" +\
             self.config.get('data').get('security').get('ssl').get('key_file')

        eid = self.config.get('data').get('security').get('ssl').get('certificate_file')
        eid = eid.split(".")[0]
        self.create_certificate(eid, cf, kf)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def create_engine_certificates(self, engine_id):
        cert_root = self.config.get('root') + "/config/certificates/"
        cf = cert_root + engine_id + ".crt"
        kf = cert_root + engine_id + ".key"
        if not self.create_certificate(engine_id, cf, kf):
            print "[e] failed to generate certificate for engine '%s'" % engine_id
            return False

        try:
            engine = self.config.get('data').get('engines').get(engine_id)
            self.config.get('data').get('engines').get(engine_id)['ssl'] = 1
            self.config.get('data').get('engines').get(engine_id)['certificate_file'] = cf
        except Exception, ex:
            print "[e] failed to save SSL configuration for engine '%s'" % engine_id
            return False

        self.config.save()
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_ssl(self, args):
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
        if args[0] == "enable":
            # Make sure we got our local cert and key
            if not self.check_local_certificates():
                if not self.create_local_certificates():
                    return

            self.create_engine_certificates(args[1])
            # TODO:
            #  2. Store engine cert locally
            #  3. Register engine cert in local config
            #  4. Transfer engine cert and key to engine
        elif args[0] == "disable":
            # TODO:
            #  1. send ssl disable request to engine
            #  2. if returns 'success', remove engine cert from local config
            #  3. delete local copy of engine cert
            pass
        else:
            print "[e] invalid option '%s'" % args[0]
            return

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def help_ssl(self):
        print "\nEnable or disable SSL for a given engine connection..\n\n" +\
              "Syntax: ssl [ enable | disable ] <engine id>\n"

