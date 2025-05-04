from variables import * 


pygame.init()
screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
running = True

# Load the image (replace with your image file path)
background = pygame.image.load("assets/bg2.png").convert()

# Scale the image to fit the screen if needed
background = pygame.transform.scale(background, (WINDOW_HEIGHT, WINDOW_WIDTH))

while running:

    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    screen.fill(white)