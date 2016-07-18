from driver import driver

import os
import abc
import sys

from bluetooth import *

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class bluetooth(driver):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, bind=None, timeout=5.0):
        media.__init__(self, bind, timeout, ["l2cap", "rfcomm"])

        self.target_bdaddr = None
        self.target_channel = None

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def connect(self):
        self.socket = None
        try:
            if self.proto == "rfcomm":
                self.socket = BluetoothSocket(RFCOMM)
            elif self.proto == "l2cap":
                self.socket = BluetoothSocket(L2CAP)
        except Exception, e:
            raise Exception, ["failed to create socket", str(e)]

        try:
            self.target_bdaddr = self.target['bdaddr']
            self.target_channel = self.target['channel']
        except Exception, e:
            raise Exception, ["failed to process target details", str(e)]

        self.socket.settimeout(self.timeout)
        try:
            self.socket.connect((self.target_bdaddr, int(self.target_channel)))
        except Exception as e:
            # File descriptor in bad state has code 77
            # Still, connection works. Fix this later properly.
            if str(e)[1:3] != "77":
                raise Exception, ["failed to connect to target", str(e)]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def send(self, data):
        if (self.socket == None):
            self.connect()

        try:
            self.socket.send(data)
        except Exception, e:
            raise Exception, ["failed to send data", str(e)]

