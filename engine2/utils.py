#!/usr/bin/env python

import json
import importlib

# =============================================================================
#
# =============================================================================

class utils:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def read_file(filename):
        data = None
        try:
            with open(filename, 'r') as f:
                data = f.read()
        except Exception, ex:
            raise Exception("failed to load packet grammar (%s)" % str(ex))
        return data

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def from_json(data):
        try:
            data = json.loads(data)
        except Exception, ex:
            raise Exception("failed to parse packet grammar (%s)" % str(ex))
        return data

