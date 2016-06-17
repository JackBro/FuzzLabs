from __primitive import __primitive__
from utils import utils
import struct
import random

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
        "default": 0,
        "error": "primitive requires min_length to be of type int or long"
    },
    {
        "name": "max_length",
        "type": ["int", "long"],
        "default": 0,
        "error": "primitive requires max_length to be of type int or long"
    },
    {
        "name": "max_mutations",
        "type": ["int", "long"],
        "default": 1000,
        "error": "primitive requires max_mutations to be of type int or long"
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
    }
]

# =============================================================================
#
# =============================================================================

class rand(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, transforms):
        global all_properties
        self.type = self.__class__.__name__
        __primitive__.__init__(self, properties, all_properties, transforms)
        self.total_mutations = self.max_mutations

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        if self.min_length > self.max_length:
            raise Exception("%s primitive requires min_length to be less " +\
                            "than max_length" % self.type)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        if self.mutation_index >= self.total_mutations:
            self.complete = True
            self.value = self.library[0]
            return

        x = []
        times = random.randint(self.min_length, self.max_length) 
        for c in range(0, times):
            x.append(struct.pack("B", random.randint(0, 255)))
        self.value = ''.join(x)
        self.mutation_index += 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        return str(self.value)

