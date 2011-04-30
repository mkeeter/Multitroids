import data_sink
import sf
import bullet
from math import sin, cos, radians

class Ship(object):
    def __init__(self, keyboard, startLoc = sf.Vector2f(0, 0)):
        # Initialize inputs.
        self.LEFT  = data_sink.DataSink(source = keyboard[sf.Key.A])
        self.RIGHT = data_sink.DataSink(source = keyboard[sf.Key.D])
        self.THRUST  = data_sink.DataSink(source = keyboard[sf.Key.W])
        self.BRAKE  = data_sink.DataSink(source = keyboard[sf.Key.S])
        self.SHOOT  = data_sink.DataSink(source = keyboard[sf.Key.SPACE])
        
        # And initialize movement state.
        self.loc = startLoc
        self.momentum = sf.Vector2f()
        self.angle = 0
        
        # Plus various other state things
        self.shootHeld = False

    def update(self, mgr = None):
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
        
        if self.SHOOT and not self.shootHeld:
            self.shootHeld = True
            return bullet.Bullet(self.loc.copy(), self.angle)
        elif not self.SHOOT:
            self.shootHeld = False
        
    def draw(self, window):
        if self.THRUST:
            thrustshape = sf.Shape()
            thrustshape.add_point(-3, -5, sf.Color.BLACK, sf.Color.RED)
            thrustshape.add_point(3, -5, sf.Color.BLACK, sf.Color.RED)
            thrustshape.add_point(0, -10, sf.Color.BLACK, sf.Color.RED)
            thrustshape.outline_thickness = 1
            thrustshape.outline_enabled = True
            thrustshape.position = self.loc
            thrustshape.rotate(self.angle)
            window.draw(thrustshape)
    
        shipshape = sf.Shape()
        shipshape.add_point(-5, -5, sf.Color.BLACK, sf.Color.WHITE)
        shipshape.add_point(5,  -5, sf.Color.BLACK, sf.Color.WHITE)
        shipshape.add_point(0, 10, sf.Color.BLACK, sf.Color.WHITE)
        shipshape.outline_thickness = 1
        shipshape.outline_enabled = True
        shipshape.position = self.loc
        shipshape.rotation = self.angle
        window.draw(shipshape)
        
