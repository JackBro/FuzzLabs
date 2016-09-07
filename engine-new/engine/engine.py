#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
from OpenSSL import SSL
from flask import Flask
from flask_restful import Api
from classes.Utils import Utils
from classes.Config import Config
from classes.ResourceInitAcl import ResourceInitAcl
from classes.ResourceInitAPIKey import ResourceInitAPIKey
from classes.ResourceSetupSsl import ResourceSetupSsl
from classes.ResourcePing import ResourcePing
from classes.ResourceShutdown import ResourceShutdown
from classes.ResourceRemove import ResourceRemove
from classes.ResourceAclList import ResourceAclList
from classes.ResourceAclAdd import ResourceAclAdd
from classes.ResourceAclRemove import ResourceAclRemove
from classes.ResourceListJobs import ResourceListJobs

ROOT = os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe()
            )))
config = Config(ROOT, "/config/config.json")

app = Flask(__name__)
api = Api(app)

api.add_resource(ResourceInitAcl,
                 '/setup/acl',
                 resource_class_kwargs=config)
api.add_resource(ResourceSetupSsl,
                 '/setup/ssl',
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
api.add_resource(ResourceAclList,
                 '/management/acl/list',
                 resource_class_kwargs=config)
api.add_resource(ResourceAclAdd,
                 '/management/acl/add',
                 resource_class_kwargs=config)
api.add_resource(ResourceAclRemove,
                 '/management/acl/remove',
                 resource_class_kwargs=config)

api.add_resource(ResourceListJobs,
                 '/jobs',
                 resource_class_kwargs=config)

def start_engine():
    context = None
    try:
        os.unlink("/tmp/.flenginerestart")
    except Exception, ex:
        pass

    try:
        if config.get('data').get('security').get('ssl').get('enabled') == 1:
            k = config.get('data').get('security').get('ssl').get('key')
            c = config.get('data').get('security').get('ssl').get('certificate')
            context = (c, k)
    except Exception, ex:
        print "[e] failed to set up SSL context"
        pass

    app.run(host=config.get('data').get('general').get('bind'),
            port=config.get('data').get('general').get('port'),
            debug=False,
            ssl_context=context)

    # Check if we have to restart. This custom restart is needed to
    # switch from HTTP to HTTPS once configured.

    r = None
    restart = False
    try:
        r = Utils.read_file("/tmp/.flenginerestart")
    except Exception, ex:
        pass
    if r and r == "restart": restart = True
    return restart

if __name__ == '__main__':
    rc = start_engine()
    while rc:
        rc = start_engine()

