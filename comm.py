from enum import Enum, auto

MSG_LEN = 8

class Message(Enum):
    QUIT = auto()
    NAME_OK = auto()
    NAME_TOO_LONG = auto()
    NAME_USED = auto()
    PELLET_EATEN = auto()       #when the player eats a pellet
    SELF_COLLISION = auto()     #when the player hits self
    OTHER_COLLISION = auto()    #when the player hits another player
    
# Sends the data in 'buffer' to 'socket'
def send_data(socket, buffer):
    buffer_len = len(buffer)
    total_sent = 0
    while total_sent < buffer_len:
        sent = socket.send(buffer[total_sent:])
        if sent == 0:
            raise RuntimeError('Socket connection broken')
        total_sent += sent

# Receive message of size 'msg_length' from socket
def receive_data(socket, msg_length):
    chunks = []
    bytes_received = 0
    while bytes_received < msg_length:
        chunk = socket.recv(min(msg_length - bytes_received, 2048))
        if chunk == b'':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_received = bytes_received + len(chunk)
    return b''.join(chunks)

# Returns the numeric string representation of the size of 'buffer' as an array of bytes
# To get the size of 'buffer' the return value must be decoded then cast to an int 
def size_as_bytes(buffer):
    size = str(len(buffer))
    for i in range(MSG_LEN - len(size)):
        size = '0' + size
    return size.encode()

# 'buffer' is expected to be an array of bytes that can be decoded to a numeric string
def size_as_int(buffer):
    return int(buffer.decode())
