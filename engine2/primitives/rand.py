from __primitive import __primitive__
from utils import utils
import random
import struct

all_properties = [
    {
        "name": "value",
        "type": ["int", "long"],
        "mandatory": 1,
        "error": "primitive requires value to be of type long or int"
    },
    {
        "name": "min_length",
        "type": ["int", "long"],
        "default": 1,
        "error": "primitive requires min_length to be of type int or long"
    },
    {
        "name": "max_length",
        "type": ["int", "long"],
        "default": 100,
        "error": "primitive requires max_length to be of type int or long"
    },
    {
        "name": "max_mutations",
        "type": ["int", "long"],
        "default": 100,
        "error": "primitive requires max_mutations to be of type int or long"
    },
    {
        "name": "min_value",
        "type": ["int", "long"],
        "default": 0,
        "error": "primitive requires min_value to be of type int or long"
    },
    {
        "name": "max_value",
        "type": ["int", "long"],
        "default": 255,
        "error": "primitive requires max_value to be of type int or long"
    },
    {
        "name": "format",
        "type": "str",
        "values": ["binary", "ascii"],
        "default": "binary",
        "error": "primitive requires format to be of type str"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [1],
        "default": 1,
        "error": "primitive requires fuzzable to be True (1)"
    },
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    },
    {
        "name": "ignore",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "value": 1,
        "error": "primitive is either ignored (1) or not (0)"
    }
]


# =============================================================================
#
# =============================================================================

class rand(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        if self.mutation_index >= self.max_mutations:
            self.complete = True
            if not self.ignore: return

        x = []
        times = random.randint(self.min_length, self.max_length)
        for c in range(0, times):
            x.append(struct.pack("B", random.randint(self.min_value, self.max_value)))
        self.value = ''.join(x)
        self.mutation_index += 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        self.mutate()
        return str(self.value)

