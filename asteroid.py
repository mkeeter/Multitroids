import sf
from random import randint

class Asteroid(object):
    def __init__(self, mgr = None, loc = None, size = 25):
        if mgr:
            if loc:
                self.loc = loc.copy()
            else:
                self.loc = sf.Vector2f(randint(0, mgr.view_size.x),
                                       randint(0, mgr.view_size.y))

            self.momentum = sf.Vector2f(randint(-2, 2), randint(-2, 2))
        else:
            self.loc = sf.Vector2f()
            self.momentum = sf.Vector2f()
        self.alive = True
        self.size = size
    
            
    def update(self, mgr = None):
        self.loc += self.momentum

        if not mgr:
            return []

        if not self.alive:
            if self.size < 5:
                return []
            return [Asteroid(mgr, self.loc, self.size / 1.5) for i in range(5)]
            
        # Bound location within window.            
        if self.loc.x > mgr.view_size.x:
            self.loc.x -= mgr.view_size.x
        if self.loc.x < 0:
            self.loc.x += mgr.view_size.x
        if self.loc.y > mgr.view_size.y:
            self.loc.y -= mgr.view_size.y
        if self.loc.y < 0:
            self.loc.y += mgr.view_size.y
            
        return []

    def draw(self, window):
        if self.alive:
            color = sf.Color.WHITE
        else:
            color = sf.Color.BLACK
            
        circ = sf.Shape.circle(self.loc.x, self.loc.y, self.size,
                               sf.Color.BLACK, 1, color)
        circ.fill_enabled = False
        window.draw(circ)
        
    def touches(self, loc):
        if loc.x > (self.loc.x - self.size) and\
           loc.x < (self.loc.x + self.size) and\
           loc.y > (self.loc.y - self.size) and\
           loc.y < (self.loc.y + self.size):
           
            dist = loc - self.loc
            if pow(dist.x, 2) + pow(dist.y, 2) <= pow(self.size, 2):
                return True

        return False
        

    