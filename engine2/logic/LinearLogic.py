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

        # There are 3 states:
        #    - items that are complete
        #    - item that have to be mutated
        #    - item that do not have to be mutated yet

        for item_position in range(0, len(self.root)):
            if self.root[item_position].complete:
                self.position += 1
                continue
            if self.position == item_position:
                while not self.root[item_position].complete:
                    self.root[item_position].mutate()
                    data = []
                    for iposition in range(0, len(self.root)):
                        data.append(self.root[iposition].render())
                    yield "".join(data)
                self.position += 1

