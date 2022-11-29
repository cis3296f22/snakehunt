from enum import Enum, auto

MSG_LEN = 8

class Message(Enum):
    """
    An enum of messages that are sent between client and server.

    Attributes
    ----------
    QUIT:
        Indicate that the client has quit
    NAME_OK:
        Indicate that the client's chosen name is valid
    NAME_TOO_LONG:
        Indicate that the client's chosen name is beyond max length
    NAME_USED:
        Indicate that the client's chosen name is already used
    PELLET_EATEN:
        Indicate that a pellet was consumed
    SELF_COLLISION:
        Indicate that a snake collided with its own body
    OTHER_COLLISION:
        Indicate that a snake collided with another snake
    SERVER_SHUTDOWN:
        Indicate that the server has shutdown
    """
    QUIT = auto()
    NAME_OK = auto()
    NAME_TOO_LONG = auto()
    NAME_USED = auto()
    PELLET_EATEN = auto()
    SELF_COLLISION = auto()
    OTHER_COLLISION = auto()
    SERVER_SHUTDOWN = auto()

def send_data(socket, buffer):
    """
    Send binary buffer through socket.

    Parameters
    ----------
    socket (socket.socket):
        A socket

    buffer (bytes)
        A bytes object containing data to be sent to socket
            
    Return
    ------
    None
    """
    buffer_len = len(buffer)
    total_sent = 0
    while total_sent < buffer_len:
        sent = socket.send(buffer[total_sent:])
        if sent == 0:
            raise RuntimeError('Socket connection broken')
        total_sent += sent

def receive_data(socket, msg_length):
    """
    Receive binary data of a given length through socket.

    Parameters
    ----------
    socket (socket.socket):
        A socket

    msg_length (int)
        The number of bytes to receive
            
    Return
    ------
    A bytes object containing the data received
    """
    chunks = []
    bytes_received = 0
    while bytes_received < msg_length:
        chunk = socket.recv(min(msg_length - bytes_received, 2048))
        if chunk == b'':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_received = bytes_received + len(chunk)
    return b''.join(chunks)

def size_as_bytes(buffer):
    """
    Return the size of a buffer as a bytes object.

    Used to send the size of a buffer through a socket.

    Parameters
    ----------
    buffer (bytes):
        The bytes object to get the size of

    Return
    ------
    size of buffer as a bytes object
    """
    size = str(len(buffer))
    for i in range(MSG_LEN - len(size)):
        size = '0' + size
    return size.encode()

def to_int(buffer):
    """
    Return the numeric value of buffer.

    buffer is expected to be the result of a previous size_as_bytes() call.

    Parameters
    ----------
    buffer (bytes):
        A bytes object denoting a number

    Return
    ------
    size of buffer as an int
    """
    return int(buffer.decode())
