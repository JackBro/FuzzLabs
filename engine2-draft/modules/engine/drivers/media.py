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

    def __init__(self, bind=None, timeout=5.0, protos = []):
        self.bind = None
        if bind:
            self.bind = (bind.get('address'), bind.get('port'))
        self.timeout = timeout
        self.proto = None
        self.protos = protos
        self.socket = None
        self.target = None

    # -------------------------------------------------------------------------
    # The media_socket function should return the socket associated with the 
    # media.
    # -------------------------------------------------------------------------

    def media_socket(self):
        return self.socket

    # -------------------------------------------------------------------------
    # The media_target function accepts a target defined by the following 
    # structure:
    #
    #     {"property-1": "<value-1>", "property-2", <value-2>}
    #
    # If no target is given, it returns the current target set.
    # -------------------------------------------------------------------------

    def media_target(self, target=None):
        if target == None:
            return self.target
        else:
            self.target = target

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

    @abc.abstractmethod
    def send(self, data):
        """ send data to target """

    # -------------------------------------------------------------------------
    # This function implements the receiving of data from the target. 
    # -------------------------------------------------------------------------

    def recv(self, size):
        return self.socket.recv(size)

    # -------------------------------------------------------------------------
    # This function returns the list of protocols supported by the transport 
    # media.
    # -------------------------------------------------------------------------

    def media_protocols(self):
        return self.protos

    # -------------------------------------------------------------------------
    # The media_protocol function accepts a the name of the protocol to be
    # used. If no protocol is given, it returns the current protocol set.
    # -------------------------------------------------------------------------

    def media_protocol(self, proto=None):
        if proto == None:
            return self.proto
        else:
            self.proto = proto


