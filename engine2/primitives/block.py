import glob
import importlib
from logic.Linear import Linear
from primitives.__primitive import __primitive__

all_properties = [
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    },
    {
        "name": "group",
        "type": "str",
        "default": "",
        "mandatory": 0,
        "error": "primitive requires group to be of type str"
    },
    {
        "name": "logic",
        "type": "str",
        "value": "linear",
        "default": "linear",
        "mandatory": 0,
        "error": "primitive requires logic to be of type str"
    },
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    }
]

global_logic = {}
for logic in glob.glob("logic/*.py"):
    name = logic.split(".")[0].split("/")[1]
    lname = name.lower()
    if lname[:2] == "__": continue
    global_logic[lname] = importlib.import_module("logic." + name)

global_transforms = {}
for transform in glob.glob("transforms/*.py"):
    name = transform.split(".")[0].split("/")[1]
    lname = name.lower()
    if lname[:2] == "__": continue
    global_transforms[lname] = importlib.import_module("transforms." + name)

global_primitives = {}
for primitive in glob.glob("primitives/*.py"):
    name = primitive.split(".")[0].split("/")[1]
    if name[:2] == "__": continue
    global_primitives[name] = importlib.import_module("primitives." + name)

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class block(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)
        self.domutate = False

        for primitive in properties.get('primitives'):
            try:
                inst = getattr(global_primitives[primitive.get('primitive')],
                               primitive['primitive'])
                inst = inst(primitive, self)
                self.primitives.append(inst)
            except Exception, ex:
                raise Exception("failed to instantiate primitive %s (%s)" % \
                      (primitive.get('primitive'), str(ex)))

        self.logic = getattr(global_logic[self.logic],
                             self.logic[0].upper() + self.logic[1:])(self)

        value = []
        for p in self.primitives:
            value.append(p.render())
        self.value = value

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        self.domutate = True
        return self.domutate

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        if not self.domutate:
            self.complete = False
            yield "".join(self.value)
        for iteration in self.logic.run():
            yield "".join(iteration)
        self.complete = True

