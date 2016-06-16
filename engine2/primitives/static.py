from __primitive import __primitive__
from utils import utils
import struct

all_properties = [
    {
        "name": "value",
        "type": "str",
        "mandatory": 1,
        "error": "primitive requires value to be of type str"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": 0,
        "default": 0,
        "error": "primitive is non-fuzzable"
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

class static(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, transforms):
        global all_properties
        self.type = self.__class__.__name__
        __primitive__.__init__(self, properties, all_properties, transforms)
        self.library = [self.value]
        self.total_mutations = len(self.library)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        return str(self.value)

