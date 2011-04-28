import weakref

class DataSource(object):
    def __init__(self, name = '', initVal = False):
        self.listeners = []
        self.name = name
        self.val = initVal

    def __nonzero__(self):
        return self.val

    def add_listener(self, L):
        self.listeners += [weakref.ref(L)]
        
    def set(self, val):
        self.val = val
        self.listeners = filter(lambda x: x() != None, self.listeners)
        for l in self.listeners:
            l().set(val)