# Programa principal
import random 
import pygame 


# (Temp) Global variables
FONT = 'arial'
WINDOW_HEIGHT = 1280
WINDOW_WIDTH = 768

# Colors 
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

running = True

# Buttons
# The first screen the user sees has a play button and a quit button.
# If the user presses play, it brings him to the second screen which has a singleplayer button and 
# a multiplayer button. 

# All rectangles are going to be the same shape and size so we can make them universal values
rect_width = 100
rect_height = 100

# Play button
play_button_x = 100
play_button_y = 100
play_button_color = "white"
play_button_foreground = "black"

# Quit button
quit_button_x = 0
quit_button_y = 0
quit_button_color = "white"
quit_button_foreground = "black"

# Singleplayer button
singleplayer_button_x = 0
singleplayer_button_y = 0
single_player_button_color = "white"
single_player_button_foreground = "black"

# Multiplayer button 
multiplayer_button_x = 0
multiplayer_button_y = 0
multiplayer_button_color = "white"
multiplayer_button_foreground = "black"

# Load font 
pygame.font.init()
font = pygame.font.SysFont(FONT, 30, bold=True)

# Start menu. 
class Button:
    def __init__(self, text, width, height, position, color, foreground):
        # Top rectangle
        self.top_rect = pygame.Rect(position, (width, height))
        self.top_color = "black"
        
        # Text 
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect)

class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
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
    

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()


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
            if current_phase == "Inicial page" and play_button_x <= mouse_x <= play_button_x + rect_width and play_button_y <= mouse_y <= play_button_y + rect_height:
            # Go into game selector phase 
                current_phase = phases[1]
            
            # Check for quit button
            if (
                (current_phase == phases[0] and 
                quit_button_x <= mouse_x <= quit_button_x + rect_width and 
                quit_button_y <= mouse_y <= quit_button_y + rect_height)
            ): 
                # Quit game 
                running = False

            # Check for multiplayer button
            if (
                (current_phase == "Game Selector" and 
                multiplayer_button_x <= mouse_x <= multiplayer_button_x + rect_width and 
                multiplayer_button_y <= mouse_y <= multiplayer_button_y + rect_height)
            ):
                current_phase = phases[2]

            # Check for singleplayer button
            if (
                (current_phase == "Game Selector" and 
                singleplayer_button_x <= mouse_x <= singleplayer_button_x + rect_width and 
                singleplayer_button_y <= mouse_y <= singleplayer_button_y + rect_height)
            ):
                current_phase = phases[3]

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    # If statement block to represent each phase
    # Show [PLAY] and [QUIT] 
    if current_phase == phases[0]: 
        play_button = Button("PLAY", play_button_x, play_button_y, (rect_width, rect_height))
        quit_button = Button("QUIT", quit_button_x, quit_button_y, (rect_width, rect_height))
        play_button.draw()

    elif current_phase == phases[1]:
        single_player_button = Button("SINGLEPLAYER", singleplayer_button_x, singleplayer_button_y, (rect_width, rect_height))
        multiplayer_button = Button("MULTIPLAYER", multiplayer_button_x, multiplayer_button_y, (rect_width, rect_height))

    # Spawn a TextBox asking the player for an IP address to join a multiplayer session 
    elif current_phase == phases[4]:
        TextBox1 = TextBox()
        TextBox1.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    
    clock.tick(60)  # limits FPS to 60

pygame.quit()