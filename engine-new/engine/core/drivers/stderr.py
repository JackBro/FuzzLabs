from __driver__ import driver

import sys

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class stderr(driver):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, driver_config):
        driver.__init__(self, driver_config)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def connect(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def send(self, data):
        sys.stderr.write(data + "\n")
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def disconnect(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def receive(self):
        return None

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def media_socket(self):
        return None

