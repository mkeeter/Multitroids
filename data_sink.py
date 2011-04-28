class DataSink(object):
    """This data sink stores a single value, passed in from some kind of data
    source."""
    def __init__(self, source, name = '', initVal = False):
        source.add_listener(self)
        self.source = source
        self.name = name
        self.val = initVal
        
    def __nonzero__(self):
        return self.val
        
    def detach(self):
        """Cleanly detach a sink from a source."""
        self.source.remove_listener(self)
        
    def set(self, val):
        """Set the value of the data sink.  This should not be called
        manually."""
        self.val = val