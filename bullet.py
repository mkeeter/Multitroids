import sf
from math import sin, cos, radians

class Bullet(object):
    def __init__(self, loc, angle, speed = 10):
        self.loc = loc
        self.angle = angle
        self.momentum = sf.Vector2f(-sin(radians(self.angle)),
                                     cos(radians(self.angle))) * speed
        self.life = 20
        self.alive = True
        
    def update(self, mgr = None):
        """Update the bullet's position, checking to see if it hits any
           asteroids"""
           
        # We move in 4 small jumps, to avoid glitching through a small asteroid.
        for i in range(4):
            self.loc += self.momentum / 4
            
            # Bound location within window.
            if mgr:
                if self.loc.x > mgr.view_size.x:
                    self.loc.x -= mgr.view_size.x
                if self.loc.x < 0:
                    self.loc.x += mgr.view_size.x
                if self.loc.y > mgr.view_size.y:
                    self.loc.y -= mgr.view_size.y
                if self.loc.y < 0:
                    self.loc.y += mgr.view_size.y
                
            for asteroid in mgr.asteroids:
                if asteroid.touches(self.loc):
                    asteroid.alive = False
                    self.alive = False

        # Bullets have a limited lifetime.
        self.life -= 1
        if self.life <= 0:
            self.alive = False
            
    def draw(self, window):
        """Draw the bullet as a straight green line."""

        if self.life < 5:
            alpha = int(255 * float(self.life) / 5.0)
        else:
            alpha = 255
        
        line = sf.Shape.line(0, -5, 0, 5, 1, sf.Color(0, 255, 0, alpha))
        line.position = self.loc
        line.rotation = self.angle
        window.draw(line)