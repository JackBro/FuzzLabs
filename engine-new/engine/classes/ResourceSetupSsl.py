import base64
from flask import Flask
from flask import request
from flask_restful import reqparse, abort, Resource
from classes.Utils import Utils

parser = reqparse.RequestParser()
parser.add_argument('apikey', type=str, location='args')
parser.add_argument("client", type=str, help="client certificate")
parser.add_argument("cert", type=str, help="engine certificate")
parser.add_argument("key", type=str, help="engine certificate key")

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class ResourceSetupSsl(Resource):

    def __init__(self, **kwargs):
        self.root   = kwargs.get('root')
        self.config = kwargs

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def check_access(self):
        client = request.remote_addr
        args   = parser.parse_args(strict=True)
        allow  = self.config.get('data').get('security').get('allow')
        apikey = self.config.get('data').get('security').get('apikey')

        allow = self.config.get('data')['security'].get('allow')
        if not allow:
            abort(500, message="invalid configuration")
        allowed = False
        if allow:
            allowed = False
            for c in allow:
                if c.get('address') and c.get('address') == request.remote_addr:
                    allowed = True
        if not allowed:
            abort(403, message="access blocked due to ACL")

        if not args.get('apikey') or args.get('apikey') != apikey:
            abort(401, message="access denied")

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def write_cert(self, fpath, data):
        try:
            open(fpath, 'w').write(data)
        except Exception, ex:
            print "[e] failed to save certificate: %s" % str(ex)
            return False
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def save_certificate(self, client, ctype, data):
        cert_root = self.root + "/config/certificates/"
        fpath = None
        if ctype == "client": 
            fpath = cert_root + client + ".crt"
        elif ctype == "cert":
            fpath = cert_root + "engine.crt"
        elif ctype == "key":
            fpath = cert_root + "engine.key"
        else:
            return False

        if not self.write_cert(fpath, data): return False
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def post(self):
        self.check_access()

        client = None
        cert   = None
        key    = None

        args = parser.parse_args(strict=True)
        if not args.get('cert') or not args.get('key') or\
           not args.get('client'):
            abort(400, message="invalid payload")

        try:
            client = base64.b64decode(args.get('client'))
            cert   = base64.b64decode(args.get('cert'))
            key    = base64.b64decode(args.get('key'))
        except Exception, ex:
            abort(400, message="failed to decode payload: " % str(ex))

        rc = []
        try:
            rc.append(self.save_certificate(request.remote_addr, "client", client))
            rc.append(self.save_certificate(request.remote_addr, "cert", cert))
            rc.append(self.save_certificate(request.remote_addr, "key", key))
        except Exception, ex:
            abort(400, message="failed to set up certificates: " % str(ex))

        if False in rc:
            abort(400, message="failed to set up certificates")

        cert_root = self.root + "/config/certificates/"
        self.config.get('data').get('security')['ssl'] = {}
        self.config.get('data').get('security').get('ssl')['enabled'] = 1
        self.config.get('data').get('security').get('ssl')['certificate'] = cert_root + "engine.crt"
        self.config.get('data').get('security').get('ssl')['key'] = cert_root + "engine.key"
        for acle in self.config.get('data').get('security').get('allow'):
            if acle.get('address') and acle.get('address') == request.remote_addr:
                acle['certificate'] = cert_root + request.remote_addr + ".crt"

        Utils.save_file(self.root + "/config/config.json",
                        self.config.get('data'))

        open("/tmp/.flenginerestart", "w").write("restart")
        func = request.environ.get('werkzeug.server.shutdown')
        func()

        return {"message": "success"}, 200

