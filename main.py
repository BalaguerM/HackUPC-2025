import os
import pygame 
from settings import *
from variables import *

import single_player
import same_pc

FONT = pygame.font.SysFont("arial", 30)
WINDOW_BACKGROUND_COLOR = pygame.Color('black')
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
running = True

# Load the image (replace with your image file path)
background = pygame.image.load("assets/bg2.png").convert()

# Scale the image to fit the screen if needed
background = pygame.transform.scale(background, (WINDOW_HEIGHT, WINDOW_WIDTH))

# Load font 
pygame.font.init()

# Set window position before initialization
os.environ['SDL_VIDEO_CENTERED'] = '0'  # This centers the window

# Initializing pygame and setting the screen
pygame.init()
screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
clock = pygame.time.Clock()

gameState = "Inicial Page"

banner = Banner(banner_image_load)

def button_clicked(button_x, button_y):
    if (button_x <= mouse_x <= button_x + rect_width and button_y <= mouse_y <= button_y + rect_height):
        return True
    else:
        return False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse clicks for all states
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if gameState == "Inicial Page":
                if button_clicked(play_button_x, play_button_y):
                    gameState = "Game Selector"
                elif (button_clicked(quit_button_x, quit_button_y)):
                    running = False

            elif gameState == "Game Selector":
                if button_clicked(singleplayer_button_x, singleplayer_button_y):
                    gameState = "Single Player"
                elif button_clicked(same_pc_button_x, same_pc_button_y):
                    gameState = "Same PC"
        
    # Rendering
    #screen.fill(WINDOW_BACKGROUND_COLOR)
    screen.blit(background, (0,0))

    if gameState == "Inicial Page": 
        play_button = Button("PLAY", play_button_x, play_button_y, play_button_color, play_button_foreground, screen)
        quit_button = Button("QUIT", quit_button_x, quit_button_y, quit_button_color, quit_button_foreground, screen)
        play_button.draw(screen)
        quit_button.draw(screen)
        banner.draw(screen)

    elif gameState == "Game Selector":
        single_player_button = Button("SINGLEPLAYER", singleplayer_button_x, singleplayer_button_y, single_player_button_color, single_player_button_foreground, screen)
        same_pc_button = Button("2 PLAYERS SAME PC", same_pc_button_x, same_pc_button_y, same_pc_button_color, same_pc_button_foreground, screen)
        single_player_button.draw(screen)
        same_pc_button.draw(screen)
        banner.draw(screen)

    elif gameState == "Single Player":
        single_player.SinglePlayerGameLoop(gameState)
    
    elif gameState == "Same PC":
        same_pc.SamePc("Playing")
    
    elif gameState == "Connect To Server":
        screen.fill(white)
        pass

    pygame.display.flip()
    clock.tick(60)
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    
    clock.tick(60)  # limits FPS to 60

pygame.quit()