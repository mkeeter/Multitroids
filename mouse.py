import sf

class Mouse(object):
    def __init__(self):
        self.xloc = 0
        self.yloc = 0
        self.loc = sf.Vector2f()
        self.buttons = [0, 0, 0]
        
    def moved(self, x, y):
        """Call this function when the mouse moves."""
        self.xloc = x
        self.yloc = y

    def down(self, button):
        """Call this function when a button is pressed."""
        self.buttons[button] = True
        
    def up(self, button):
        """Call this function when a button is released."""
        self.buttons[button] = False