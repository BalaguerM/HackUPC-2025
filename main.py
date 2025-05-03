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


# (Temp) Global variables
WINDOW_HEIGHT = 1280
WINDOW_WIDTH = 768
FONT = pygame.font.SysFont("arial", 30)

WINDOW_BACKGROUND_COLOR = pygame.Color('black')

# Colors 
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

running = True
ip_address = ""
# Buttons
# The first screen the user sees has a play button and a quit button.
# If the user presses play, it brings him to the second screen which has a singleplayer button and 
# a multiplayer button. 

# All rectangles are going to be the same shape and size so we can make them universal values
rect_width = 500
rect_height = 100

# Simple macro to find the center of the screen
center = WINDOW_WIDTH / 2 

# Banner that is present on all screens 
# Banner will be an imported image 
banner_x = center
banner_y = rect_width + 10
banner_image_path = ""

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

# Multiplayer button 
multiplayer_button_x = center
multiplayer_button_y = rect_width + 10
multiplayer_button_color = "white"
multiplayer_button_foreground = "black"

# 2 Players same PC
same_pc_button_x = center
same_pc_button_y = rect_width + 120
same_pc_button_color = "white"
same_pc_button_foreground = "black"

# IP TextBox
ip_textbox_x = center
ip_textbox_y = 400
ip_textbox_color = "white"
ip_textbox_foreground = "black"

# Load font 
pygame.font.init()


# Start menu. 
class Button:
    def __init__(self, text, x, y, color, foreground):
        # Top rectangle
        self.top_rect = pygame.Rect((x, y), (rect_width, rect_height))
        self.top_color = color
        
        # Text
        self.text = text
        self.text_surf = FONT.render(text, True, foreground)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self, surface):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        surface.blit(self.text_surf, self.text_rect)

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
                    print("Player entered ip address")
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


# Set window position before initialization
os.environ['SDL_VIDEO_CENTERED'] = '1'  # This centers the window

# Initializing pygame and setting the screen
pygame.init()
screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
clock = pygame.time.Clock()

# < -------- SINGLEPLAYER GAME -------- >
def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else:
        rect = (x, y)
    gameDisplay.blit(screen_text, rect)


# Create funtion to chek for collision
def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False

