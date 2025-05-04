import os
import pygame 
import math
import random
from settings import *
from player import Player
from bullet import Bullet
from saucer import Saucer
from asteroid import Asteroid
from player import deadPlayer


# Const variables
WINDOW_HEIGHT = 1280
WINDOW_WIDTH = 768
FONT = pygame.font.SysFont("arial", 30)
WINDOW_BACKGROUND_COLOR = pygame.Color('black')
# Colors 
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
light_sky_blue = (36, 179, 227)
dodger_blue = (15, 26, 184)

# Imported from old settings.py
player_size = 10
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20
player_max_rtspd = 10
bullet_speed = 15
saucer_speed = 5
small_saucer_accuracy = 10

gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids")
timer = pygame.time.Clock()

# Import sound effects
snd_fire = pygame.mixer.Sound("assets/fire.wav")
snd_bangL = pygame.mixer.Sound("assets/bangLarge.wav")
snd_bangM = pygame.mixer.Sound("assets/bangMedium.wav")
snd_bangS = pygame.mixer.Sound("assets/bangSmall.wav")
snd_extra = pygame.mixer.Sound("assets/extra.wav")
snd_saucerB = pygame.mixer.Sound("assets/saucerBig.wav")
snd_saucerS = pygame.mixer.Sound("assets/saucerSmall.wav")


rect_width = 500
rect_height = 100
center = WINDOW_WIDTH / 2 


banner_x = center + 250
banner_y = 200
banner_image_load = "assets/asteroids.svg"
banner_pos = (banner_x, banner_y)

# Play button
play_button_x = center
play_button_y = 400
play_button_color = "white"
play_button_foreground = "black"

# Quit button
quit_button_x = center
quit_button_y = rect_width + 10
quit_button_color = "white"
quit_button_foreground = "black"

# Singleplayer button
singleplayer_button_x = center
singleplayer_button_y = 400
single_player_button_color = "white"
single_player_button_foreground = "black"

# 2 Players same PC
same_pc_button_x = center
same_pc_button_y = rect_width + 10
same_pc_button_color = "white"
same_pc_button_foreground = "black"

# IP TextBox
ip_textbox_x = center
ip_textbox_y = 400
ip_textbox_color = "white"
ip_textbox_foreground = "black"

class Button:
    def __init__(self, text, x, y, color, foreground, screen):
        # Top rectangle
        self.top_rect = pygame.Rect((x, y), (rect_width, rect_height))
        self.top_color = color

        # Text
        self.text = text
        self.text_surf = FONT.render(text, True, foreground)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.screen = screen

    def draw(self, surface):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect)
        surface.blit(self.text_surf, self.text_rect)

class Banner:
    def __init__(self, banner_image_load):
        self.image = pygame.image.load(banner_image_load).convert_alpha()
        self.rect = self.image.get_rect(center=(banner_x, banner_y))

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)  # Draw a black rectangle behind the image
        surface.blit(self.image, self.rect.topleft)

class TextBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks inside the text box, activate it
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False  # Deactivate if clicked outside
            # Change color based on active state
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:  # Only process keys if the box is active
                if event.key == pygame.K_RETURN:
                    #print(self.text)  # Submit text on Enter
                    ip_address = self.text
                    print(f"Player entered ip address {ip_address}")
                    print("Connecting to server")
                    gameState = "Connect To Server"
                    
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Remove last character
                else:
                    self.text += event.unicode  # Add typed character
                # Re-render the text
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
