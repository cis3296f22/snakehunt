import pickle
import socket
from pygame.time import Clock
from threading import Thread

from gamedata import *
import comm
from game import *

class Server():
    def __init__(self):
        self.players = []
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.camera_dimensions = (500, 500)
        self.pellets = RandomPellets(1)
        self.bounds = {
            'left': 0,
            'right': BOARD[0],
            'up': 0,
            'down': BOARD[1]
        }
        
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
            socket, addr = self.s.accept()
            print("Connected to:", addr)

            Thread(target=self.player_handler, args=(socket,)).start()

    def receive_name(self, player):
        while True:
            # Receive name input or quit signal
            input_size_as_bytes = comm.receive_data(player.socket, comm.MSG_LEN)
            input_size = comm.size_as_int(input_size_as_bytes)
            input = pickle.loads(comm.receive_data(player.socket, input_size))

            # Client quit during name selection
            if input == comm.Message.QUIT:
                return False

            name_accepted = False

            # The name is either valid, too long, or already used.
            response = None
            if len(input) > MAX_NAME_LENGTH:
                response = pickle.dumps(comm.Message.NAME_TOO_LONG)
            else:
                for pl in self.players:
                    if pl.name == input:
                        response = pickle.dumps(comm.Message.NAME_USED)
                        break
            if response == None:
                response = pickle.dumps(comm.Message.NAME_OK)
                player.name = input
                name_accepted = True

            # Tell client if name was valid, too long, or already used
            size_as_bytes = comm.size_as_bytes(response)
            comm.send_data(player.socket, size_as_bytes)
            comm.send_data(player.socket, response)

            if name_accepted:
                return True

            # If the name was too long, send a message to client indicating max allowed length
            if len(input) > MAX_NAME_LENGTH:
                max_length = pickle.dumps(MAX_NAME_LENGTH)
                size_as_bytes = comm.size_as_bytes(max_length)
                comm.send_data(player.socket, size_as_bytes)
                comm.send_data(player.socket, max_length)

    def receive_input(self, player):
        while True:
            input_size_as_bytes = comm.receive_data(player.socket, comm.MSG_LEN)
            input_size = comm.size_as_int(input_size_as_bytes)
            input = pickle.loads(comm.receive_data(player.socket, input_size))
            if input == comm.Message.QUIT:
                self.players.remove(player)
                break
            player.snake.change_direction(input)

    def player_handler(self, socket):
        xdir = 1
        ydir = 0
        snake = Snake((250, 250), 5, xdir, ydir, self.bounds)
        player = Player(snake, socket)
        
        if not self.receive_name(player): return

        self.players.append(player)
        self.receive_input(player)

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
                CellData(
                    body_part.position,
                    body_part.color,
                    body_part.width
                )
            )
        return body_parts

    def get_game_data(self, receiver_player):
        camera_target = receiver_player.snake.head.position
        snakes = []
        pellets = []
        for player in self.players:
            if player == receiver_player: continue
            snakes.append(self.get_snake_data(player.snake, camera_target))
        for pellet in self.pellets.pellets:
            if not self.within_camera_bounds(camera_target, pellet.position):
                continue
            pellets.append(
                CellData(
                    pellet.position,
                    pellet.color,
                    pellet.width
                )
            )
        snake = self.get_snake_data(receiver_player.snake, camera_target)
        return GameData(snake, snakes, pellets)

    def send_game_data(self, player, game_data_serialized):
        size = comm.size_as_bytes(game_data_serialized)
        comm.send_data(player.socket, size)
        comm.send_data(player.socket, game_data_serialized)

    def game_loop(self):
        clock = Clock()
        while True:
            pos = self.pellets.getPositions()
            for player in self.players:
                snake = player.snake
                snake.move()
                if [snake.head.position[0], snake.head.position[1]] in pos:
                    pellet = self.pellets.pellets[pos.index([snake.head.position[0],snake.head.position[1]])]
                    self.pellets.resetPellet(pellet)
                    snake.grow(1)
                snake.check_body_collision()

            for player in self.players:
                game_data_serialized = pickle.dumps(self.get_game_data(player))
                self.send_game_data(player, game_data_serialized)
            clock.tick(18)

def main():
    server = Server()
    server.start()
    server.listen()

if __name__ == '__main__':
    main()