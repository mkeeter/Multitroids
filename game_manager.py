import sf
from keyboard import Keyboard
from virtual_keyboard import VirtualKeyboard
from mouse import Mouse
from ship import Ship
from toggle import Toggle
from asteroid import Asteroid
import random

class GameManager(object):
    """The game manager class handles the entire game system."""
    
    def __init__(self):
        """Initialize the render window and set the game as running"""

        # Initialize the window
        self.window = sf.RenderWindow(sf.VideoMode(800, 600),\
                                      "Swarm")
        self.window.framerate_limit = 60
        self.view_size = sf.Vector2f(800, 600)
        self.window.view = sf.View.from_center_and_size(sf.Vector2f(),
                                                        self.view_size)        
        # Initialize real and virtual keyboards.
        self.keyboard = Keyboard()
        self.virtual_keyboards = []
        self.mouse = Mouse()
        
        # Initialize game objects
        self.players = [Ship(self.keyboard, self.view_size / 2.0)]
        self.bullets = []
        self.rand_state = random.getstate()
        self.asteroids = [Asteroid(self, clear_zone = self.view_size / 2.0,
                                   seed = random.random())
                          for i in range(0)]
        
        self.DEBUG = Toggle(source = self.keyboard[sf.Key.NUM0],
                            initVal = False)

        # Start the system running
        self.running = Toggle(initVal = True,\
                              source = self.keyboard[sf.Key.ESCAPE])
            

################################################################################

    def start_again(self):
        # Save a new virtual keyboard.
        self.virtual_keyboards += [VirtualKeyboard(self.keyboard)]
        
        # Switch over the last bot to running on the virtual keyboard.
        self.players[-1].reset(self.virtual_keyboards[-1],
                               self.view_size / 2.0)
        
        self.players += [Ship(self.keyboard, self.view_size / 2.0)]
        
        # Reset all of the keyboards, real and virtual.
        for vkb in self.virtual_keyboards:
            vkb.reset()
        self.keyboard.reset()
        
        # Reset player locations
        for player in self.players:
            player.reset(None, self.view_size / 2.0)
        self.players[-1].is_clone = False

        random.setstate(self.rand_state)
        self.asteroids = [Asteroid(self, clear_zone = self.view_size / 2.0,
                                   seed = random.random())
                          for i in range(0)]
        
################################################################################

    def handle_input(self):
        """Processes the list of events, sending them to their various handlers.
        """
        self.keyboard.increment()
        for vkb in self.virtual_keyboards:
            vkb.increment()
            
        for event in self.window.iter_events():
            # If the window is ever closed, stop running.
            if event.type == sf.Event.CLOSED:
                self.running = False

            elif event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Key.R or \
                  (event.code == sf.Key.SPACE and not self.players[-1].alive):
                    self.start_again()
                    continue
                # Pass the key into the keyboard data handler.
                self.keyboard.down(event.code)
                
            elif event.type == sf.Event.KEY_RELEASED:
                self.keyboard.up(event.code)  

            elif event.type == sf.Event.MOUSE_MOVED:
                self.mouse.moved(event.x, event.y)
            
            elif event.type == sf.Event.MOUSE_BUTTON_PRESSED:
                self.mouse.down(event.button)

            elif event.type == sf.Event.MOUSE_BUTTON_RELEASED:
                self.mouse.up(event.button)
                
################################################################################

    def run(self):
        """Main game loop.  Updates all entities then draws everything,
        repeating over and over again."""
        
        # Begin loop
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
        self.shutdown()

################################################################################
    
    def update(self):
        for player in self.players:
            bullet = player.update(self)
            if bullet:
                self.bullets += [bullet]
        [bullet.update(self) for bullet in self.bullets]
        self.bullets = filter(lambda x: x.alive, self.bullets)
        
        # Figure out if any new asteroids spawn
        newAsteroids = []
        for asteroid in self.asteroids:
            newAsteroids += asteroid.update(self)
        self.asteroids = filter(lambda x: x.alive, self.asteroids)
        self.asteroids += newAsteroids

################################################################################
    
    def shutdown(self):
        """The program is about to end.  Clean up and close the window."""
        # Close the window.
        self.window.close()

################################################################################
    
    def draw_FPS(self):
        """Write the number of frames per second in the upper left corner."""
        ft = self.window.frame_time
        if (ft > 0):
            text = sf.Text("FPS: %(fps)03d" % {'fps': 1 / ft})
        else:
            text = sf.Text("FPS:inf")
        text.scale = sf.Vector2f(0.5, 0.5)
        self.window.draw(text)

################################################################################
    
    def draw(self):
        self.window.clear()
        
        self.window.view = sf.View.from_center_and_size(self.view_size / 2.,
                                                        self.view_size)        
        self.draw_FPS()

        for player in self.players:        
            player.draw(self.window)
        [bullet.draw(self.window) for bullet in self.bullets]
        [asteroid.draw(self.window) for asteroid in self.asteroids]        
        
        self.window.display()

################################################################################

    def drawGrid(self):
        center = self.window.view.center
        size = self.window.view.size
        
        stepSize = 50
        
        startX = int(center[0] - size[0]) - int(center[0] - size[0]) % stepSize
        endX =   int(center[0] + size[0]) - int(center[0] + size[0]) % stepSize
        startY = int(center[1] - size[1]) - int(center[1] - size[1]) % stepSize
        endY =   int(center[1] + size[1]) - int(center[1] + size[1]) % stepSize

        color = sf.Color(120, 120, 120)
        
        for i in range(startX, endX, stepSize):
            for j in range(startY, endY, stepSize):
                circ = sf.Shape.circle(i, j, 2, color)
                self.window.draw(circ)
        circ = sf.Shape.circle(0, 0, 5, sf.Color.BLUE)
        self.window.draw(circ)

################################################################################

if __name__ == '__main__':
    mgr = GameManager()
    mgr.run()