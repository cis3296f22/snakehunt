import pickle
import socket
from threading import Thread

from gamedata import *
import comm
from game import *

class Server():
    def __init__(self):
        self.game = Game(self)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start(self):
        try:
            self.s.bind((self.host, self.port))
        except socket.error as e:
            print("Error binding.", e)

        self.s.listen(5)
        Thread(target=self.game.game_loop).start()
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
                for pl in self.game.players:
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
                self.game.remove_player(player)
                break
            player.snake.change_direction(input)

    def player_handler(self, socket):
        xdir = 1
        ydir = 0
        snake = Snake((250, 250), 5, xdir, ydir, self.game.bounds)
        player = Player(snake, socket)
        
        if not self.receive_name(player): return

        self.game.add_player(player)
        self.receive_input(player)

    def send_game_data(self, player, game_data_serialized):
        size = comm.size_as_bytes(game_data_serialized)
        comm.send_data(player.socket, size)
        comm.send_data(player.socket, game_data_serialized)

def main():
    server = Server()
    server.start()
    server.listen()

if __name__ == '__main__':
    main()
