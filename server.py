import pickle
import socket
from pygame.time import Clock
from gamedata import *
from threading import Thread, Lock
import comm

class BodyPart():
    speed = 25   # Number of pixels that the part moves per frame
    width = 25
    def __init__(self, position, xdir, ydir, color):
        self.position = position
        self.xdir = xdir
        self.ydir = ydir
        self.color = color

    def set_direction(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir

    def move(self):
        self.position = (self.position[0] + self.speed * self.xdir, self.position[1] + self.speed * self.ydir)

class Snake():
    def __init__(self, position, length, xdir, ydir, color, field_dimension):
        self.body = []
        self.turns = {}
        self.position = position
        self.length = length
        self.color = color
        self.field_dimension = field_dimension
        self.initialize(position, xdir, ydir, color)

    # Initializes all parts of the snake based on length
    def initialize(self, position, xdir, ydir, color):
        posx = position[0]
        for i in range(self.length):
            self.body.append(BodyPart((posx, position[1]), xdir, ydir, color))
            posx -= 25
        self.head = self.body[0]

    def change_direction(self, direction):
        if direction == None: return

        if self.head.xdir != -direction[0] or self.head.ydir != -direction[1]:
            if self.head.xdir != -direction[0]:
                self.head.xdir = direction[0]
            if self.head.ydir != -direction[1]:
                self.head.ydir = direction[1]
            self.turns[self.head.position[:]] = [self.head.xdir, self.head.ydir]
    
    # Move every part of the snake.
    # If a part is at a position where a previous turn occurred, set its direction to the
    # direction of the previous turn.
    # When the last part passes a turn, the turn is removed from the dictionary.
    def move(self):
        for i, part in enumerate(self.body):
            pos = part.position[:]
            if pos in self.turns:
                turn = self.turns[pos]
                part.set_direction(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(pos)
            part.move()
            if part.position[0] < 0:
                part.position = (self.field_dimension[0] - 25, part.position[1])
            elif part.position[0] > self.field_dimension[0] - 1:
                part.position = (0, part.position[1])
            elif part.position[1] > self.field_dimension[1] - 1:
                part.position = (part.position[0], 0)
            elif part.position[1] < 0:
                part.position = (part.position[0], self.field_dimension[0] - 25)

class Client():
    def __init__(self, conn, snake):
        self.conn = conn
        self.snake = snake
        self.received_input = False
        self.lock = Lock()

class Server():
    def __init__(self):
        self.clients = []
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
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
            snake = Snake((250, 250), 3, xdir, ydir, (255, 255, 255), (500, 500))
            client = Client(conn, snake)
            self.clients.append(client)
            Thread(target=self.get_input, args=(client,)).start()

    def get_input(self, client):
        while True:
            input = pickle.loads(client.conn.recv(2048))    #input is either False or a direction
            if input == False:
                self.clients.remove(client)
                break
            client.snake.change_direction(input)
            with client.lock:
                client.received_input = True

    def get_game_data(self):
        snakes = []
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
        return GameData(snakes)

    def send_game_data(self, client, game_data_serialized):
        size = comm.size_as_bytes(game_data_serialized)
        comm.send_data(client.conn, size)
        comm.send_data(client.conn, game_data_serialized)

    def game_loop(self):
        clock = Clock()
        while True:
            for client in self.clients:
                client.snake.move()
            game_data_serialized = pickle.dumps(self.get_game_data())
            for client in self.clients:
                with client.lock:
                    if client.received_input:
                        self.send_game_data(client, game_data_serialized)
                        client.received_input = False
            clock.tick(15)

def main():
    server = Server()
    server.start()
    server.listen()

if __name__ == '__main__':
    main()