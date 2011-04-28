import sf
from keyboard import Keyboard
from virtual_keyboard import VirtualKeyboard
from mouse import Mouse
from bot import Bot
from blob import Blob
from tile_map import TileMap
from toggle import Toggle

class GameManager(object):
    """The game manager class handles the entire game system."""
    
    def __init__(self):
        """Initialize the render window and set the game as running"""

        # Initialize the window
        self.window = sf.RenderWindow(sf.VideoMode(800, 600),\
                                      "Time & Time Again")
        self.window.framerate_limit = 60
        self.view_size = sf.Vector2f(32 * 12, 32 * 9)
        self.window.view = sf.View.from_rect(sf.FloatRect(0, 0,
                                                          self.view_size.x,
                                                          self.view_size.y))
        # Initialize real and virtual keyboards.
        self.keyboard = Keyboard()
        self.virtual_keyboards = []
        self.mouse = Mouse()
        
        # Initialize everything else
        self.tile_map = TileMap('basic')
        self.players = [Bot(self.keyboard, self.tile_map.start_loc)]
        self.bullets = []

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
                               self.tile_map.start_loc)
        
        self.players += [Bot(self.keyboard)]
        
        # Reset all of the keyboards, real and virtual.
        for vkb in self.virtual_keyboards:
            vkb.reset()
        self.keyboard.reset()
        
        # Reset player locations
        for player in self.players:
            player.reset(None, self.tile_map.start_loc)
        self.players[-1].is_clone = False
            
        
################################################################################

    def handle_events(self):
        """Processes the list of events, sending them to their various handlers.
        """
        for event in self.window.iter_events():
            # If the window is ever closed, stop running.
            if event.type == sf.Event.CLOSED:
                self.running = False

            elif event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Key.R:
                    self.start_again()
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
            self.handle_events()
            self.update()
            self.window.clear()
            self.draw()
            self.window.display()
        self.shutdown()

################################################################################
    
    def update(self):
        [bullet.update(self) for bullet in self.bullets]

        for player in self.players:
            bullet = player.update(self)
            if  bullet:
                self.bullets += [bullet]

        self.keyboard.increment()
        for vkb in self.virtual_keyboards:
            vkb.increment()

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
        text.scale = sf.Vector2f(0.25, 0.25)
        self.window.draw(text)

################################################################################
    
    def draw(self):
        view = sf.View.from_center_and_size(self.players[-1].get_center(),\
                                            self.view_size)
        view = self.tile_map.bound_view(view)
        self.window.view = view
        self.tile_map.draw(self.window)

        [player.draw(self.window, debug = self.DEBUG) for player in self.players]
        
        [bullet.draw(self.window) for bullet in self.bullets]
        self.window.view = sf.View.from_center_and_size(self.view_size / 2.0,\
                                                        self.view_size)
        self.draw_FPS()

################################################################################

if __name__ == '__main__':
    mgr = GameManager()
    mgr.run()