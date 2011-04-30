import sf

class Asteroid(object):
    def __init__(self, mgr = None):
        if mgr:
            self.loc = sf.Vector2f(randint(0, mgr.view_size.x),
                                   randint(0, mgr.view_size.y))
            self.momentum = sf.Vector2f(randint(4, 10), randint(4, 10))
        else:
            self.loc = sf.Vector2f()
            self.momentum = sf.Vector2f()
            
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

    def draw(self, window):
        circ = sf.Shape.circle(self.loc.x, self.loc.y, 2, sf.Color.WHITE)
        window.draw(circ)

    