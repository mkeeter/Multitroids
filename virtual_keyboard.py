import sf
import data_logic

class VirtualKeyboard(object):
    """This class allows you to play back a set of keystrokes, repeating a
    certain behavior."""
    
    def __init__(self, keyboard):
        self.keys_down = {}
        self.history = keyboard.history
        self.time = 0
        self.i = 0
        for k in dir(sf.Key):
            kVal = eval("sf.Key."+k)
            if type(kVal) == int:
                self.keys_down[kVal] = data_logic.DataBit()

    def __getitem__(self, c):
        return self.keys_down[c]

    def down(self, code):
        """Sends a key down."""
        if not(self.keys_down[code]):
            self.keys_down[code].set(True)

    def up(self, code):
        """Sends a key release."""
        self.keys_down[code].set(False)
        
    def increment(self):
        while self.i < len(self.history) and self.history[self.i][0] == self.time:
            if self.history[self.i][2] == 'd':
                self.down(self.history[self.i][1])
            elif self.history[self.i][2] == 'u':
                self.up(self.history[self.i][1])
            self.i += 1
        self.time += 1
        
    def reset(self):
        self.time = 0
        self.i = 0
        for k in self.keys_down.keys():
            self.keys_down[k].set(False)