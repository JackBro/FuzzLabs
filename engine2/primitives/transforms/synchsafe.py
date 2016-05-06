class synchsafe:

    primitive_types = [byte, word, dword, qword]
    value_types     = [int, long]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def transform(integer):
        out = mask = 0x7F
        while (mask ^ 0x7FFFFFFF):
            out = integer & ~mask
            out <<= 1
            out |= integer & mask
            mask = ((mask + 1) << 8) - 1
            integer = out
        return out

