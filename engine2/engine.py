#!/usr/bin/env python
from utils import utils
from logic.Linear import Linear
from primitives.block import block

# ----------------------------------------------------------
#
# ----------------------------------------------------------

grammar = utils.read_grammar("./packet.json")
grammar = block(grammar)

for iteration in Linear(grammar).run():
    if iteration:
        print "".join(iteration)

