#!/usr/bin/env python

import json
import uuid
import importlib

# =============================================================================
#
# =============================================================================

class Utils:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def read_file(filename):
        data = None
        try:
            with open(filename, 'r') as f:
                data = f.read()
        except Exception, ex:
            raise Exception("failed to load packet grammar (%s)" % str(ex))
        return data

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def read_json(filename):
        data = Utils.read_file(filename)
        return Utils.from_json(data)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def read_grammar(filename):
        return Utils.read_json(filename)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def from_json(data):
        try:
            data = json.loads(data)
        except Exception, ex:
            raise Exception("failed to parse packet grammar (%s)" % str(ex))
        return data

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def bin_to_dec(binary):
        '''
        Convert a binary string to a decimal number.
        @type  binary: String
        @param binary: Binary string
        @rtype:  Integer
        @return: Converted bit string
        '''

        return int(binary, 2)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def generate_name():
        return str(uuid.uuid4())

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def integer_boundaries(library, max_num, integer):
        '''
        Add the supplied integer and border cases to the integer fuzz
        heuristics library.
        @type  integer: Int
        @param integer: Integer to append to fuzz heuristics
        '''
        ilist = []
        for i in xrange(-10, 10):
            case = integer + i
            if 0 > case or case > max_num: continue
            if case in library: continue
            ilist.append(case)
        return ilist

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def format_binary_numeric(value, width, endian = "big"):
        hex_str = hex(value)[2:]
        padded  = ("0" + hex_str) if len(hex_str) % 2 else hex_str
        str_list = []
        for c in range(0, len(padded) / 2):
            str_list.append(int(padded[c:c + 2], 16))
        str_list = list(reversed(str_list))
        str_list += ([0] * (width - len(str_list)))
        if endian == "big": str_list = list(reversed(str_list))
        return "".join(map(chr, str_list))

