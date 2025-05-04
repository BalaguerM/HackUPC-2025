import pygame 
import math
import random
from settings import *
from player import Player
from bullet import Bullet
from saucer import Saucer
from asteroid import Asteroid
from player import deadPlayer

def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else:
        rect = (x, y)
    gameDisplay.blit(screen_text, rect)

def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False

def SamePc(startingState):
    # Init variables
    gameState = startingState
    player_red_state = "Alive"
    player_blue_state = "Alive"
    player_red_blink = 0
    player_blue_blink = 0
    player_red_pieces = []
    player_blue_pieces = []
    player_red_dying_delay = 0
    player_blue_dying_delay = 0
    player_red_invi_dur = 0
    player_blue_invi_dur = 0
    player_red_lives = 3
    player_blue_lives = 3

    hyperspace = 0
    next_level_delay = 0
    bullet_capacity = 4
    bullets = []
    asteroids = []
    stage = 3
    score = 0
    oneUp_multiplier = 1
    playOneUpSFX = 0
    intensity = 0
    player_red = Player(WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2, red)
    player_blue = Player(WINDOW_WIDTH * 2/3, WINDOW_HEIGHT / 2, blue)
    saucer = Saucer()

    # Main loop
    while gameState != "Exit":
        # User inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                # Player Red controls
                if event.key == pygame.K_UP:
                    player_red.thrust = True
                if event.key == pygame.K_LEFT:
                    player_red.rtspd = -player_max_rtspd
                if event.key == pygame.K_RIGHT:
                    player_red.rtspd = player_max_rtspd
                if event.key == pygame.K_SPACE and player_red_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(player_red.x, player_red.y, player_red.dir))
                    pygame.mixer.Sound.play(snd_fire)
                
                # Player Blue controls
                if event.key == pygame.K_w:
                    player_blue.thrust = True
                if event.key == pygame.K_a:
                    player_blue.rtspd = -player_max_rtspd
                if event.key == pygame.K_d:
                    player_blue.rtspd = player_max_rtspd
                if event.key == pygame.K_f and player_blue_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(player_blue.x, player_blue.y, player_blue.dir))
                    pygame.mixer.Sound.play(snd_fire)

                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        SamePc("Playing")
                if event.key == pygame.K_LSHIFT:
                    hyperspace = 30
            
            if event.type == pygame.KEYUP:
                # Player Red controls
                if event.key == pygame.K_UP:
                    player_red.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_red.rtspd = 0
                
                # Player Blue controls
                if event.key == pygame.K_w:
                    player_blue.thrust = False
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_blue.rtspd = 0

        # Update players
        player_red.updatePlayer()
        player_blue.updatePlayer()

        # Checking players invincible time
        if player_red_invi_dur != 0:
            player_red_invi_dur -= 1
        elif hyperspace == 0:
            player_red_state = "Alive"

        if player_blue_invi_dur != 0:
            player_blue_invi_dur -= 1
        elif hyperspace == 0:
            player_blue_state = "Alive"

        # Reset display
        gameDisplay.fill(black)

        # Hyperspace
        if hyperspace != 0:
            player_red_state = "Died"
            player_blue_state = "Died"
            hyperspace -= 1
            if hyperspace == 1:
                player_red.x = random.randrange(0, WINDOW_WIDTH)
                player_red.y = random.randrange(0, WINDOW_HEIGHT)
                player_blue.x = random.randrange(0, WINDOW_WIDTH)
                player_blue.y = random.randrange(0, WINDOW_HEIGHT)

        # Check for collision w/ asteroid
        for a in asteroids:
            a.updateAsteroid()
            
            # Player Red collision
            if player_red_state != "Died":
                if isColliding(player_red.x, player_red.y, a.x, a.y, a.size):
                    player_red_pieces.append(deadPlayer(player_red.x, player_red.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_red_pieces.append(deadPlayer(player_red.x, player_red.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_red_pieces.append(deadPlayer(player_red.x, player_red.y, player_size))
                    
                    player_red_state = "Died"
                    player_red_dying_delay = 30
                    player_red_invi_dur = 120
                    player_red.killPlayer()

                    if player_red_lives != 0:
                        player_red_lives -= 1
                    else:
                        gameState = "Game Over"

                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)
            
            # Player Blue collision
            if player_blue_state != "Died":
                if isColliding(player_blue.x, player_blue.y, a.x, a.y, a.size):
                    player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, player_size))
                    
                    player_blue_state = "Died"
                    player_blue_dying_delay = 30
                    player_blue_invi_dur = 120
                    player_blue.killPlayer()

                    if player_blue_lives != 0:
                        player_blue_lives -= 1
                    else:
                        gameState = "Game Over"

                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

        # Update ship fragments
        for f in player_red_pieces:
            f.updateDeadPlayer()
            if f.x > WINDOW_WIDTH or f.x < 0 or f.y > WINDOW_HEIGHT or f.y < 0:
                player_red_pieces.remove(f)

        for f in player_blue_pieces:
            f.updateDeadPlayer()
            if f.x > WINDOW_WIDTH or f.x < 0 or f.y > WINDOW_HEIGHT or f.y < 0:
                player_blue_pieces.remove(f)

        # Check for end of stage
        if len(asteroids) == 0 and saucer.state == "Dead":
            if next_level_delay < 30:
                next_level_delay += 1
            else:
                stage += 1
                intensity = 0
                for i in range(stage):
                    xTo = WINDOW_WIDTH / 2
                    yTo = WINDOW_HEIGHT / 2
                    while xTo - WINDOW_WIDTH / 2 < WINDOW_WIDTH / 4 and yTo - WINDOW_HEIGHT / 2 < WINDOW_HEIGHT / 4:
                        xTo = random.randrange(0, WINDOW_WIDTH)
                        yTo = random.randrange(0, WINDOW_HEIGHT)
                    asteroids.append(Asteroid(xTo, yTo, "Large"))
                next_level_delay = 0

        # Update intensity
        if intensity < stage * 450:
            intensity += 1

        # Saucer
        if saucer.state == "Dead":
            if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and next_level_delay == 0:
                saucer.createSaucer()
                if score >= 40000:
                    saucer.type = "Small"
        else:
            # Set saucer target dir (choose randomly between players)
            target_player = random.choice([player_red, player_blue])
            acc = small_saucer_accuracy * 4 / stage
            saucer.bdir = math.degrees(math.atan2(-saucer.y + target_player.y, -saucer.x + target_player.x) + math.radians(random.uniform(acc, -acc)))

            saucer.updateSaucer()
            saucer.drawSaucer()

            # Check for collision w/ asteroid
            for a in asteroids:
                if isColliding(saucer.x, saucer.y, a.x, a.y, a.size + saucer.size):
                    saucer.state = "Dead"

                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

            # Check for collision w/ bullet
            for b in bullets:
                if isColliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                    if saucer.type == "Large":
                        score += 200
                    else:
                        score += 1000

                    saucer.state = "Dead"
                    pygame.mixer.Sound.play(snd_bangL)
                    bullets.remove(b)

            # Check collision w/ players
            if isColliding(saucer.x, saucer.y, player_red.x, player_red.y, saucer.size):
                if player_red_state != "Died":
                    player_red_pieces.append(deadPlayer(player_red.x, player_red.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_red_pieces.append(deadPlayer(player_red.x, player_red.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_red_pieces.append(deadPlayer(player_red.x, player_red.y, player_size))

                    player_red_state = "Died"
                    player_red_dying_delay = 30
                    player_red_invi_dur = 120
                    player_red.killPlayer()

                    if player_red_lives != 0:
                        player_red_lives -= 1
                    else:
                        gameState = "Game Over"

                    pygame.mixer.Sound.play(snd_bangL)

            if isColliding(saucer.x, saucer.y, player_blue.x, player_blue.y, saucer.size):
                if player_blue_state != "Died":
                    player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, player_size))

                    player_blue_state = "Died"
                    player_blue_dying_delay = 30
                    player_blue_invi_dur = 120
                    player_blue.killPlayer()

                    if player_blue_lives != 0:
                        player_blue_lives -= 1
                    else:
                        gameState = "Game Over"

                    pygame.mixer.Sound.play(snd_bangL)

            # Saucer's bullets
            for b in saucer.bullets:
                b.updateBullet()

                # Check for collision w/ asteroids
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            pygame.mixer.Sound.play(snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            pygame.mixer.Sound.play(snd_bangL)
                        else:
                            pygame.mixer.Sound.play(snd_bangL)

                        asteroids.remove(a)
                        saucer.bullets.remove(b)
                        break

                # Check for collision w/ players
                if isColliding(player_red.x, player_red.y, b.x, b.y, 5):
                    if player_red_state != "Died":
                        player_red_pieces.append(deadPlayer(player_red.x, player_red.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_red_pieces.append(deadPlayer(player_red.x, player_red.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_red_pieces.append(deadPlayer(player_red.x, player_red.y, player_size))

                        player_red_state = "Died"
                        player_red_dying_delay = 30
                        player_red_invi_dur = 120
                        player_red.killPlayer()

                        if player_red_lives != 0:
                            player_red_lives -= 1
                        else:
                            gameState = "Game Over"

                        pygame.mixer.Sound.play(snd_bangL)
                        saucer.bullets.remove(b)

                if isColliding(player_blue.x, player_blue.y, b.x, b.y, 5):
                    if player_blue_state != "Died":
                        player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_blue_pieces.append(deadPlayer(player_blue.x, player_blue.y, player_size))

                        player_blue_state = "Died"
                        player_blue_dying_delay = 30
                        player_blue_invi_dur = 120
                        player_blue.killPlayer()

                        if player_blue_lives != 0:
                            player_blue_lives -= 1
                        else:
                            gameState = "Game Over"

                        pygame.mixer.Sound.play(snd_bangL)
                        saucer.bullets.remove(b)

                if b.life <= 0:
                    try:
                        saucer.bullets.remove(b)
                    except ValueError:
                        continue

        # Bullets
        for b in bullets:
            b.updateBullet()

            # Check for bullets collide w/ asteroid
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
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

        # Extra lives
        if score > oneUp_multiplier * 10000:
            oneUp_multiplier += 1
            player_red_lives += 1
            player_blue_lives += 1
            playOneUpSFX = 60
        
        # Play sfx
        if playOneUpSFX > 0:
            playOneUpSFX -= 1
            pygame.mixer.Sound.play(snd_extra, 60)

        # Draw players
        if gameState != "Game Over":
            # Draw player_red
            if player_red_state == "Died":
                if hyperspace == 0:
                    if player_red_dying_delay == 0:
                        if player_red_blink < 5:
                            if player_red_blink == 0:
                                player_red_blink = 10
                            else:
                                player_red.drawPlayer()
                        player_red_blink -= 1
                    else:
                        player_red_dying_delay -= 1
            else:
                player_red.drawPlayer()
            
            # Draw player_blue
            if player_blue_state == "Died":
                if hyperspace == 0:
                    if player_blue_dying_delay == 0:
                        if player_blue_blink < 5:
                            if player_blue_blink == 0:
                                player_blue_blink = 10
                            else:
                                player_blue.drawPlayer()
                        player_blue_blink -= 1
                    else:
                        player_blue_dying_delay -= 1
            else:
                player_blue.drawPlayer()
        else:
            drawText("Game Over", white, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 100)
            drawText("Press \"R\" to restart!", white, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100, 50)

        # Draw score
        drawText(str(score), white, 60, 20, 40, False)

        # Draw Lives - Red player on left, Blue player on right
        for l in range(player_red_lives):
            Player(75 + l * 25, 75, red).drawPlayer()
        for l in range(player_blue_lives):
            Player(WINDOW_WIDTH - 75 - l * 25, 75, blue).drawPlayer()

        # Update screen
        pygame.display.update()

        # Tick fps
        timer.tick(30)
                    
