class Linear:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, b):
        try:
            if b.type != "block":
                raise Exception("logic has to be initialized with block")
        except Exception, ex:
            raise Exception("failed to initialize logic (%s)" % str(ex))
        self.root = b
        self.position = 0

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def base(self):
        data = []
        for item_position in range(0, len(self.root)):
            if self.position == item_position:
                data.append(str(self.root[item_position].value))
            else:
                r = self.root[item_position].render()
                if type(r).__name__ == "generator": r = r.next()
                data.append(r)
        return data

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        for item_position in range(0, len(self.root)):
            if self.position == item_position:
                if not self.root[item_position].get('ignore'):
                    while not self.root[item_position].complete:
                        self.root[item_position].mutate()
                        r = self.root[item_position].render()
                        if type(r).__name__ == "generator":
                            r = self.root[item_position].render().next()
                        data = self.base()
                        data[item_position] = r
                        yield data
                self.position += 1
        yield None

