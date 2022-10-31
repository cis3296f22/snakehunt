import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "localhost"
port = 5555
playerCount = 0

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#listen/wait for incoming client connections
s.listen(2)
print("Waiting for a connection, Server Started")

#convert string "(x,y)" to int tuple (x,y)
def read_pos(str): 
    str = str.split(",")
    return int(str[0]), int(str[1])

#convert int tuple (x,y) to string "(x,y)"
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

#initial positions of 3 players; pos[0]=(0,0)
pos = [(0,0),(100,100)]#,(0,100)]

#connect every client from addresses provided by server simultaneously
def threaded_client(conn, player):
    #send data, convert (0,0) to "(0,0)"
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        '''conn.recv gets data from every client
        & returns server response to a specific client
        '''
        try:
            #read received data and convert "(0,0)" to (0,0)
            data = read_pos(conn.recv(2048).decode()) #(int,int)
            #set player position to (0,0) [player1]
            pos[player] = data

            #if data not received, 
            if not data:
                print("Disconnected")
                break
            else:
                #if player1, reply with player0 pos
                if player == 1:
                    reply = pos[0]
                #if player0, reply with player1 pos
                else:
                    reply = pos[1]
            
            #send reply
            conn.sendall(str.encode(make_pos(reply)))
                    
                    
        except:
            break

    print("Lost connection")
    conn.close()

playerCount = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, playerCount))
    playerCount += 1
s.close()