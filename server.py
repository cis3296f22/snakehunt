import pickle
import socket
from threading import Thread

from gamedata import *
import comm
from game import *

class Server():
    """
    Game server

    Attributes
    ----------
    game (Game):
        Instance of the running game

    host (str):
        Hostname of the machine

    port (int):
        Port number

    s (socket.socket):
        A TCP server socket

    next_id (int):
        Unique ID to assign to next player
    
    Methods
    -------
    start()
    listen()
    receive_name(player)
    receive_input(player)
    player_handler(player)
    send_game_data(player, game_data_serialized)
    on_exit()
    listen_exit()
    """
    def __init__(self):
        """Initialize server."""
        self.game = Game(self)
        self.host = self.get_ip_address()
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.next_id = 0

    def get_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.9", 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            return socket.gethostbyname(socket.gethostname())
        return ip
        
    def start(self):
        """
        Start listening for connections and start game loop

        Return
        ------
        None
        """
        try:
            self.s.bind((self.host, self.port))
        except socket.error as e:
            print("Error binding.", e)

        self.s.listen(5)
        Thread(target=self.game.game_loop).start()
        print("Server started.")
        print(f"Server IP: {self.host} Server Port: {self.port}")

    def listen(self):
        """
        Listen for connections, create a thread for each connected client.

        Return
        ------
        None
        """
        while True:
            sock, addr = self.s.accept()
            if not self.game.running:
                break
            print("Connected to:", addr)

            position = self.game.get_random_position()
            snake = Snake(position, Snake.INITIAL_LENGTH, 1, 0, self.game.bounds)
            player = Player(self.next_id, snake, sock)
            self.next_id = self.next_id + 1

            Thread(target=self.player_handler, args=(player,)).start()

    def receive_name(self, player):
        """
        Receive name input from a player

        Parameters
        ----------
        player (Player):
            The player to listen to

        Return
        ------
        True if the name was accepted, False if the player quits.
        """
        while True:
            input_size_as_bytes = comm.receive_data(player.socket, comm.MSG_LEN)
            input_size = comm.to_int(input_size_as_bytes)
            input = pickle.loads(comm.receive_data(player.socket, input_size))

            if input == comm.Message.QUIT:
                return False

            name_accepted = False

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

            size_as_bytes = comm.size_as_bytes(response)
            comm.send_data(player.socket, size_as_bytes)
            comm.send_data(player.socket, response)

            if name_accepted:
                return True

            if len(input) > MAX_NAME_LENGTH:
                max_length = pickle.dumps(MAX_NAME_LENGTH)
                size_as_bytes = comm.size_as_bytes(max_length)
                comm.send_data(player.socket, size_as_bytes)
                comm.send_data(player.socket, max_length)

    def receive_input(self, player):
        """
        Receive directional input or quit signal from player.

        Use input to change direction.

        Parameters
        ----------
        player (Player):
            The player to receive input from

        Return
        ------
        None
        """

        while self.game.running:
            try:
                input_size_as_bytes = comm.receive_data(player.socket, comm.MSG_LEN)
                input_size = comm.to_int(input_size_as_bytes)
                input = pickle.loads(comm.receive_data(player.socket, input_size))
                #print(input)
            except:
                self.game.remove_player(player)
                break
            if input == comm.Message.QUIT:
                self.game.remove_player(player)
                break
            player.snake.change_direction(input)

    def player_handler(self, player):
        """
        Handle a connected player.

        Parameters
        ----------
        player (Player):
            The player to handle

        Return
        ------
        None
        """
        if not self.receive_name(player): return
        self.game.add_player(player)
        self.receive_input(player)

    def send_game_data(self, player, game_data_serialized):
        """
        Send game data to a player

        Parameters
        ----------
        player (Player):
            The player to send data to

        game_data_serialized (bytes):
            Game data as a bytes object

        Return
        ------
        None
        """
        size = comm.size_as_bytes(game_data_serialized)
        comm.send_data(player.socket, size)
        comm.send_data(player.socket, game_data_serialized)

    def on_exit(self):
        """
        Notify players that server will shutdown and close sockets.

        Return
        ------
        None
        """
        self.game.running = False
        shutdown_msg = pickle.dumps(comm.Message.SERVER_SHUTDOWN)
        shutdown_msg_length = comm.size_as_bytes(shutdown_msg)
        for player in self.game.players:
            comm.send_data(player.socket, shutdown_msg_length)
            comm.send_data(player.socket, shutdown_msg)

        terminator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        terminator_socket.connect((self.host, self.port))
        
    def listen_exit(self):
        """
        Prompt user to shutdown server.

        Return
        ------
        None
        """
        while self.game.running:
            print('Enter \'exit\' to shutdown server')
            user_input = input()
            if user_input.lower() == 'exit':
                self.on_exit()

def main():
    server = Server()
    server.start()
    Thread(target=server.listen).start()
    server.listen_exit()

if __name__ == '__main__':
    main()
