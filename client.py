import socket
import pickle
import pygame
from gamedata import *
import comm

class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def input_addr(self):
        server_ip = input("Enter server IP: ")
        server_port = input("Enter server port: ")
        self.addr = (server_ip, int(server_port))

    def connect(self):
        try:
            self.socket.connect(self.addr)
        except:
            print('Connection failed')
            pass

class Game():
    def __init__(self, client):
        pygame.init()

        self.camera = (500, 500)
        self.board = (1000, 1000)
        self.client = client
        self.window = pygame.display.set_mode(self.camera)

    def render_bounds(self, head):
        if head.position[0] + self.camera[0]/2 > self.board[0]:
            off_map_width = (head.position[0] + self.camera[0]/2 - self.board[0])
            off_map_rect = (self.camera[0] - off_map_width, 0, off_map_width, self.camera[1])
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)
        elif head.position[0] - self.camera[0]/2 < 0:
            off_map_width = -(head.position[0] - self.camera[0]/2)
            off_map_rect = (0, 0, off_map_width, self.camera[1])
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)
        if head.position[1] + self.camera[1]/2 > self.board[1]:
            off_map_width = (head.position[1] + self.camera[1]/2 - self.board[1])
            off_map_rect = (0, self.camera[0] - off_map_width, self.camera[0], off_map_width)
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)
        elif head.position[1] - self.camera[1]/2 < 0:
            off_map_width = -(head.position[1] - self.camera[1]/2)
            off_map_rect = (0, 0, self.camera[0], off_map_width)
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)

    def render(self, game_data):
        snakes = game_data.snakes
        pellets = game_data.pellets

        self.window.fill((0, 0, 0))
        my_head = game_data.snake[0]

        self.render_bounds(my_head)
    
        head_rect = (self.camera[0] / 2, self.camera[1] / 2, my_head.width - 2, my_head.width - 2)
        pygame.draw.rect(self.window, my_head.color, head_rect)

        game_objects = game_data.snake[1:]
        for snake in snakes:
            for body_part in snake:
                game_objects.append(body_part)
        for pellet in pellets:
            game_objects.append(pellet)
        
        for object in game_objects:
            left = head_rect[0] + object.position[0] - my_head.position[0]
            top = head_rect[1] + object.position[1] - my_head.position[1]
            rect = (left, top, object.width - 2, object.width - 2)
            pygame.draw.rect(self.window, object.color, rect);

        #snakes.append(game_data.snake)
        #for snake in snakes:
        #    for body_part in snake:
        #        rect = (body_part.position[0], body_part.position[1], body_part.width - 2, body_part.width - 2)
        #        pygame.draw.rect(self.window, body_part.color, rect);
        #for pellet in pellets:
        #    rect = (pellet.position[0], pellet.position[1], pellet.width - 2, pellet.width - 2)
        #    pygame.draw.rect(self.window, pellet.color, rect);
        pygame.display.update()

    def get_direction(self):
        direction = None
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            direction = (-1, 0)
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            direction = (1, 0)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]):
            direction = (0, -1)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            direction = (0, 1)
        return direction

    def game_loop(self):
        self.running = True
        while self.running:
            msg = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    msg = pickle.dumps(comm.Signal.QUIT)
                    self.running = False
            
            # Send input or quit signal to server
            if msg == None:
                msg = pickle.dumps(self.get_direction())
            comm.send_data(self.client.socket, comm.size_as_bytes(msg))
            comm.send_data(self.client.socket, msg)

            # If the player decided to quit, exit the game loop after notifying server
            if not self.running: break
            
            # Receive game data from server, use it to render
            size_as_bytes = comm.receive_data(self.client.socket, comm.MSG_LEN)
            length = comm.size_as_int(size_as_bytes)
            game_data = pickle.loads(comm.receive_data(self.client.socket, length))
            self.render(game_data)
        pygame.quit()

def main():
    client = Client()
    client.input_addr()
    client.connect()
    game = Game(client)
    game.game_loop()

if __name__ == "__main__":
    main()
