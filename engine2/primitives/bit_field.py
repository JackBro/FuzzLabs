from __primitive import __primitive__

# =============================================================================
#
# =============================================================================

all_properties = [
    {
        "name": "value",
        "type": ["int", "long"],
        "mandatory": 1,
        "error": "primitive requires value to be of type long or int"
    },
    {
        "name": "width",
        "type": "int",
        "mandatory": 1,
        "error": "primitive requires value to be of type int"
    },
    {
        "name": "max_num",
        "type": "int",
        "default": 0,
        "error": "primitive requires value to be of type int"
    },
    {
        "name": "endian",
        "type": ["str"],
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

class bit_field(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__ (self, properties, transforms):
        global all_properties
        self.type = self.__class__.__name__
        __primitive__.__init__(self, properties, all_properties, transforms)

        # TODO: check and refactor the below

        """
        if type(self.value) in [int, long]:
            if synchsafe: self.value = self.t_synchsafe(self.value)
        self.value         = self.original_value = self.value
        """

        # TODO: review the below

        if self.max_num == None:
            self.max_num = self.to_decimal("1" + "0" * width)

        assert(type(self.max_num) is int or type(self.max_num) is long)


        # build the fuzz library.
        if self.full_range:
            # add all possible values.
            for i in xrange(0, self.max_num):
                self.fuzz_library.append(i)
        else:
                # try only "smart" values.
                self.add_integer_boundaries(0)
                self.add_integer_boundaries(self.max_num / 2)
                self.add_integer_boundaries(self.max_num / 3)
                self.add_integer_boundaries(self.max_num / 4)
                self.add_integer_boundaries(self.max_num / 8)
                self.add_integer_boundaries(self.max_num / 16)
                self.add_integer_boundaries(self.max_num / 32)
                self.add_integer_boundaries(self.max_num)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def add_integer_boundaries (self, integer):
        '''
        Add the supplied integer and border cases to the integer fuzz heuristics library.
        @type  integer: Int
        @param integer: Integer to append to fuzz heuristics
        '''

        for i in xrange(-10, 10):
            case = integer + i

            # ensure the border case falls within the valid range for this field.
            if 0 <= case < self.max_num:
                if case not in self.fuzz_library:
                    self.fuzz_library.append(case)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render (self):
        '''
        Render the primitive.
        '''

        if self.format == "binary":
            bit_stream = ""
            rendered   = ""

            # pad the bit stream to the next byte boundary.
            if self.width % 8 == 0:
                bit_stream += self.to_binary()
            else:
                bit_stream  = "0" * (8 - (self.width % 8))
                bit_stream += self.to_binary()

            # convert the bit stream from a string of bits into raw bytes.
            for i in xrange(len(bit_stream) / 8):
                chunk = bit_stream[8*i:8*i+8]
                rendered += struct.pack("B", self.to_decimal(chunk))

            # if necessary, convert the endianess of the raw bytes.
            if self.endian == "<":
                rendered = list(rendered)
                rendered.reverse()
                rendered = "".join(rendered)

            self.rendered = rendered

        #
        # ascii formatting.
        #

        else:
            # if the sign flag is raised and we are dealing with a signed integer (first bit is 1).
            if self.signed and self.to_binary()[0] == "1":

                max_num = self.to_decimal("1" + "0" * (self.width - 1))
                # mask off the sign bit.
                val = self.value & self.to_decimal("1" * (self.width - 1))

                # account for the fact that the negative scale works backwards.
                val = max_num - val - 1

                # toss in the negative sign.
                self.rendered = "%d" % ~val

            # unsigned integer or positive signed integer.
            else:
                self.rendered = "%d" % self.value

        return self.rendered

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def to_binary (self, number=None, bit_count=None):
        '''
        Convert a number to a binary string.
        @type  number:    Integer
        @param number:    (Optional, def=self.value) Number to convert
        @type  bit_count: Integer
        @param bit_count: (Optional, def=self.width) Width of bit string
        @rtype:  String
        @return: Bit string
        '''

        if number == None:
            number = self.value

        if bit_count == None:
            bit_count = self.width

        return "".join(map(lambda x:str((number >> x) & 1), range(bit_count -1, -1, -1)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def to_decimal (self, binary):
        '''
        Convert a binary string to a decimal number.
        @type  binary: String
        @param binary: Binary string
        @rtype:  Integer
        @return: Converted bit string
        '''

        return int(binary, 2)

