import sf
import data_logic

class Keyboard(object):
    """The Keyboard class records a set of key presses."""
    
    def __init__(self):
        self.keys_down = {}
        self.history = []
        self.time = 0
        for k in dir(sf.Key):
            kVal = eval("sf.Key."+k)
            if type(kVal) == int:
                self.keys_down[kVal] = data_logic.DataBit()
        self.recording = True

    def __getitem__(self, c):
        return self.keys_down[c]

    def down(self, code):
        """Call this when a key is pressed."""
        
        if not(code in self.keys_down.keys()):
            return

        self.keys_down[code].set(True)
        if self.recording:
            self.history += [(self.time, code, 'd')]

    def up(self, code):
        """Call this when a key is released."""
        
        if not(code in self.keys_down.keys()):
            return

        self.keys_down[code].set(False)
        if self.recording:
            self.history += [(self.time, code, 'u')]

    def increment(self):
        """Increment internal timer."""
        self.time += 1
        
    def reset(self):
        """Reset to original state."""
        self.time = 0
        self.history = []
        for k in self.keys_down.keys():
            self.keys_down[k].set(False)
        self.recording = True