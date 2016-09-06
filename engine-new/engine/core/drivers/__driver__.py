import os
import abc
import sys
import json
import time
import socket
import select

# =============================================================================
# DRIVER SKELETON
# =============================================================================

# -----------------------------------------------------------------------------
# A driver class is an interface for the fuzzer, basically the sulley core, to 
# send and receive data. The media class implements a skeleton which can be 
# extended by other drivers.
# -----------------------------------------------------------------------------

class driver:
    __metaclass__  = abc.ABCMeta

    # -------------------------------------------------------------------------
    # Standard constructor/initialization
    # -------------------------------------------------------------------------

    def __init__(self, driver_config = None):
        self.driver_config = driver_config
        self.socket = None

    # -------------------------------------------------------------------------
    # The media_socket function should return the socket associated with the 
    # media.
    # -------------------------------------------------------------------------

    def media_socket(self):
        return self.socket

    # -------------------------------------------------------------------------
    # This function is responsible of building up a connection to the target
    # set via the media_target function.
    # As each transport media might require a completely different way to build
    # up a connection, this function is empty and each transport media handler
    # should override it to implement the necessary functionality.
    # -------------------------------------------------------------------------

    def connect(self):
        pass

    # -------------------------------------------------------------------------
    # This function disconnects from the target by closing the socket.
    # -------------------------------------------------------------------------

    def disconnect(self):
        try:
            self.socket.close()
        except Exception, ex:
            pass
        self.socket = None

    # -------------------------------------------------------------------------
    # This function implements the sending of data to the target. 
    # -------------------------------------------------------------------------

    def send(self, data):
        self.socket.send(data)

    # -------------------------------------------------------------------------
    # This function implements the receiving of data from the target. 
    # -------------------------------------------------------------------------

    def receive(self, size = 4096):
        return self.socket.recv(size)

