import sf
from math import sin, cos, radians

class Bullet(object):
    def __init__(self, loc, angle, speed = 10):
        self.loc = loc
        self.angle = angle
        self.momentum = sf.Vector2f(-sin(radians(self.angle)),
                                     cos(radians(self.angle))) * speed
        self.life = 100

    def update(self, mgr = None):
        self.loc += self.momentum
        # Bound location within window.
        if not mgr:
            return
            
        if self.loc.x > mgr.view_size.x:
            self.loc.x -= mgr.view_size.x
        if self.loc.x < 0:
            self.loc.x += mgr.view_size.x
        if self.loc.y > mgr.view_size.y:
            self.loc.y -= mgr.view_size.y
        if self.loc.y < 0:
            self.loc.y += mgr.view_size.y
        self.life -= 1
        
        for asteroid in mgr.asteroids:
            if asteroid.touches(self.loc):
                asteroid.alive = False
                self.life = 0
            
    def draw(self, window):
        line = sf.Shape.line(0, -5, 0, 5, 1, sf.Color.GREEN)
        line.position = self.loc
        line.rotation = self.angle
        window.draw(line)
        
    def alive(self):
        return self.life > 0