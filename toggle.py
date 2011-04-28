class Toggle(object):
    """This is a data sink that switches every time the input transitions
    between low and high."""
    def __init__(self, source, name = '', initVal = False):
        source.add_listener(self)
        self.source = source
        self.name = name
        self.val = initVal
        self.clk = False
        
    def __nonzero__(self):
        return self.val
        
    def detach(self):
        """Cleanly detach a sink from a source."""
        self.source.RemoveListener(self)
        
    def set(self, clk):
        """May switch the toggle.  This should not be called manually."""
        if clk and not self.clk:
            self.val = not(self.val)
        self.clk = clk