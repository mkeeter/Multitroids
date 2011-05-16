import sf
from data_logic import *
from keyboard import Keyboard
from virtual_keyboard import VirtualKeyboard
from ship import Ship
from asteroid import Asteroid
import random
from os import getcwd

class GameManager(object):
    """The game manager class handles the entire game system."""
    
    global RESOURCE_DIR
    
    def __init__(self):
        """Initialize the render window and start the game running"""

        # Constants
        FULLSCREEN = True
        self.FONT = sf.Font.load_from_file(RESOURCE_DIR + "raleway_thin.ttf")
        self.num_asteroids = 3
        self.view_size = sf.Vector2f(720, 450)
 
        # Initialize the window
        if FULLSCREEN:
            self.window = sf.RenderWindow(sf.VideoMode(1440, 900), "Multitroids",
                              sf.Style.FULLSCREEN,
                              sf.ContextSettings(antialiasing = 32))
#            self.image = sf.Image(1440, 900)
        else:
            self.window = sf.RenderWindow(sf.VideoMode(720, 450), "Multitroids",
                               sf.Style.DEFAULT,
                               sf.ContextSettings(antialiasing = 32))
#            self.image = sf.Image(720, 450)
        

        self.window.framerate_limit = 60
        self.window.view = sf.View.from_center_and_size(sf.Vector2f(),
                                                        self.view_size)
        self.window.show_mouse_cursor = False
        
        self.full_restart()
                
        self.state = 'start'
        
#        self.RECORDING = Toggle(source = self.keyboard[sf.Key.T],
#                                initVal = False)
#        self.frameNo = 0        
            

################################################################################

    def start_again(self):
        """Restart the game, preserving state.  Save a new virtual keyboard,
           and add the most recent set of commands to the army of ghost ships.
           """
        # Save a new virtual keyboard.
        self.keyboard.history += [(self.keyboard.time, sf.Key.SPACE, 'u')]
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

        self.bullets = []
        random.setstate(self.rand_state)
        self.asteroids = [Asteroid(self, clear_zone = self.view_size / 2.0,
                                   seed = random.random())
                          for i in range(self.num_asteroids)]

################################################################################
                          
    def full_restart(self):
        """Fully restart the game, clearing all history, etc."""
        # Initialize real and virtual keyboards.
        self.keyboard = Keyboard()
        self.virtual_keyboards = []
        
        # Initialize game objects
        self.players = [Ship(self.keyboard, self.view_size / 2.0)]
        self.bullets = []
        self.rand_state = random.getstate()

        self.asteroids = [Asteroid(self, clear_zone = self.view_size / 2.0,
                                   seed = random.random())
                          for i in range(self.num_asteroids)]
        
        self.DEBUG = DataToggle(source = self.keyboard[sf.Key.NUM0],
                                initVal = False)
                                
#        self.RECORDING = Toggle(source = self.keyboard[sf.Key.T],
#                                initVal = False)

        self.won = False

        # Start the system running
        self.running = DataToggle(
            source = DataOr(self.keyboard[sf.Key.ESCAPE],
                            DataAnd(self.keyboard[sf.Key.Q], 
                                    DataOr(self.keyboard[sf.Key.L_SYSTEM],
                                           self.keyboard[sf.Key.R_SYSTEM]))),
                                  initVal = True)
        
################################################################################

    def handle_input(self):
        """Processes the list of events, sending them to their various handlers.
        """
            
        for event in self.window.iter_events():
            # If the window is ever closed, stop running.
            if event.type == sf.Event.CLOSED:
                self.running = False
                return
            
            # Send key events to the keyboard, intercepting certain special
            # cases (that restart the game)
            elif event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Key.R or \
                  (event.code == sf.Key.SPACE and not self.players[-1].alive):
                    self.start_again()
                    continue
                self.keyboard.down(event.code)
                
            elif event.type == sf.Event.KEY_RELEASED:
                self.keyboard.up(event.code)  
                
        self.keyboard.increment()
        for vkb in self.virtual_keyboards:
            vkb.increment()
                
################################################################################

    def run(self):
        """Main game loop.  Updates all entities then draws everything,
        repeating over and over again."""
        
        # Begin loop
        while self.running:
            self.handle_input()
            self.update()
            if self.running:
                self.draw()
#                if self.RECORDING:
#                    self.image.copy_screen(self.window)
#                    self.image.save_to_file("frames/"+str(self.frameNo) + ".png")
#                    self.frameNo += 1
        self.shutdown()

