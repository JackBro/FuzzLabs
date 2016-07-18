from driver import driver

import os
import abc
import sys
import select

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class file(driver):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, bind=None, timeout=0):
        media.__init__(self, bind, timeout, ["file"])

        self.session_counter = 0
        self.f_path = None
        self.f_name = None
        self.f_ext = None
        self.p_sub = None

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def connect(self):
        self.f_path = self.target['path']
        self.f_name = self.target['filename']
        self.f_ext = self.target['extension']
        if not os.path.exists(self.f_path): os.makedirs(self.f_path)
        subdir = self.f_path + "/" + str(self.session_counter / 1000)
        if subdir != self.p_sub:
            self.p_sub = subdir
            if not os.path.exists(subdir): os.makedirs(subdir)

        try:
            f_full = self.p_sub + "/" + self.f_name + "." + \
                     str(self.session_counter) + \
                     "." + self.f_ext

            self.socket = open(f_full, 'w')
        except Exception, ex:
            raise ex

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def send(self, data):
        try:
            self.socket.write(data)
            self.session_counter += 1
        except Exception, ex:
            raise ex

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def disconnect(self):
        try:
            self.socket.close()
        except Exception, ex:
            pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def recv(self, size):
        return("OK")

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def media_socket(self):
        return self.socket