def SinglePlayerGameLoop(startingState):
    # Init variables
    gameState = startingState
    player_state = "Alive"
    player_blink = 0
    player_pieces = []
    player_dying_delay = 0
    player_invi_dur = 0
    hyperspace = 0
    next_level_delay = 0
    bullet_capacity = 4
    bullets = []
    asteroids = []
    stage = 3
    score = 0
    live = 2
    oneUp_multiplier = 1
    playOneUpSFX = 0
    intensity = 0
    player = Player(display_width / 2, display_height / 2)
    saucer = Saucer()

    # Main loop
    while gameState != "Exit":
        # User inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_LEFT:
                    player.rtspd = -player_max_rtspd
                if event.key == pygame.K_RIGHT:
                    player.rtspd = player_max_rtspd
                if event.key == pygame.K_SPACE and player_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(player.x, player.y, player.dir))
                    # Play SFX
                    pygame.mixer.Sound.play(snd_fire)
                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        SinglePlayerGameLoop("Playing")
                if event.key == pygame.K_LSHIFT:
                    hyperspace = 30
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.rtspd = 0

        # Update player
        player.updatePlayer()

        # Checking player invincible time
        if player_invi_dur != 0:
            player_invi_dur -= 1
        elif hyperspace == 0:
            player_state = "Alive"

        # Reset display
        gameDisplay.fill(black)

        # Hyperspace
        if hyperspace != 0:
            player_state = "Died"
            hyperspace -= 1
            if hyperspace == 1:
                player.x = random.randrange(0, display_width)
                player.y = random.randrange(0, display_height)

        # Check for collision w/ asteroid
        for a in asteroids:
            a.updateAsteroid()
            if player_state != "Died":
                if isColliding(player.x, player.y, a.x, a.y, a.size):
                    # Create ship fragments
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, player_size))
                    
                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

        # Update ship fragments
        for f in player_pieces:
            f.updateDeadPlayer()
            if f.x > display_width or f.x < 0 or f.y > display_height or f.y < 0:
                player_pieces.remove(f)

        # Check for end of stage
        if len(asteroids) == 0 and saucer.state == "Dead":
            if next_level_delay < 30:
                next_level_delay += 1
            else:
                stage += 1
                intensity = 0
                # Spawn asteroid away of center
                for i in range(stage):
                    xTo = display_width / 2
                    yTo = display_height / 2
                    while xTo - display_width / 2 < display_width / 4 and yTo - display_height / 2 < display_height / 4:
                        xTo = random.randrange(0, display_width)
                        yTo = random.randrange(0, display_height)
                    asteroids.append(Asteroid(xTo, yTo, "Large"))
                next_level_delay = 0

        # Update intensity
        if intensity < stage * 450:
            intensity += 1

        # Saucer
        if saucer.state == "Dead":
            if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and next_level_delay == 0:
                saucer.createSaucer()
                # Only small saucers >40000
                if score >= 40000:
                    saucer.type = "Small"
        else:
            # Set saucer targer dir
            acc = small_saucer_accuracy * 4 / stage
            saucer.bdir = math.degrees(math.atan2(-saucer.y + player.y, -saucer.x + player.x) + math.radians(random.uniform(acc, -acc)))

            saucer.updateSaucer()
            saucer.drawSaucer()

            # Check for collision w/ asteroid
            for a in asteroids:
                if isColliding(saucer.x, saucer.y, a.x, a.y, a.size + saucer.size):
                    # Set saucer state
                    saucer.state = "Dead"

                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

            # Check for collision w/ bullet
            for b in bullets:
                if isColliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                    # Add points
                    if saucer.type == "Large":
                        score += 200
                    else:
                        score += 1000

                    # Set saucer state
                    saucer.state = "Dead"

                    # Play SFX
                    pygame.mixer.Sound.play(snd_bangL)

                    # Remove bullet
                    bullets.remove(b)

            # Check collision w/ player
            if isColliding(saucer.x, saucer.y, player.x, player.y, saucer.size):
                if player_state != "Died":
                    # Create ship fragments
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, player_size))

                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    # Play SFX
                    pygame.mixer.Sound.play(snd_bangL)

            # Saucer's bullets
            for b in saucer.bullets:
                # Update bullets
                b.updateBullet()

                # Check for collision w/ asteroids
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangL)
                        else:
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangL)

                        # Remove asteroid and bullet
                        asteroids.remove(a)
                        saucer.bullets.remove(b)

                        break

                # Check for collision w/ player
                if isColliding(player.x, player.y, b.x, b.y, 5):
                    if player_state != "Died":
                        # Create ship fragments
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, player_size))

                        # Kill player
                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.killPlayer()

                        if live != 0:
                            live -= 1
                        else:
                            gameState = "Game Over"

                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)

                        # Remove bullet
                        saucer.bullets.remove(b)

                if b.life <= 0:
                    try:
                        saucer.bullets.remove(b)
                    except ValueError:
                        continue

        # Bullets
        for b in bullets:
            # Update bullets
            b.updateBullet()

            # Check for bullets collide w/ asteroid
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)
                    bullets.remove(b)

                    break

            # Destroying bullets
            if b.life <= 0:
                try:
                    bullets.remove(b)
                except ValueError:
                    continue

        # Extra live
        if score > oneUp_multiplier * 10000:
            oneUp_multiplier += 1
            live += 1
            playOneUpSFX = 60
        # Play sfx
        if playOneUpSFX > 0:
            playOneUpSFX -= 1
            pygame.mixer.Sound.play(snd_extra, 60)

        # Draw player
        if gameState != "Game Over":
            if player_state == "Died":
                if hyperspace == 0:
                    if player_dying_delay == 0:
                        if player_blink < 5:
                            if player_blink == 0:
                                player_blink = 10
                            else:
                                player.drawPlayer()
                        player_blink -= 1
                    else:
                        player_dying_delay -= 1
            else:
                player.drawPlayer()
        else:
            drawText("Game Over", white, display_width / 2, display_height / 2, 100)
            drawText("Press \"R\" to restart!", white, display_width / 2, display_height / 2 + 100, 50)
            live = -1

        # Draw score
        drawText(str(score), white, 60, 20, 40, False)

        # Draw Lives
        for l in range(live + 1):
            Player(75 + l * 25, 75).drawPlayer()

        # Update screen
        pygame.display.update()

        # Tick fps
        timer.tick(30)

