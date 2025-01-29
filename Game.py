import pygame
import sys
import random
from Scripts.ui import Button, Text, TextBox
from Scripts.util import loadImage

class Game:
    
    def __init__(self):

         # Starts up Pygame
        pygame.init()

        # Sets the name of the window icon to "Rogue-like"
        pygame.display.set_caption("Unleached")

        # Creating a screen variable with the window dimension variables set above
        # when setting window dimensions have to do .set_mode( (_,_) )
        # Treat the (_,_) as order pairs inside of ( (_,_) ).
        self.screen = pygame.display.set_mode((1280 , 720 ))

        self.titleColor = (200, 50, 50)

        self.fonts = {
            'title': pygame.font.Font('Media/Assets/Fonts/fantasy.ttf', 100),
            'shopTitle': pygame.font.Font('Media/Assets/Fonts/fantasy.ttf', 100)
        }
        
        # Stores the TextBox objects for the introduction exposition.
        self.startingText = {
            'Intro': TextBox(200, 75, 900, 600, text="Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah")
        }

        # Stores the Buttons objects for the main menu
        self.menuState = "main"

        # Stores the Button objects for the main menu.
        self.mainMenuOptions = {
            'Title': Text(500, 200, 280, 50, 'Unleeched', self.fonts['title'], self.titleColor),
            'Start': Button(500, 375, 280, 50, 'Start'),
            'Shop': Button(500, 450, 280, 50, 'Shop'),
            'Exit': Button(500, 525, 280, 50, 'Exit')
        }

        # Stores the Button objects for the battle menu.
        self.battle = {
            # The text box is at the beginning of the map because it will be the first thing to be drawn.
            'Text': TextBox(200, 75, 900, 600, text=''),
            'Attack': Button(500, 500, 280, 50, 'Attack'),
            'Skill': Button(500, 575, 280, 50, 'Skill'),
            'Guard': Button(500, 575, 280, 50, 'Guard'),
            'Inventory': Button(500, 650, 280, 50, 'Inventory')
        }
        
        # Stores the Button objects for the shop menu.
        self.shopOptions = {
            'Box': TextBox(200, 75, 900, 600, '', (43, 44, 58, 160)),
            'Title': Text(500, 120, 280, 50, 'Upgrades', self.fonts['shopTitle'], self.titleColor),
            'Attack':Button(275, 500, 140,50, 'Attack'),
            'Infection': Button(575, 500, 140, 50, 'Infect'),
            'SP': Button(875, 500, 140, 50, 'SP'),
            'Back': Button(20, 620, 140, 50, 'Back')
        }

        # Manages the upgrades the players have
        self.upgrades = {
           'attack': 0,
           'infection': 0,
           'sp': 0
        }

        self.itemReward = {
            'reward': TextBox(200, 600, 900, 200, text="Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah Blah")

        }

        # Maintains the game state to determine which menu to display.
        self.gameStates = {
            'main': True, 
            'shop': False, 
            'startGame':False,
            'battle': False, 'intermission': False, 
            'gameOver': False,
            'itemReward': False,
            
        }

       

        # Stores the selected button by the player.
        self.selectedOption = None

        self.assets = {
            'titleBackground':pygame.transform.scale(loadImage('/background/otherTitle.png').convert_alpha(), (1280, 720)),
            'intermission': pygame.transform.scale(loadImage('/background/intermission.png').convert_alpha(), (1280, 720)),
            'intermissionSong': pygame.mixer.Sound('Media/Music/intermission.wav'),
            'titleSong': pygame.mixer.Sound('Media/Music/title.wav'),
            'shopBackground': pygame.transform.scale(loadImage('/background/shop.png'), (1280, 720))
        }

        self.intermission = {
            'left': Button(100, 300, 200, 100, 'Left'),
            'right': Button(1000, 300, 200, 100, 'Right')
        }
        
        # Maintains and increments the numbers of upgrades purchased in
        # the shop.
        self.upgrades = {
            'Attack':0,
            'SP': 0, 
            'Infection': 0
        }

         # Flags to track if certain music are playing.
        self.intermissionMusicPlaying = False
        self.titleMusicPlaying = False

    def drawMenu(self, menu):
        # Draw the menu options for the main menu.
        for option in menu.values():
            option.draw(self.screen)


    def run(self):
        while True:

            clock = pygame.time.Clock() # Initiates clock
            
            # Plays the intermission song after the intro exposition.
            if self.gameStates['intermission'] and not self.intermissionMusicPlaying:
                self.assets['titleSong'].stop()
                self.assets['intermissionSong'].play(-1)
                self.intermissionMusicPlaying = True
                self.titleMusicPlaying = False

            # Plays the title song when in the main menu and the exposition state.
            elif (self.gameStates['main'] or self.gameStates['startGame'] or self.gameStates['shop']) and not self.titleMusicPlaying:
                self.assets['intermissionSong'].stop()
                self.assets['titleSong'].play(-1)
                self.titleMusicPlaying = True
                self.intermissionMusicPlaying = False

            
            # Event loop
            for event in pygame.event.get():

                # Exit the game when pressing the close button on window.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check if the mouse button is pressed.
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Checks if the left mouse button is pressed.
                    if event.button == 1:
                        mousePos = pygame.mouse.get_pos()

                        # After pressing left or right button, create a 50% chance for a battle and a 50% chance for a bonus intermission
                        if self.gameStates['intermission']:
                            if self.intermission['right'].rect.collidepoint(mousePos):
                                
                                self.gameStates['intermission'] = False
                                self.gameStates['itemReward'] = True
                                # if random.random() < .5:
                                #     self.gameStates['intermission'] = False
                                #     self.gameStates['battle'] = True
                                # else:
                                #     self.gameStates['intermission'] = False
                                #     self.gameStates['itemReward'] = True
                            
                            elif self.intermission['left'].rect.collidepoint(mousePos):

                                if random.random() < .5:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['battle'] = True
                                else:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['itemReward'] = True

                        # Switches to the shop menu when the shop button is clicked.
                        if self.gameStates['main']:

                            if self.mainMenuOptions['Shop'].rect.collidepoint(mousePos):
                                self.gameStates['main'] = False
                                self.gameStates['shop'] = True


                            # Exits the game when the exit button is clicked.
                            if self.mainMenuOptions['Exit'].rect.collidepoint(mousePos):
                                pygame.quit()
                                sys.exit()

                            # Starts game when start button is hit.
                            if self.mainMenuOptions['Start'].rect.collidepoint(mousePos):
                                self.gameStates['Start'] = True
                                self.gameStates['main'] = False
                                self.gameStates['shop'] = False

                        # Switches back to the main menu when the back button is clicked.
                        if self.gameStates['shop']:

                            # Changes color of shop buttons if hovering over them.
                            for button in self.shopOptions.values():
                                button.isHovered = button.rect.collidepoint(mousePos)

                            if self.shopOptions['Back'].rect.collidepoint(mousePos):
                                self.gameStates['shop'] = False
                                self.gameStates['main'] = True

                            elif self.shopOptions['Attack'].rect.collidepoint(mousePos):
                                if self.upgrades['Attack'] < 4:
                                    self.upgrades['Attack']+= 1

                            elif self.shopOptions['Infection'].rect.collidepoint(mousePos):
                                if self.upgrades['Infection'] < 4:
                                    self.upgrades['Infection'] += 1

                            elif self.shopOptions['SP'].rect.collidepoint(mousePos):
                                  if self.upgrades['SP'] < 4:
                                    self.upgrades['SP']+= 1
                        
                        
            if self.gameStates['itemReward']:
                # Changes the background when the item reward screen starts.
                print('Got reward')

                # Need for creating the typing animation for the text box.
                dt = clock.tick(60) / 1  

                # Writes the intermiision dialogue with the typing animation.
                self.itemReward['reward'].update(dt) # Adds next character from text
                self.drawMenu(self.intermission)
                self.drawMenu(self.itemReward)

            


            if self.gameStates['main']:

                # Get mouse position for hover effect on buttons.
                mousePos = pygame.mouse.get_pos()
                for button in self.mainMenuOptions.values():
                    button.isHovered = button.rect.collidepoint(mousePos)


                self.screen.blit((self.assets['titleBackground']), (0,0))
                # Draws the Main Menu when the game is in the main menu state.
                self.drawMenu(self.mainMenuOptions)

            # Draws the Shop Menu when the game is in the shop state.
            elif self.gameStates['shop']:
                self.screen.blit(self.assets['shopBackground'], (0, 0))
                self.drawMenu(self.shopOptions)

            
            elif self.gameStates['Start']:
                # Changes the background when the intro exposition starts.
                self.screen.fill((0,0,0))

                dt = clock.tick(60) / 1  # Time in seconds since last frame

                # Writes the introduction exposition with the typing animation.
                self.startingText['Intro'].update(dt) # Adds next character from text
                self.drawMenu(self.startingText)  # Draw the text box

                for event in pygame.event.get():

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # If the text is not finsihed typing, 
                            # and the user clicks the screen, skip the typing animation.
                            if self.startingText['Intro'].isTyping():
                                self.startingText['Intro'].skipTyping()

                            # If the text is finished typing, performs an
                            # additional click which will exist the 
                            # exposition.
                            else:
                                self.gameStates['Start'] = False
                                self.gameStates['intermission'] = True
            
            # Needed for creating hover effect on the buttons in the shop menu
            # and for adding functionality to the upgrade buttons.
            if self.gameStates['shop']:
                mousePos = pygame.mouse.get_pos()
                for button in self.shopOptions.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

            if self.gameStates['intermission']:
                
                # Get mouse position for hover effect on buttons.
                mousePos = pygame.mouse.get_pos()
                for button in self.intermission.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

                
                # Draws the intermission background and the buttons within the 
                # intermission screen.
                self.screen.blit(self.assets['intermission'], (0, 0))
                self.drawMenu(self.intermission)


            # Display the screen
            pygame.display.flip()

            # Limit the frame rate to 60 FPS
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()




