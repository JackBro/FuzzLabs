from __primitive import __primitive__

all_properties = [
    {
        "name": "value",
        "type": ["int", "long"],
        "mandatory": 1,
        "error": "primitive requires value to be of type long or int"
    },
    {
        "name": "endian",
        "type": "str",
        "values": ["big", "little"],
        "default": "little",
        "error": "primitive requires value to be of type str ('big' or 'little')"
    },
    {
        "name": "format",
        "type": "str",
        "values": ["binary", "ascii"],
        "default": "binary",
        "error": "primitive requires value to be of type str"
    },
    {
        "name": "signed",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires value to be of type bool (1 or 0)"
    },
    {
        "name": "full_range",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires value to be of type bool (1 or 0)"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires value to be of type bool (1 or 0)"
    },
    {
        "name": "synchsafe",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires value to be of type bool (1 or 0)"
    },
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires value to be of type str"
    }
]

# =============================================================================
#
# =============================================================================

class byte(__primitive__):

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

    def mutate(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        return 'byte'

