import pygame
import socket
import threading
import json
from settings import *
from player import Player
from bullet import Bullet
from asteroid import Asteroid

gray = (103, 105, 128)


class MultiplayerClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.client_socket = None
        self.connected = False
        self.player_id = None
        self.players = {}
        self.bullets = []
        self.asteroids = []
        self.game_state = "Connecting"
        
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, 5555))
            self.connected = True
            threading.Thread(target=self.receive_data, daemon=True).start()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def receive_data(self):
        while self.connected:
            try:
                data = self.client_socket.recv(4096).decode()
                if not data:
                    break
                    
                messages = data.split('|')
                for msg in messages:
                    if msg:
                        self.handle_server_message(json.loads(msg))
            except Exception as e:
                print(f"Receive error: {e}")
                self.connected = False
                break
    
    def handle_server_message(self, data):
        if data['type'] == 'init':
            self.player_id = data['player_id']
            self.game_state = "Playing"
        elif data['type'] == 'game_state':
            self.players = data['players']
            self.bullets = data['bullets']
            self.asteroids = data['asteroids']
    
    def send_input(self, inputs):
        if self.connected:
            try:
                message = json.dumps({
                    'type': 'player_input',
                    'player_id': self.player_id,
                    'inputs': inputs
                })
                self.client_socket.send(message.encode())
            except Exception as e:
                print(f"Send error: {e}")
                self.connected = False

def JoinMultiplayerSession(ip):
    client = MultiplayerClient(ip)
    if not client.connect():
        return "Connection Failed"
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
    # Game loop
    running = True
    while running:
        # Handle events
        inputs = {
            'thrust': False,
            'left': False,
            'right': False,
            'fire': False
        }
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    inputs['thrust'] = True
                if event.key == pygame.K_LEFT:
                    inputs['left'] = True
                if event.key == pygame.K_RIGHT:
                    inputs['right'] = True
                if event.key == pygame.K_SPACE:
                    inputs['fire'] = True
        
        # Send inputs to server
        client.send_input(inputs)
        
        # Draw game state
        screen.fill(black)
        
        if client.game_state == "Playing":
            # Draw players
            for player_id, player_data in client.players.items():
                color = red if player_id == client.player_id else blue
                Player(player_data['x'], player_data['y'], color, player_data['dir']).drawPlayer(screen)
            
            # Draw bullets
            for bullet in client.bullets:
                pygame.draw.circle(screen, white, (bullet['x'], bullet['y']), 3)
            
            # Draw asteroids
            for asteroid in client.asteroids:
                pygame.draw.circle(screen, gray, (asteroid['x'], asteroid['y']), asteroid['size'])
        
        elif client.game_state == "Connecting":
            font = pygame.font.SysFont("Arial", 30)
            text = font.render("Connecting to server...", True, white)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    return "Game Selector"