import socket
import threading
import json
import random
from asteroid import Asteroid
from variables import *

class GameServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 5555))
        self.server_socket.listen()
        
        self.players = {}
        self.bullets = []
        self.asteroids = []
        self.player_counter = 0
        
        # Initialize asteroids
        for _ in range(5):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.asteroids.append(Asteroid(x, y, "Large"))
    
    def handle_client(self, client_socket, player_id):
        while True:
            try:
                data = client_socket.recv(4096).decode()
                if not data:
                    break
                    
                # Process player input
                inputs = json.loads(data)['inputs']
                if player_id in self.players:
                    player = self.players[player_id]
                    if inputs['left']:
                        player['dir'] -= 5
                    if inputs['right']:
                        player['dir'] += 5
                    if inputs['thrust']:
                        player['x'] += math.cos(math.radians(player['dir'])) * 5
                        player['y'] -= math.sin(math.radians(player['dir'])) * 5
                    if inputs['fire']:
                        self.bullets.append({
                            'x': player['x'],
                            'y': player['y'],
                            'dir': player['dir'],
                            'life': 60
                        })
                
                # Send game state
                game_state = {
                    'type': 'game_state',
                    'players': self.players,
                    'bullets': self.bullets,
                    'asteroids': [a.__dict__ for a in self.asteroids]
                }
                client_socket.send(json.dumps(game_state).encode())
                
            except Exception as e:
                print(f"Error with player {player_id}: {e}")
                break
        
        # Remove disconnected player
        if player_id in self.players:
            del self.players[player_id]
        client_socket.close()
    
    def update_game(self):
        # Update bullets
        for bullet in self.bullets[:]:
            bullet['life'] -= 1
            if bullet['life'] <= 0:
                self.bullets.remove(bullet)
            else:
                bullet['x'] += math.cos(math.radians(bullet['dir'])) * 10
                bullet['y'] -= math.sin(math.radians(bullet['dir'])) * 10
    
    def run(self):
        print("Server started. Waiting for connections...")
        threading.Thread(target=self.update_game, daemon=True).start()
        
        while True:
            client_socket, addr = self.server_socket.accept()
            self.player_counter += 1
            player_id = self.player_counter
            
            # Initialize new player
            x = WINDOW_WIDTH / 2 if player_id % 2 == 0 else WINDOW_WIDTH / 3
            y = WINDOW_HEIGHT / 2
            self.players[player_id] = {
                'x': x,
                'y': y,
                'dir': 0
            }
            
            # Send initial data
            init_data = {
                'type': 'init',
                'player_id': player_id
            }
            client_socket.send(json.dumps(init_data).encode())
            
            # Start client thread
            threading.Thread(
                target=self.handle_client,
                args=(client_socket, player_id)
            ).start()

if __name__ == "__main__":
    server = GameServer()
    server.run()