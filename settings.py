import pygame

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 768

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