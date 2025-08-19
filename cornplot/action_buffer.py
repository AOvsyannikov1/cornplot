class ActionBuffer(list):

    def __init__(self):
        super(ActionBuffer, self).__init__()

    def add_action(self, xstart, xstop, ystart, ystop):
        self.append((xstart, xstop, ystart, ystop))

    def get_last_action(self):
        if len(self) > 0:
            return self.pop(-1)
        else:
            return False
