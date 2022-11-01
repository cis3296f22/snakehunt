import socket
from threading import Thread
import pickle
import random
from client import Player

players = {}

class Server:

    def __init__(self):
        self.host = "localhost"
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.playerNum = 0

    def start(self):
        #bind to host
        try:
            self.s.bind((self.host, self.port))
        except socket.error as e:
            print("Error binding.", e)

        #listen/wait for incoming client connections
        self.s.listen(5)
        print(f"Server started. Waiting for a connection on {self.port}")
        self.take_connection()
        
    #continuously listen and take connections
    def take_connection(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            ACCEPT_THREAD = Thread(target=self.thread_client, args=(conn, addr, self.playerNum))
            ACCEPT_THREAD.start()
            self.playerNum += 1
    
    def thread_client(self, conn, addr, player_index):
        rand_x = random.randrange(1, 50)
        rand_y = random.randrange(1, 50)
        color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        
        player = Player(rand_x, rand_y, 50, 50, color)
        players[player_index] = player
        conn.send(pickle.dumps(players[player_index]))
        print("[SERVER] Started thread with player index:", player_index)
        current_player = players[player_index]
        is_online = True
        while is_online:
            try:
                data = pickle.loads(conn.recv(2048))
                players[player_index] = data
                list_players = {}
                if not data:
                    print(f"{addr} has disconnected")
                    is_online = False
                else:
                    for player_idx in players:
                        player = players[player_idx]
                        if player != current_player:
                            list_players[player_idx] = player

                conn.sendall(pickle.dumps(list_players))

            except Exception as e:
                print(f"[SERVER] {addr} has disconnected.", e)
                is_online = False

        print(f"[SERVER] Ended threaded tasks for client: {addr}")
        self.player_index -= 1
        del players[player_index]
        conn.close()


def main():
    server = Server()
    server.start()


if __name__ == '__main__':
    main()
