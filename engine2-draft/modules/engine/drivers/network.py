from driver import driver

import os
import abc
import sys
import json
import time
import socket
import select

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class network(driver):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, bind, timeout):
        media.__init__(self, bind, timeout, ["tcp", "udp"])
        self.target_address = None
        self.target_port = None
        self.connected = False

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def connect(self):
        try:
            if self.proto == "tcp" or self.proto == "ssl":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.proto == "udp":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except Exception, e:
            raise Exception, ["failed to create socket", str(e)]

        if self.bind:
            try:
                self.socket.bind(self.bind)
            except Exception, e:
                raise Exception, ["failed to bind on socket", str(e)]

        try:
            self.target_address = self.target['address']
            self.target_port = int(self.target['port'])
        except Exception, e:
            raise Exception, ["failed to process target details", str(e)]

        try:
            self.socket.settimeout(self.timeout)
            if self.proto == "tcp":
                self.socket.connect((self.target_address, self.target_port))
                self.connected = True
        except Exception, e:
            raise Exception, ["failed to connect to target %s:%d" %
                              (self.target_address, self.target_port),
                             str(e)]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def disconnect(self):
        try:
            self.socket.shutdown(2)
        except Exception, ex:
            raise Exception(ex)

        try:
            self.socket.close()
        except Exception, ex:
            pass
        self.socket = None


    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def send(self, data):
        if self.proto == "tcp":
            try:
                self.socket.send(data)
            except Exception, e:
                raise Exception, ["failed to send data", str(e)]
        else:
            # max UDP packet size.
            # TODO: anyone know how to determine this value smarter?
            MAX_UDP = 65507

            if os.name != "nt" and os.uname()[0] == "Darwin":
                MAX_UDP = 9216

            if len(data) > MAX_UDP:
                data = data[:MAX_UDP]

            try:
                self.socket.sendto(data, (self.target_address,
                                   self.target_port))
            except Exception, e:
                raise Exception, ["failed to send data", str(e)]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def disconnect(self):
        try:
            self.socket.shutdown(2)
        except Exception, ex:
            raise Exception(ex)

        try:
            self.socket.close()
        except Exception, ex:
            pass
        self.socket = None


    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def send(self, data):
        try:
            self.socket.send(data)
        except Exception, e:
            raise Exception, ["failed to send data", str(e)]

