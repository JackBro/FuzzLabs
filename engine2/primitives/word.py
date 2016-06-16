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
        "name": "max_num",
        "type": ["int", "long"],
        "default": 0,
        "error": "primitive requires max_num to be of type int"
    },
    {
        "name": "endian",
        "type": "str",
        "values": ["big", "little"],
        "default": "little",
        "error": "primitive requires endian to be of type str ('big' or 'little')"
    },
    {
        "name": "format",
        "type": "str",
        "values": ["binary", "ascii"],
        "default": "binary",
        "error": "primitive requires format to be of type str"
    },
    {
        "name": "signed",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires signed to be of type bool (1 or 0)"
    },
    {
        "name": "full_range",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires full_range to be of type bool (1 or 0)"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
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

class word(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, transforms):
        global all_properties
        self.type = self.__class__.__name__
        __primitive__.__init__(self, properties, all_properties, transforms)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        max = utils.bin_to_dec("1" + "0" * 16) # 16 bits
        if self.signed:
	    max = utils.bin_to_dec("1" + "0" * 16) / 2 - 1

        if self.max_num and self.max_num > max:
            raise Exception("%s primitive maximum value is %d" % (self.type, max))
        if self.max_num == None or self.max_num == 0:
            self.max_num = max

        if self.full_range:
            for i in xrange(0, self.max_num):
                if i not in self.library: self.library.append(i)
        else:
            self.library += utils.integer_boundaries(
                self.library, 
                self.max_num, 
                0)
            self.library += utils.integer_boundaries(
                self.library,
                self.max_num,
                self.max_num)
            for v in [2, 3, 4, 8, 16, 32]:
                self.library += utils.integer_boundaries(
                    self.library,
                    self.max_num,
                    self.max_num / v)

        negatives = []
        if self.signed:
            for v in self.library:
                negatives.append(-v)
        self.library += negatives

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        if self.format == "binary":
            try:
                if self.signed:
                    return struct.pack("h", self.value)
                else:
                    return struct.pack("H", self.value)
            except Exception, ex:
                raise Exception(str(ex) + " - value: %d" % self.value)
        return str(self.value)

