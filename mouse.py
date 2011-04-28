import sf

class Mouse(object):
    def __init__(self):
        self.xloc = 0
        self.yloc = 0
        self.loc = sf.Vector2f()
        self.buttons = [0, 0, 0]
        
    def moved(self, x, y):
        self.xloc = x
        self.yloc = y

    def down(self, button):
        self.buttons[button] = True
        
    def up(self, button):
        self.buttons[button] = False