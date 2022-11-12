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
                'right': 500,
                'up': 0,
                'down': 500
            }
            snake = Snake((250, 250), 1, xdir, ydir, bounds)
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

    def get_game_data(self):
        snakes = []
        pellets = []
        for client in self.clients:
            body_parts = []
            for body_part in client.snake.body:
                body_parts.append(
                    BodyPartData(
                        body_part.position,
                        body_part.color,
                        body_part.width
                    )
                )
            snakes.append(body_parts)
        for pellet in self.pellets.pellets:
            pellets.append(
                BodyPartData(
                    pellet.position,
                    pellet.color,
                    pellet.width
                )
            )
        return GameData(snakes, pellets)

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
            game_data_serialized = pickle.dumps(self.get_game_data())
            for client in self.clients:
                self.send_game_data(client, game_data_serialized)
            clock.tick(18)

def main():
    server = Server()
    server.start()
    server.listen()

if __name__ == '__main__':
    main()