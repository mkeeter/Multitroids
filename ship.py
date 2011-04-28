import data_sink
import sf
from math import sin, cos, radians

class Ship(object):
    def __init__(self, keyboard, startLoc = sf.Vector2f(0, 0)):
        # Initialize inputs
        self.LEFT  = data_sink.DataSink(source = keyboard[sf.Key.A])
        self.RIGHT = data_sink.DataSink(source = keyboard[sf.Key.D])
        self.THRUST  = data_sink.DataSink(source = keyboard[sf.Key.W])
        self.BRAKE  = data_sink.DataSink(source = keyboard[sf.Key.S])
        
        self.loc = sf.Vector2f()
        self.momentum = sf.Vector2f()
        self.angle = 0
        self.ang_vel = 0

    def update(self):
        if self.LEFT and not self.RIGHT:
            self.ang_vel = -5
        elif self.RIGHT and not self.LEFT:
            self.ang_vel = 5
        else:
            self.ang_vel = 0
        
        if self.THRUST:
            direction = sf.Vector2f(sin(radians(self.angle)),
                                    -cos(radians(self.angle)))
            self.momentum += 0.1 * direction
            speed = pow(self.momentum.x, 2) + pow(self.momentum.y, 2)
            if speed > 5:
                self.momentum *= 5 / speed
        elif self.BRAKE:
            self.momentum *= 0.9
            
        self.loc += self.momentum
        self.angle += self.ang_vel
        
    def draw(self, window):
        if self.THRUST:
            thrustshape = sf.Shape()
            thrustshape.add_point(self.loc.x - 3, self.loc.y - 5,
                            sf.Color.BLACK, sf.Color.RED)
            thrustshape.add_point(self.loc.x + 3, self.loc.y - 5,
                            sf.Color.BLACK, sf.Color.RED)
            thrustshape.add_point(self.loc.x, self.loc.y - 10,
                            sf.Color.BLACK, sf.Color.RED)
            thrustshape.outline_thickness = 1
            thrustshape.outline_enabled = True
            thrustshape.origin = self.loc
            thrustshape.rotate(self.angle)
            window.draw(thrustshape)
    
        shipshape = sf.Shape()
        shipshape.add_point(self.loc.x - 5, self.loc.y - 5,
                        sf.Color.BLACK, sf.Color.WHITE)
        shipshape.add_point(self.loc.x + 5, self.loc.y - 5,
                        sf.Color.BLACK, sf.Color.WHITE)
        shipshape.add_point(self.loc.x, self.loc.y + 10,
                        sf.Color.BLACK, sf.Color.WHITE)
        shipshape.outline_thickness = 1
        shipshape.outline_enabled = True
        shipshape.origin = self.loc
        shipshape.rotate(self.angle)
        window.draw(shipshape)
        
