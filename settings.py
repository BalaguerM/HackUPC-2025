import pygame

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

display_width = 800
display_height = 600

player_size = 10
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20
player_max_rtspd = 10
bullet_speed = 15
saucer_speed = 5
small_saucer_accuracy = 10

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Asteroids")
timer = pygame.time.Clock()

# Import sound effects
snd_fire = pygame.mixer.Sound("sfx/fire.wav")
snd_bangL = pygame.mixer.Sound("sfx/bangLarge.wav")
snd_bangM = pygame.mixer.Sound("sfx/bangMedium.wav")
snd_bangS = pygame.mixer.Sound("sfx/bangSmall.wav")
snd_extra = pygame.mixer.Sound("sfx/extra.wav")
snd_saucerB = pygame.mixer.Sound("sfx/saucerBig.wav")
snd_saucerS = pygame.mixer.Sound("sfx/saucerSmall.wav")