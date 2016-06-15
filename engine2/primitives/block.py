import glob
import importlib
from __primitive import __primitive__

global_primitives = {}
for primitive in glob.glob("primitives/*.py"):
    name = primitive.split(".")[0].split("/")[1]
    if name[:2] != "__":
        global_primitives[name] = importlib.import_module("primitives." + name)

all_properties = []

# =============================================================================
#
# =============================================================================

class block:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, transforms = None):
        global all_properties
        self.type       = self.__class__.__name__
        self.properties = properties
        self.primitives = []
        self.iter_cnt   = 0
        self.complete   = False

        for primitive in self.properties:
            try:
                inst = getattr(global_primitives[primitive.get('primitive')], 
                               primitive['primitive'])
                inst = inst(primitive.get('properties'), primitive.get('transforms'))
                self.primitives.append(inst)
            except Exception, ex:
                raise Exception("failed to instantiate primitive %s (%s)" % \
                      (primitive.get('primitive'), str(ex)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __len__(self):
        return len(self.primitives)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __getitem__(self, c):
        return self.primitives[c]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __iter__(self):
        return self

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def next(self):
        if self.iter_cnt >= len(self.primitives):
            self.iter_cnt = 0
            raise StopIteration
        else:
            self.iter_cnt += 1
            return self.primitives[self.iter_cnt - 1]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        return False

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_render(self, items):
        values = []
        for item in items:
            if item.type == 'block':
                values = values + self.do_render(item)
            else:
                values.append(item.render())
        return values

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        return "".join(self.do_render(self.primitives))

