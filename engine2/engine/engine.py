#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
from flask import Flask
from flask_restful import Api
from classes.Config import Config
from classes.ResourceInitAcl import ResourceInitAcl
from classes.ResourceInitAPIKey import ResourceInitAPIKey
from classes.ResourcePing import ResourcePing
from classes.ResourceShutdown import ResourceShutdown
from classes.ResourceRemove import ResourceRemove

ROOT = os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe()
            )))
config = Config(ROOT, "/config/config.json")
config['root'] = ROOT

app = Flask(__name__)
api = Api(app)

api.add_resource(ResourceInitAcl,
                 '/setup/acl',
                 resource_class_kwargs=config)
api.add_resource(ResourceInitAPIKey,
                 '/setup/apikey',
                 resource_class_kwargs=config)
api.add_resource(ResourcePing,
                 '/management/ping',
                 resource_class_kwargs=config)
api.add_resource(ResourceShutdown,
                 '/management/shutdown',
                 resource_class_kwargs=config)
api.add_resource(ResourceRemove,
                 '/management/remove',
                 resource_class_kwargs=config)

if __name__ == '__main__':
    app.run(host=config.get('data').get('general').get('bind'),
            port=config.get('data').get('general').get('port'),
            debug=False)

