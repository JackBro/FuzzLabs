class LinearLogic:

    def __init__(self, b):
        try:
            if b.type != "block":
                raise Exception("logic has to be initialized with block")
        except Exception, ex:
            raise Exception("failed to initialize logic (%s)" % str(ex))
        self.root = b
        self.position = 0

    def run(self):
        for item_position in range(0, len(self.root)):
            if self.root[item_position].complete:
                self.position += 1
                continue
            if self.position == item_position:
                while not self.root[item_position].complete:
                    self.root[item_position].mutate()
                    data = []
                    # TODO: have to rework so all primitives incl blocks
                    #       are generators.
                    for iposition in range(0, len(self.root)):
                        d = self.root[iposition].render()
                        if type(d).__name__ == "str":
                            data.append(d)
                        if type(d).__name__ == "generator":
                            data.append(d.next())
                    yield "".join(data)
                self.position += 1

