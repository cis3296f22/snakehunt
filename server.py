import socket
import threading #referenced https://realpython.com/intro-to-python-threading/
import pickle
import sys

class Server:
    def __init__(self):
        self.running = True
        
    def Session(self, conn_list):
        player1_data = []
        player2_data = []
        
        while self.running:
            player1_data = conn_list[0].recv(1024)
            player2_data = conn_list[1].recv(1024)
            if not (player1_data or player2_data):
                break
            
            player1_data = pickle.loads(player1_data)
            player2_data = pickle.loads(player2_data)
            player1_data = pickle.dumps(player1_data)
            player2_data = pickle.dumps(player2_data)
            
            conn_list[0].sendall(player1_data)
            conn_list[1].sendall(player2_data)
            
            
    def Start(self):
        PLAYERCOUNT = 2
        self.running = True
        HOST = "localhost"
        PORT = 5556
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((HOST, PORT))
        except socket.error as e:
            str(e)

        #playerCount = 0 ###?

        #listen/wait for incoming client connections
        self.s.listen(5)
        conn_list = []
        threads = []
        print("Waiting for a connection, Server Started")
        
        while self.running:
            for i in range(PLAYERCOUNT):
                try:
                    if i:
                        print("Waiting for Player {} to connect".format(i))
                    conn, addr = self.s.accept()
                    print("Connected to:", addr)
                    conn_list.append(conn) #add new connection to list of connections
                except:
                    self.running = False
            
            threads.append(threading.Thread(target=self.Session, args=(conn_list,)))
            threads[-1].start() #start just-added thread
            conn_list = []
            
    def End(self):
        self.s.close()
        self.running = False
        
class Window():
    def __init__(self):
        self.server_online = False
        self.new_server = Server()
        if not self.server_online:
            self.server = threading.Thread(target=self.new_server.Start, args=())
            self.server.start()
            self.server_online = True
        else:
            print("Server running already.")
if __name__ == "__main__":
    window = Window()
