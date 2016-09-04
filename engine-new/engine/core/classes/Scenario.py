import os
import time
import inspect
import threading
from classes.Utils import Utils
from classes.Config import Config
from logic.Linear import Linear
from primitives.block import block

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Scenario(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, scenario_id, worker_id, job, logger, config, scenario):
        self.id         = worker_id
        self.sleep_time = 0
        self.completed  = False
        self.job        = job
        self.logger     = logger
        self.config     = config
        self.name       = scenario.get('name')
        if not self.name:
            self.name   = str(scenario_id)
        self.units      = []

        if self.job.get('session').get('sleep_time'):
            self.sleep_time = self.job.get('session').get('sleep_time')

        if not scenario.get('units'):
            self.logger.log("no unit specified for scenario", "warning",
                            str(ex),
                            self.id,
                            self.job.get('id'),
                            self.name)

        for unit in scenario.get('units'):
            self.units.append(self.load_unit(unit))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def load_unit(self, unit):
        u_path = self.config.get('root') + "/../units/" + unit + ".json"
        try:
            data = Utils.read_json(u_path)
            if not data.get('properties'):
                data['properties'] = {}
            if data.get('properties').get('name'):
                data['properties']['name'] = unit
            return block(data)
        except Exception, ex:
            msg = self.logger.log("failed to load unit", "error",
                            str(ex),
                            self.id,
                            self.job.get('id'),
                            self.name,
                            unit)
            raise Exception(msg)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def status(self, unit, ident = 0):
        for item in unit:
            primitives = item.get('primitives')
            if not primitives:
                print "%s%s: %d/%d" % ("    "*ident, item.name, item.total_mutations, item.mutation_index)
            else: 
                print "%s%s: %d/%d" % ("    "*ident, item.name, item.total_mutations, item.mutation_index)
                self.status(item, ident + 1)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        for unit in self.units:
            self.logger.log("executing", "info",
                            "",
                            self.id,
                            self.job.get('id'),
                            self.name,
                            unit.name)

            while not unit.completed:
                try:
                    unit.mutate()
                except Exception, ex:
                    msg = self.logger.log("failed to mutate unit", "error",
                                    str(ex),
                                    self.id,
                                    self.job.get('id'),
                                    self.name,
                                    unit.name)
                    raise Exception(msg)

                # TODO: connect
                for r_unit in self.units:
                    data = None
                    try:
                        print "-"*80        # TODO: remove
                        self.status(r_unit) # TODO: remove
                        data = r_unit.render()
                    except Exception, ex:
                        msg = self.logger.log("failed to render unit", "error",
                                        str(ex),
                                        self.id,
                                        self.job.get('id'),
                                        self.name,
                                        unit.name)
                        raise Exception(msg)

                    # TODO: send(data)
                    # TODO: recv
                    time.sleep(self.sleep_time)
                # TODO: disconnect

            self.logger.log("finished", "info",
                            "",
                            self.id,
                            self.job.get('id'),
                            self.name,
                            unit.name)
        self.completed = True

