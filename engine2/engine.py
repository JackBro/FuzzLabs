#!/usr/bin/env python

import json
import inspect
import importlib
from utils import utils

# =============================================================================
#
# =============================================================================

def read_packet_grammar(filename):
    data = utils.read_file(filename)
    return utils.from_json(data)

# =============================================================================
#
# =============================================================================

def init_root(grammar):
    root = None
    try:
        root = getattr(importlib.import_module("primitives.block"), "block")(grammar)
    except Exception, ex:
        print "failed to instantiate root block (%s)" % str(ex)
    return root

# =============================================================================
#
# =============================================================================

if __name__ == "__main__":
    g = read_packet_grammar("./packet.json")
    root = init_root(g)

    if root == None:
        raise Exception("failed to initialize root block")

    for item in root:
        item.mutate()
        print item.render()

