# Programa principal
import random 
import pygame 

# Load font 
font = pygame.font.SysFont('Arial', 30, bold=True)

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
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    
    # Generate the start menu and give the user the option to play or to quit
    Button("Play", 500, 100, 300)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()