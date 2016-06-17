from __primitive import __primitive__
from utils import utils
import struct

all_properties = [
    {
        "name": "value",
        "type": ["int", "long"],
        "mandatory": 1,
        "error": "primitive requires value to be of type long or int"
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

class increment(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, transforms):
        global all_properties
        self.type = self.__class__.__name__
        __primitive__.__init__(self, properties, all_properties, transforms)
        self.total_mutations = 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        self.value += 1
        return str(self.value)

