from flask import Flask
from flask import request
from flask_restful import reqparse, abort, Resource
from classes.Utils import Utils

parser = reqparse.RequestParser()
parser.add_argument('apikey', type=str, location='args')

class ResourceShutdown(Resource):

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

    def get(self):
        self.check_access()

        func = request.environ.get('werkzeug.server.shutdown')
        func()

        return {"message": "bye"}, 200

