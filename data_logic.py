import weakref

class DataBit(object):
    def __init__(self, source = None, initVal = False):
        if source is not None:
            self.source = source
            self.val = None
        else:
            self.source = None
            self.val = initVal

    def __nonzero__(self):
        if self.source is None:
            return self.val
        return self.source.val

        
    def set(self, val):
        if self.val is None:
            raise Exception("Warning: Trying to set a value in a sink-style DataBit.")            
        self.val = val
            
class DataToggle(object):
    """This is a data sink that switches every time the input transitions
    between low and high."""
    def __init__(self, source, initVal = False):
        self.source = source
        self._val = initVal
        self.clk = False
        
    def __nonzero__(self):
        return self.val
        
    @property    
    def val(self):
        # Otherwise, change values at a rising clock edge.
        if self.source.val and not self.clk:
            self._val = not(self._val)
        self.clk = self.source.val
        return self._val


class DataOr(object):
    def __init__(self, *args):
        self.values = [DataBit(s) for s in args]
        
    def __nonzero__(self):
        return self.val

    @property    
    def val(self):
        return any(self.values)
        
        
class DataAnd(object):
    def __init__(self, *args):
        self.values = [DataBit(s) for s in args]
        
    def __nonzero__(self):
        return self.val

    @property    
    def val(self):
        return all(self.values)