import sf
import random
from math import sqrt, cos, sin, pi

class Asteroid(object):
    def __init__(self, mgr = None, loc = None, size = 25,
                 clear_zone = None, seed = 1):
                 
        self.rand = random.Random()
        self.rand.seed(seed)
        
        if mgr:
            if loc:
                self.loc = loc.copy()
            else:
                self.loc = sf.Vector2f(self.rand.randint(0, mgr.view_size.x),
                                       self.rand.randint(0, mgr.view_size.y))
                self.size = size * 4
                # Look for a starting spot far away from the clear zone (which
                # is where the ship starts).
                while clear_zone:
                    if self.touches(clear_zone):
                        self.loc = sf.Vector2f(
                                    self.rand.randint(0, mgr.view_size.x),
                                    self.rand.randint(0, mgr.view_size.y))
                    else:
                        clear_zone = None

            self.momentum = sf.Vector2f(self.rand.randint(-10, 10) / 5.,
                                        self.rand.randint(-10, 10) / 5.)
        else:
            self.loc = sf.Vector2f()
            self.momentum = sf.Vector2f()
        self.alive = True
        self.size = size
        self.shape = sf.Shape()
        
        # Make irregular shape
        numPoints = 20
        for i in range(0, numPoints):
            angle = i/float(numPoints) * 2 * pi
            if self.rand.random() < 0.2:
                scale = 0
                while scale < 0.5:
                    scale = self.rand.random()
            else:
                scale = 1
            self.shape.add_point(cos(angle) * self.size * scale,
                                 sin(angle) * self.size * scale,
                                 sf.Color.BLACK, sf.Color.WHITE)
        self.shape.outline_thickness = 1
        self.shape.outline_enabled = True
        self.shape.fill_enabled = False
            
    
            
    def update(self, mgr = None):
        self.loc += self.momentum

        if not mgr:
            return []

        if not self.alive:
            if self.size < 10:
                return []
            return [Asteroid(mgr, loc = self.loc, size = self.size / 1.5,
                             seed = self.rand.random()) for i in range(3)]
            
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

    def draw(self, window, offset = sf.Vector2f(0, 0)):
        self.shape.position = self.loc + offset
        window.draw(self.shape)
        
    def touches(self, loc):
        if loc.x > (self.loc.x - self.size) and\
           loc.x < (self.loc.x + self.size) and\
           loc.y > (self.loc.y - self.size) and\
           loc.y < (self.loc.y + self.size):
           
            dist = loc - self.loc
            if pow(dist.x, 2) + pow(dist.y, 2) <= pow(self.size, 2):
                return True

        return False
        
    def distance(self, loc):
        dist = loc - self.loc
        return sqrt(pow(dist.x, 2) + pow(dist.y, 2)) - self.size
        

    