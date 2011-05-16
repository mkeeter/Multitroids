import sf
import random
from math import sqrt, cos, sin, pi

class Asteroid(object):
    def __init__(self, mgr = None, loc = None, size = 25,
                 clear_zone = None, seed = 1, fragment = False):

        # Each asteroid keeps a personal random number generator, to make its
        # behavior deterministic.                 
        self.rand = random.Random()
        self.rand.seed(seed)
        
        # To make particles, we set fragment to true.
        self.fragment = fragment
        
        # Initialize the asteroid's location to somewhere within the window,
        # far from the ship's location.
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

        # State variables.            
        self.alive = True
        self.size = size
        self.drawSize = size
        
        # Make an irregular shape for the asteroid
        self.shape = sf.Shape()
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
        self.rotation = self.rand.randint(0, 360)
        self.dRot = self.rand.randint(-10, 10) / 10.0
        
    def update(self, mgr = None):
        """Update the asteroid's location and rotation.  If the astroid has
           died, return a list of new asteroids to manage."""
        self.loc += self.momentum
        self.rotation += self.dRot
        
        if not mgr:
            return []

        # If this asteroid is a fragment, slowly shrink in size.
        if self.fragment:
            self.drawSize -= 0.2
            if self.drawSize <= 0:
                self.alive = False
            return []

        # If this asteroid is dead, break into either fragments (if small)
        # or smaller asteroids (if large)
        if not self.alive and not self.fragment:
            if self.size < 10:
                return [Asteroid(mgr, loc = self.loc, size = 4,
                                 seed = self.rand.random(), fragment = True)
                        for i in range(10)]
            return [Asteroid(mgr, loc = self.loc, size = self.size / 1.5,
                             seed = self.rand.random()) for i in range(3)] + \
                    [Asteroid(mgr, loc = self.loc, size = 4,
                             seed = self.rand.random(), fragment = True)
                     for i in range(10)]
            
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

    def draw(self, window, offset = sf.Vector2f()):
        """Draw the asteroid, with a provided offset."""
        self.shape.position = self.loc + offset
        self.shape.rotation = self.rotation
        self.shape.scale = sf.Vector2f(float(self.drawSize) / float(self.size),
                                       float(self.drawSize) / float(self.size))
        window.draw(self.shape)
        
    def touches(self, loc):
        """Figure out if the asteroid is touching a point."""
        if self.fragment:
            return False
            
        if loc.x > (self.loc.x - self.size) and\
           loc.x < (self.loc.x + self.size) and\
           loc.y > (self.loc.y - self.size) and\
           loc.y < (self.loc.y + self.size):
           
            dist = loc - self.loc
            if pow(dist.x, 2) + pow(dist.y, 2) <= pow(self.size, 2):
                return True

        return False
        
    def distance(self, loc):
        """Return the distance between the asteroid and a given point."""
        dist = loc - self.loc
        return sqrt(pow(dist.x, 2) + pow(dist.y, 2)) - self.size
        

    