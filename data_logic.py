import weakref

class DataBit(object):
    def __init__(self, source = None, initVal = False):
        self.listeners = []
        if source is not None:
            source.add_listener(self)
            self.val = source.val
        else:
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
            
class DataToggle(object):
    """This is a data sink that switches every time the input transitions
    between low and high."""
    def __init__(self, source, initVal = False):
        self.listeners = []
        if source is not None:
            source.add_listener(self)
        self.val = initVal
        self.clk = False
        
    def __nonzero__(self):
        return self.val
        
    def set(self, clk):
        """May switch the toggle.  This should not be called manually."""
        # Change stored value on a rising clock edge
        if clk and not self.clk:
            self.val = not(self.val)
        self.clk = clk
        # Pass changes to all of the listeners
        self.listeners = filter(lambda x: x() != None, self.listeners)
        for l in self.listeners:
            l().set(val)