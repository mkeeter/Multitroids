class DataBit(object):
    """This is a simple data container.  It allows multiple references to the
       same container, which allows for easy data sharing."""
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
            raise Exception("Trying to set a value in a sink-style DataBit.")            
        self.val = val

################################################################################
            
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

################################################################################

class DataEdge(object):
    """This is a data sink that is high for one tick at incoming data edge."""
    def __init__(self, source):
        self.source = source
        self._val = False
        self.triggered = False
        
    def __nonzero__(self):
        return self.val
        
    @property    
    def val(self):
        # Otherwise, change values at a rising clock edge.
        if self.source.val and not self._val and not self.triggered:
            self._val = 1
            self.triggered = True
        else:
            self._val = 0

        if not self.source.val:
            self.triggered = False
            
        return self._val
        
################################################################################

class DataNot(object):
    """This data object performs a logical NOT on its input."""
    def __init__(self, source):
        self.source = source

    def __nonzero__(self):
        return self.val

    @property
    def val(self):
        return not self.source.val
        
################################################################################

class DataOr(object):
    """This data object performs a logical OR on a set of inputs."""
    def __init__(self, *args):
        self.values = [DataBit(s) for s in args]
        
    def __nonzero__(self):
        return self.val

    @property    
    def val(self):
        return any(self.values)
        
################################################################################
        
class DataAnd(object):
    """This data object performs a logical AND on a set of inputs."""
    def __init__(self, *args):
        self.values = [DataBit(s) for s in args]
        
    def __nonzero__(self):
        return self.val

    @property    
    def val(self):
        return all(self.values)

################################################################################

class DataExpr(object):
    """This data object executes an arbitrary function."""
    def __init__(self, expr):
        self.expr = expr

    def __nonzero__(self):
        return self.val

    @property    
    def val(self):
        return self.expr()
        
