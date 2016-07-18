"""
Manage the configuration file of FuzzLabs.
"""

import os.path
import json
import fcntl

class ConfigurationHandler:
    """
    Manage the configuration data stored in JSON format. The configuration is
    read from the JSON file, parsed and stored in a variable. The configuration
    can be retrieved using the get() method.
    """

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, c_path = None):
        """ 
        Initialize variables and reload (load) configuration.

        @type  c_path:   String
        @param c_path:   The path to the configuration file
        """

        self.config = None
        self.file = c_path
        self.__loadConfiguration()

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __loadConfiguration(self):
        """
        Open the configuration file and read, then parse its content.
        """

        if not os.path.isfile(self.file) or not os.access(self.file, os.R_OK):
            raise Exception("cannot access configuration file")

        try:
            file_desc = open(self.file, "r")
            fcntl.flock(file_desc, fcntl.LOCK_EX)
            self.config = json.loads(file_desc.read())
            fcntl.flock(file_desc, fcntl.LOCK_UN)
            file_desc.close()
        except Exception, ex:
            raise Exception("failed to load configuration: " + str(ex))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def get(self):
        """
        Return the parsed configuration data.

        @rtype:          Dictionary
        @return:         The complete configuration as a dictionary.
        """

        return self.config

