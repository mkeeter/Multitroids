import sf
import data_source

class Keyboard(object):
    """The Keyboard class allows us to listen for key presses, then pass them
    on to a set of listeners."""
    
    def __init__(self):
        self.keys_down = {}
        self.history = []
        self.time = 0
        for k in dir(sf.Key):
            kVal = eval("sf.Key."+k)
            if type(kVal) == int:
                self.keys_down[kVal] = data_source.DataSource()
        self.recording = True

    def __getitem__(self, c):
        return self.keys_down[c]

    def down(self, code):
        """Record a key press."""
        if not(code in self.keys_down.keys()):
            print "Key not found (code",code,")"
            return
        # Set keys_down to be true for this character.  
        if not(self.keys_down[code]):
            self.keys_down[code].set(True)
        if self.recording:
            self.history += [(self.time, code, 'd')]

    def up(self, code):
        """Record a key release."""
        if not(code in self.keys_down.keys()):
            return
        self.keys_down[code].set(False)
        if self.recording:
            self.history += [(self.time, code, 'u')]

    def increment(self):
        self.time += 1
        
    def reset(self):
        self.time = 0
        self.history = []
        for k in self.keys_down.keys():
            self.keys_down[k].set(False)
        self.recording = True