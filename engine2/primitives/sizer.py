import struct
from primitives.__primitive import __primitive__

all_properties = [
    {
        "name": "size",
        "type": ["int", "long"],
        "values": [1, 4, 8],
        "default": 4,
        "error": "primitive requires size to be of type int or long"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    },
    {
        "name": "inclusive",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires inclusive to be of type bool (1 or 0)"
    },
    {
        "name": "offset",
        "type": ["int", "long"],
        "default": 0,
        "value": 0,
        "mandatory": 0,
        "error": "primitive requires offset to be of type type int or long"
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
        "name": "block",
        "type": "str",
        "mandatory": 0,
        "error": "primitive requires block name to be of type str"
    },
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    }
]

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class sizer(__primitive__):

    """
     NOTE: Sizer always has to be outside of the target block.
    """

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        bitw = self.get('size') * 8
        max = utils.bin_to_dec("1" + "0" * bitw)
        if self.signed:
            max = utils.bin_to_dec("1" + "0" * bitw) / 2 - 1

        if self.max_num and self.max_num > max:
            raise Exception("%s primitive maximum value is %d" % (self.type, max))
        if self.max_num == None or self.max_num == 0:
            self.max_num = max

        if self.full_range:
            for i in xrange(0, self.max_num + 1):
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

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        b = self.search(self.block)
        length = len(b.render())
        if self.get('inclusive'): length += self.get('size')
        if self.get('offset'): length += self.get('offset')

        if self.get('format') == "ascii":
            return str(length)
        else:
            endian = ">"
            if self.get('endian') == "little":
                endian = "<"

            format = "I"
            if self.get('size') == 1:
                format = "B"
            elif self.get('size') == 4:
                format = "I"
            elif self.get('size') == 8:
                format = "Q"

            try:
                return struct.pack(endian + format, length)
            except Exception, ex:
                raise Exception('failed to render sizer %s (%s)' %\
                (self.name,  str(ex)))