################################################################################
    
    def update(self):
        """Update the game's state."""
        # Handle the menu screens
        if self.state == 'game':
            if len(self.asteroids) == 0:
                self.state = 'win'
                self.keyboard.up(sf.Key.SPACE)
                return
        else:
            if self.state == 'start' and self.keyboard[sf.Key.SPACE]:
                self.state = 'game'
                self.full_restart()
            elif self.state == 'win' and self.keyboard[sf.Key.SPACE]:
                self.state = 'start'
                self.keyboard.up(sf.Key.SPACE)
            return
                
        # Update the player, adding any bullets to the master list.
        for player in self.players:
            bullet = player.update(self)
            if bullet:
                self.bullets += [bullet]

        # Update bullets and keep only those that are alive.
        [bullet.update(self) for bullet in self.bullets]
        self.bullets = filter(lambda x: x.alive, self.bullets)
        
        # Figure out if any new asteroids spawn
        newAsteroids = []
        for asteroid in self.asteroids:
            newAsteroids += asteroid.update(self)
        self.asteroids = filter(lambda x: x.alive, self.asteroids)
        self.asteroids += newAsteroids
        
        # When the player dies, stop recording keystrokes.
        if not self.players[-1].alive and self.keyboard.recording:
            self.keyboard.recording = False

################################################################################
    
    def shutdown(self):
        """The program is about to end.  Clean up and close the window."""
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
        text.position = sf.Vector2f(0, self.view_size.y - 20)
        self.window.draw(text)

################################################################################

    def draw_HUD(self):
        """Draw text in the upper left corner showing how many ships have
           been used."""
        text = sf.Text("Ships: %d" % len(self.players), self.FONT, 30)
        text.style = sf.Text.BOLD
        text.scale = sf.Vector2f(0.5, 0.5)
        text.position = sf.Vector2f(15, 15)
        self.window.draw(text)
        
################################################################################
    
    def draw(self):
        """Draw the entire game window."""
        self.window.clear()
        
        self.window.view = sf.View.from_center_and_size(self.view_size / 2.,
                                                        self.view_size)        
        if self.DEBUG:
            self.draw_FPS()

        # Draw the start screen.
        if self.state == 'start':
            text = sf.Text("Multitroids", self.FONT, 200)
            text.scale = sf.Vector2f(0.5, 0.5)
            text.position = sf.Vector2f(self.view_size.x / 2.0 -
                                        text.rect.width / 2.0,
                                        self.view_size.y / 2.0 -
                                        text.rect.height - 30)
            self.window.draw(text)
            text = sf.Text("Arrow keys to fly\nSpacebar to shoot and restart"+
                           "\n\n    Press spacebar to begin",
                           self.FONT, 60)
            text.scale = sf.Vector2f(0.5, 0.5)
            text.position = sf.Vector2f(self.view_size.x / 2.0 -
                                        text.rect.width / 2.0,
                                        self.view_size.y / 2.0 +
                                        text.rect.height / 2.0 - 30)
            self.window.draw(text)
            text = sf.Text("www.mattkeeter.com",
                           self.FONT, 50)
            text.scale = sf.Vector2f(0.5, 0.5)
            text.position = sf.Vector2f(15,
                                        self.view_size.y -
                                        text.rect.height * 1.5)
            self.window.draw(text)
            self.window.display()
            return
        # Draw the end screen.
        elif self.state == 'win':
            text = sf.Text("YOU WIN", self.FONT, 160)
            text.scale = sf.Vector2f(0.5, 0.5)
            text.position = sf.Vector2f(self.view_size.x / 2.0 -
                                        text.rect.width / 2.0,
                                        self.view_size.y / 2.0 -
                                        text.rect.height)
            self.window.draw(text)
            text = sf.Text("Ships: %d" % len(self.players), self.FONT, 60)
            text.scale = sf.Vector2f(0.5, 0.5)
            text.position = sf.Vector2f(self.view_size.x / 2.0 -
                                        text.rect.width / 2.0,
                                        self.view_size.y / 2.0 +
                                        text.rect.height / 2.0)
            self.window.draw(text)
            text = sf.Text("Press spacebar to restart", self.FONT, 40)
            text.scale = sf.Vector2f(0.5, 0.5)
            text.position = sf.Vector2f(self.view_size.x / 2.0 -
                                        text.rect.width / 2.0,
                                        self.view_size.y / 2.0 +
                                        text.rect.height * 2.5)
            self.window.draw(text)
            self.window.display()
            return
            
        # Draw the rest of the game.
        for player in self.players:        
            player.draw(self.window)
        [bullet.draw(self.window) for bullet in self.bullets]
        
        # Draw each asteroid at 8 positions, so that they wrap around cleanly.
        for offset in [sf.Vector2f(0, 0), sf.Vector2f(self.view_size.x, 0),
                       sf.Vector2f(-self.view_size.x, 0),
                       sf.Vector2f(0, self.view_size.y),
                       sf.Vector2f(0, -self.view_size.y)]:
            [asteroid.draw(self.window, offset) for asteroid in self.asteroids]        
        
        self.draw_HUD()
        self.window.display()

################################################################################

RESOURCE_DIR = "./Resources/"

if __name__ == '__main__':
    # Figure out if this script is running from within a bundled application or
    # from the command line.  This will determine the path to resources.
    if "Resources" in getcwd():
        RESOURCE_DIR = "./"
    mgr = GameManager()
    mgr.run()