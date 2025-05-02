# Programa principal
import random 
import pygame 
import time

# (Temp) Global variables
FONT = 'arial'
WINDOW_HEIGHT = 1280
WINDOW_WIDTH = 800
running = True

# Buttons
# The first screen the user sees has a play button and a quit button.
# If the user presses play, it brings him to the second screen which has a singleplayer button and 
# a multiplayer button. 

# All rectangles are going to be the same shape and size so we can make them universal values
rect_width = 0
rect_height = 0

# Play button
play_button_x = 0
play_button_y = 0

# Quit button
quit_button_x = 0
quit_button_y = 0

# Singleplayer button
singleplayer_button_x = 0
singleplayer_button_y = 0

# Multiplayer button 
multiplayer_button_x = 0
multiplayer_button_y = 0

# Load font 
pygame.font.init()
font = pygame.font.SysFont(FONT, 30, bold=True)

# Start menu. 
class Button:
    def __init__(self, text, width, height, position):
        # Top rectangle
        self.top_rect = pygame.Rect(position, (width, height))
        self.top_color = '#000000'
        
        # Text 
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

play_button = Button("Play", play_button_x, play_button_y, (200, 200))

# There is a phase counter that changes depending.  
# The program evaluates what phase it is and changes accordingly 
phases = ["Inicial page", "Game selector", "Multiplayer", "SinglePlayer", "Ask for ip"]
current_phase = phases[0]  

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # < -------- START MENU SCREEN -------- >
        # If the user clicks the mouse, check if it clicked on any of the buttons 
        # and activate the phase requested. 
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check for play button in the inicial page phase
            if (
                (current_phase == "Inicial page")
                (play_button_x <= mouse_x <= play_button_x + rect_width)
                (play_button_y <= mouse_y <= play_button_y + rect_height)
            ):
            # Go into game selector phase 
                current_phase = phases[1]
            
            # Check for quit button
            if (
                (current_phase == phases[0])
                (quit_button_x <= mouse_x <= quit_button_x + rect_width)
                (quit_button_y <= mouse_y <= quit_button_y + rect_height)
            ): 
                # Quit game 
                running = False

            # Check for multiplayer button
            if (
                (current_phase == "Game Selector")
                (multiplayer_button_x <= mouse_x <= multiplayer_button_x + rect_width)
                (multiplayer_button_y <= mouse_y <= multiplayer_button_y + rect_height)
            ):
                current_phase = phases[2]

            # Check for singleplayer button
            if (
                (current_phase == "Game Selector")
                (singleplayer_button_x <= mouse_x <= singleplayer_button_x + rect_width)
                (singleplayer_button_y <= mouse_y <= singleplayer_button_y + rect_height)
            ):
                current_phase = phases[3]

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    
    clock.tick(60)  # limits FPS to 60

pygame.quit()