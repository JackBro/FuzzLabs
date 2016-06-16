# =============================================================================
#
# =============================================================================

class Property(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, prop, prop_value, prop_desc):
        if prop == None:
            raise Exception('incomplete primitive')
        if prop_value == None and prop_desc.get('default'):
            prop_value = value.get('default')
        if prop_value == None:
            raise Exception('could not set value for primitive %s' % prop)
        prop_value = self.convert(prop_desc['type'], prop_value, prop_desc['error'])
        if prop_desc.get('values'):
		    self.check_possible_values(prop_value,
                                       prop_desc['type'],
                                       prop_desc.get('values'))
        self.value = prop_value

        self.total_mutations = None
        self.mutation_index  = None

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def convert(self, ptype, value, error = None):
        if type(ptype) == list: ptype = ptype[0]
        try:
            if ptype == "str":
                return str(value)
            if ptype == "int":
                return int(value)
            if ptype == "bool":
                return bool(value)
            if ptype == "float":
                return float(value)
            if ptype == "long":
                return long(value)
            if ptype == "list":
                return list(value)
        except Exception, ex:
            if error:
                raise Exception(error + " (%s)" % str(ex))
            else:
                raise Exception(ex)
        if error:
            raise Exception(error)
        else:
            raise Exception('invalid property type')

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def check_possible_values(self, value, ptype, values):
        values_list = []
        for v in values:
            values_list.append(self.convert(ptype, v))
        if value not in values_list:
            raise Exception('invalid value for property')

# =============================================================================
#
# =============================================================================

class __primitive__(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, all_properties, transforms = None):
        self.check_properties(all_properties, properties)
        self.transforms     = transforms
        self.rendered       = ""    # rendered value
        self.complete       = False # flag if this primitive has been completely fuzzed
        self.library        = []    # library of fuzz heuristics
        self.mutation_index = 0     # current mutation number

        # Set up properties that were provided in the grammar
        for prop in properties:
            for primitive_prop in all_properties:
                if prop == primitive_prop.get('name'):
                    p = Property(prop, properties[prop], primitive_prop)
                    self[prop] = p.value
                    del p

        # Set up defaults for properties that were not included
        props_provided = self.get_properties(properties)
        for prop in all_properties:
            if prop.get('name') not in props_provided:
                p = Property(prop.get('name'), prop.get('default'), prop)
                self[prop.get('name')] = p.value
                del p

        # First item in library is the original value
        self.library.append(self.value)

       # do not initialize library is primitive is non-fuzzable
        if self.fuzzable:
            self.init_library()
        else:
            self.complete = True

        # TODO: apply "before" transformations to self.value

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def get_mandatories(self, all_properties):
        props = []
        for property in all_properties:
            if property.get('mandatory') and property.get('mandatory') == 1:
                props.append(property.get('name'))
        return props

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def get_properties(self, properties):
        props = []
        for property in properties:
                props.append(property)
        return props

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def check_property(self, name, mandatories):
        props = []
        for prop in mandatories:
            props.append(prop)
        if name in props: return True
        return False

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def check_properties(self, all_properties, properties):
        mandatories = self.get_mandatories(all_properties)
        props = self.get_properties(properties)

        for mandatory in mandatories:
            if mandatory not in props:
                raise Exception(mandatory +\
                      ' property is mandatory but missing')

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def reset(self):
        self.mutation_index = 0
        self.value = self.library[0]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        if self.fuzzable:
            if self.mutation_index > len(self.library) - 1:
                self.complete = True
                self.value = self.library[0]

            if self.complete == True: return

            self.value = self.library[self.mutation_index]
            self.mutation_index += 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        return self.value
        # TODO: apply "after" transformations to self.value