# < -------- 2 PLAYERS SAME PC -------- >
def TwoPlayersSamePC():
    pass



# There is a phase counter that changes depending.  
# The program evaluates what phase it is and changes accordingly 
"""
# 1: Inicial Page
# 2: Game Selector
# 3: Multiplayer 
# 4: Single Player
# 5: Introduce ip 

"""
gameState = "Inicial Page"

# Initialize text box before the main loop
text_box = None

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse clicks for all states
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if gameState == "Inicial Page":
                if (play_button_x <= mouse_x <= play_button_x + rect_width and 
                    play_button_y <= mouse_y <= play_button_y + rect_height):
                    gameState = "Game Selector"
                elif (quit_button_x <= mouse_x <= quit_button_x + rect_width and 
                      quit_button_y <= mouse_y <= quit_button_y + rect_height):
                    running = False
            
            elif gameState == "Game Selector":
                if (multiplayer_button_x <= mouse_x <= multiplayer_button_x + rect_width and 
                    multiplayer_button_y <= mouse_y <= multiplayer_button_y + rect_height):
                    gameState = "Multiplayer"
                    text_box = TextBox(ip_textbox_x, ip_textbox_y, rect_width, rect_height)  # Create here
                elif (singleplayer_button_x <= mouse_x <= singleplayer_button_x + rect_width and 
                      singleplayer_button_y <= mouse_y <= singleplayer_button_y + rect_height):
                    gameState = "Single Player"
                elif (same_pc_button_x <= mouse_x <= same_pc_button_x + rect_width and
                      same_pc_button_y <= mouse_y <= same_pc_button_y + rect_height):
                    gameState = "Same PC"
        
        # Handle keyboard events for text box
        if gameState == "Multiplayer" and text_box is not None:
            text_box.handle_event(event)  # This is where we pass key events
    
    # Rendering
    screen.fill(WINDOW_BACKGROUND_COLOR)
    
    if gameState == "Inicial Page": 
        play_button = Button("PLAY", play_button_x, play_button_y, play_button_color, play_button_foreground)
        quit_button = Button("QUIT", quit_button_x, quit_button_y, quit_button_color, quit_button_foreground)
        play_button.draw(screen)
        quit_button.draw(screen)

    elif gameState == "Game Selector":
        single_player_button = Button("SINGLEPLAYER", singleplayer_button_x, singleplayer_button_y, single_player_button_color, single_player_button_foreground)
        multiplayer_button = Button("MULTIPLAYER", multiplayer_button_x, multiplayer_button_y, multiplayer_button_color, multiplayer_button_foreground)
        same_pc_button = Button("2 PLAYERS SAME PC", same_pc_button_x, same_pc_button_y, same_pc_button_color, same_pc_button_foreground)
        single_player_button.draw(screen)
        multiplayer_button.draw(screen)
        same_pc_button.draw(screen)
    
    elif gameState == "Single Player":
        SinglePlayerGameLoop(gameState)
    
    elif gameState == "Multiplayer":
        if text_box is not None:
            text_box.update()
            text_box.draw(screen)
    
    elif gameState == "Same PC":
        pass
    
    elif gameState == "Connect To Server":
        screen.fill("#FFFFFF")
        pass


    pygame.display.flip()
    clock.tick(60)
    
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    
    clock.tick(60)  # limits FPS to 60

pygame.quit()