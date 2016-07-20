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

class ResourceSetupSsl(Resource):

    def __init__(self, **kwargs):
        self.root   = kwargs.get('root')
        self.config = kwargs

    def check_access(self):
        client = request.remote_addr
        args   = parser.parse_args(strict=True)
        allow  = self.config.get('data').get('security').get('allow')
        apikey = self.config.get('data').get('security').get('apikey')

        if not allow or len(allow) == 0 or client not in allow:
            abort(403, message="access denied")

        if not args.get('apikey') or args.get('apikey') != apikey:
            abort(401, message="access denied")

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

        print client
        print cert
        print key
        return {"message": "success"}, 200

