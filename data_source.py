class DataSource(object):
    def __init__(self, name = '', initVal = False):
        self.listeners = []
        self.name = name
        self.val = initVal

    def __del__(self):
        for l in self.listeners:
            l.source = None

    def __nonzero__(self):
        return self.val

    def add_listener(self, L):
        self.listeners += [L]
        
    def remove_listener(self, L):
        self.listeners = filter(lambda x: x != L, self.listeners)
        
    def set(self, val):
        self.val = val
        for l in self.listeners:
            l.set(val)