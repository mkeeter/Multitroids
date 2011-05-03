import data_sink
import sf
import bullet
from math import sin, cos, radians

class Ship(object):
    def __init__(self, keyboard, startLoc = sf.Vector2f(0, 0)):
        # Initialize inputs.
        self.LEFT  = data_sink.DataSink(source = keyboard[sf.Key.LEFT])
        self.RIGHT = data_sink.DataSink(source = keyboard[sf.Key.RIGHT])
        self.THRUST  = data_sink.DataSink(source = keyboard[sf.Key.UP])
        self.BRAKE  = data_sink.DataSink(source = keyboard[sf.Key.DOWN])
        self.SHOOT  = data_sink.DataSink(source = keyboard[sf.Key.SPACE])
        
        # And initialize movement state.
        self.loc = startLoc
        self.momentum = sf.Vector2f()
        self.angle = 180
        
        self.corners = [sf.Vector2f(-5, -5),
                        sf.Vector2f(5, -5),
                        sf.Vector2f(0, 10)]
        # Plus various other state things
        self.shootHeld = 0
        self.alive = True
        self.is_clone = False
        
################################################################################        
    def reset(self, keyboard, startLoc = sf.Vector2f(0, 0)):
        if keyboard:
            self.LEFT  = data_sink.DataSink(source = keyboard[sf.Key.LEFT])
            self.RIGHT = data_sink.DataSink(source = keyboard[sf.Key.RIGHT])
            self.THRUST  = data_sink.DataSink(source = keyboard[sf.Key.UP])
            self.BRAKE  = data_sink.DataSink(source = keyboard[sf.Key.DOWN])
            self.SHOOT  = data_sink.DataSink(source = keyboard[sf.Key.SPACE])
        self.loc = startLoc
        self.momentum = sf.Vector2f()
        self.angle = 180
        self.shootHeld = False
        self.alive = True
        self.is_clone = True
################################################################################

    def boundLoc(self, mgr):
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
################################################################################
    def update(self, mgr = None):
        if not self.alive:
            self.loc += self.momentum
            self.boundLoc(mgr)
            return
            
        for asteroid in mgr.asteroids:
            if asteroid.distance(self.loc) < 5:
                self.alive = False
    
        if self.LEFT and not self.RIGHT:
            self.angle -= 5
        elif self.RIGHT and not self.LEFT:
            self.angle += 5
        
        if self.THRUST:
            direction = sf.Vector2f(-sin(radians(self.angle)),
                                     cos(radians(self.angle)))
            self.momentum += 0.1 * direction
            speed = pow(self.momentum.x, 2) + pow(self.momentum.y, 2)
            if speed > 5:
                self.momentum *= 5 / speed
        elif self.BRAKE:
            self.momentum *= 0.9
            
        self.loc += self.momentum
        self.boundLoc(mgr)
        
        if self.SHOOT and self.shootHeld == 0:
            self.shootHeld = 10
            return bullet.Bullet(self.loc.copy(), self.angle)
        elif self.shootHeld > 0:
            self.shootHeld -= 1
################################################################################        
    def draw(self, window):
        if self.THRUST and self.alive:
            thrustshape = sf.Shape()
            thrustshape.add_point(-3, -6, sf.Color.BLACK, sf.Color.RED)
            thrustshape.add_point(3, -6, sf.Color.BLACK, sf.Color.RED)
            thrustshape.add_point(0, -10, sf.Color.BLACK, sf.Color.RED)
            thrustshape.outline_thickness = 1
            thrustshape.outline_enabled = True
            thrustshape.fill_enabled = False
            thrustshape.position = self.loc
            thrustshape.rotate(self.angle)
            window.draw(thrustshape)
    
        shipshape = sf.Shape()
        if self.is_clone:
            dark = 0.3
        else:
            dark = 1
        if self.alive:
            color = sf.Color(255 * dark, 255 * dark, 255 * dark)
        else:
            color = sf.Color(255 * dark, 0, 0)
        for c in self.corners:
            shipshape.add_point(c.x, c.y, sf.Color.BLACK, color)
        shipshape.outline_thickness = 1
        shipshape.outline_enabled = True
        shipshape.fill_enabled = False
        shipshape.position = self.loc
        shipshape.rotation = self.angle
        window.draw(shipshape)
        
