import pickle
import socket
from pygame.time import Clock
from threading import Thread

from gamedata import *
import comm
from game import *

class Client():
    def __init__(self, socket, snake):
        self.socket = socket
        self.snake = snake
        self.received_input = False
        self.dead = False

class Server():
    def __init__(self):
        self.clients = []
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.camera_dimensions = (500, 500)

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
        self.color_index = 0
        self.pellets = RandomPellets(1)
        
    def start(self):
        try:
            self.s.bind((self.host, self.port))
        except socket.error as e:
            print("Error binding.", e)

        self.s.listen(5)
        Thread(target=self.game_loop).start()
        print("Server started.")
        print(f"Server IP: {self.host} Server Port: {self.port}")

    def listen(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            xdir = 1
            ydir = 0
            bounds = {
                'left': 0,
                'right': BOARD[0],
                'up': 0,
                'down': BOARD[1]
            }
            snake = Snake((250, 250), 5, xdir, ydir, bounds)
            client = Client(conn, snake)
            self.clients.append(client)
            self.color_index = (self.color_index + 1) % len(self.colors)
            Thread(target=self.get_input, args=(client,)).start()

    def get_input(self, client):
        while True:
            input_size_as_bytes = comm.receive_data(client.socket, comm.MSG_LEN)
            input_size = comm.size_as_int(input_size_as_bytes)
            input = pickle.loads(comm.receive_data(client.socket, input_size))
            if input == comm.Signal.QUIT:
                self.clients.remove(client)
                break
            client.snake.change_direction(input)

    def within_camera_bounds(self, camera_target, object_position):
        camera_left = camera_target[0] - self.camera_dimensions[0] / 2
        camera_right = camera_target[0] + self.camera_dimensions[0] / 2
        camera_up = camera_target[1] - self.camera_dimensions[1] / 2
        camera_down = camera_target[1] + self.camera_dimensions[1] / 2

        if object_position[0] < camera_left:
            return False
        elif object_position[0] > camera_right:
            return False
        if object_position[1] < camera_up:
             return False
        elif object_position[1] > camera_down:
            return False
        return True

    def get_snake_data(self, snake, camera_target):
        body_parts = []
        for body_part in snake.body:
            if not self.within_camera_bounds(camera_target, body_part.position):
                continue
            body_parts.append(
                BodyPartData(
                    body_part.position,
                    body_part.color,
                    body_part.width
                )
            )
        return body_parts

    def get_game_data(self, receiver_client):
        camera_target = receiver_client.snake.head.position
        snakes = []
        pellets = []
        for client in self.clients:
            if client == receiver_client: continue
            snakes.append(self.get_snake_data(client.snake, camera_target))
        for pellet in self.pellets.pellets:
            if not self.within_camera_bounds(camera_target, pellet.position):
                continue
            pellets.append(
                BodyPartData(
                    pellet.position,
                    pellet.color,
                    pellet.width
                )
            )
        snake = self.get_snake_data(receiver_client.snake, camera_target)
        return GameData(snake, snakes, pellets)

    def send_game_data(self, client, game_data_serialized):
        size = comm.size_as_bytes(game_data_serialized)
        comm.send_data(client.socket, size)
        comm.send_data(client.socket, game_data_serialized)

    def game_loop(self):
        clock = Clock()
        while True:
            pos = self.pellets.getPositions()
            for client in self.clients:
                snake = client.snake
                snake.move()
                if [snake.head.position[0], snake.head.position[1]] in pos:
                    pellet = self.pellets.pellets[pos.index([snake.head.position[0],snake.head.position[1]])]
                    self.pellets.resetPellet(pellet)
                    snake.grow(1)
                snake.check_body_collision()

            for client in self.clients:
                game_data_serialized = pickle.dumps(self.get_game_data(client))
                self.send_game_data(client, game_data_serialized)
            clock.tick(18)

def main():
    server = Server()
    server.start()
    server.listen()

if __name__ == '__main__':
    main()