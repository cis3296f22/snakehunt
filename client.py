# Imports from standard/third-party modules
import socket
import pickle
import pygame
import tkinter
from tkinter import *
from tkinter import ttk

# Imports from local modules
from gamedata import *
import comm

class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def input_addr(self):
        server_ip = input("Enter server IP: ")
        server_port = input("Enter server port: ")
        self.addr = (server_ip, int(server_port))

    def connect(self):
        try:
            self.socket.connect(self.addr)
            return True
        except:
            print('Connection failed')
            return False

class PauseMenu:
    def __init__(self, game):
        self.root = Tk()
        self.root.geometry('275x125')
        self.game = game
        self.current_name = StringVar()
        self.populate()
        self.root.mainloop()

    def receive_name_feedback(self):
        socket = self.game.client.socket

        feedback_size_bytes = comm.receive_data(socket, comm.MSG_LEN)
        feedback_size = comm.size_as_int(feedback_size_bytes)
        feedback = pickle.loads(comm.receive_data(socket, feedback_size))

        if feedback == comm.Message.NAME_OK:
            self.root.destroy()
        elif feedback == comm.Message.NAME_TOO_LONG:
            size_bytes = comm.receive_data(socket, comm.MSG_LEN)
            size = comm.size_as_int(size_bytes)
            max_name_length = pickle.loads(comm.receive_data(socket, size))
            self.name_feedback.config(text=f"Max name length is {max_name_length} characters.")
        elif feedback == comm.Message.NAME_USED:
            self.name_feedback.config(text=f"Name taken, please select another name.")

    def send_name(self):
        socket = self.game.client.socket

        name = pickle.dumps(self.current_name.get())
        size = comm.size_as_bytes(name)
        comm.send_data(socket, size)
        comm.send_data(socket, name)

        self.receive_name_feedback()

    def quit(self):
        self.game.running = False
        self.root.destroy()

    def populate(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack()

        naming_frame = ttk.Frame(frame)
        naming_frame.pack()
        ttk.Label(naming_frame, text = "Display Name: ").pack(side=tkinter.LEFT)
        naming_entry = Entry(naming_frame, width=25, textvariable=self.current_name)
        naming_entry.pack(side=tkinter.LEFT)

        self.name_feedback = ttk.Label(frame, text = "")
        self.name_feedback.pack(pady=10)

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=5)
        ttk.Button(buttons_frame, text='Play', command=self.send_name).pack(side=tkinter.LEFT, padx=3)
        ttk.Button(buttons_frame, text='Quit', command=self.quit).pack(side=tkinter.LEFT, padx=3)

class Game():
    def __init__(self, client):
        pygame.init()
        self.camera = (500, 500)
        self.board = (1000, 1000)
        self.client = client

    def start(self):
        self.window = pygame.display.set_mode(self.camera)

    def render_bounds(self, head):
        if head.position[0] + self.camera[0]/2 > self.board[0]:
            off_map_width = (head.position[0] + self.camera[0]/2 - self.board[0])
            off_map_rect = (self.camera[0] - off_map_width, 0, off_map_width, self.camera[1])
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)
        elif head.position[0] - self.camera[0]/2 < 0:
            off_map_width = -(head.position[0] - self.camera[0]/2)
            off_map_rect = (0, 0, off_map_width, self.camera[1])
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)
        if head.position[1] + self.camera[1]/2 > self.board[1]:
            off_map_width = (head.position[1] + self.camera[1]/2 - self.board[1])
            off_map_rect = (0, self.camera[0] - off_map_width, self.camera[0], off_map_width)
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)
        elif head.position[1] - self.camera[1]/2 < 0:
            off_map_width = -(head.position[1] - self.camera[1]/2)
            off_map_rect = (0, 0, self.camera[0], off_map_width)
            pygame.draw.rect(self.window, (255, 0, 0), off_map_rect)

    def render(self, game_data):
        snakes = game_data.snakes
        pellets = game_data.pellets

        self.window.fill((0, 0, 0))
        my_head = game_data.snake[0]

        self.render_bounds(my_head)
    
        head_rect = (self.camera[0] / 2, self.camera[1] / 2, my_head.width - 2, my_head.width - 2)
        pygame.draw.rect(self.window, my_head.color, head_rect)

        game_objects = game_data.snake[1:]
        for snake in snakes:
            for body_part in snake:
                game_objects.append(body_part)
        for pellet in pellets:
            game_objects.append(pellet)
        
        for object in game_objects:
            left = head_rect[0] + object.position[0] - my_head.position[0]
            top = head_rect[1] + object.position[1] - my_head.position[1]
            rect = (left, top, object.width - 2, object.width - 2)
            pygame.draw.rect(self.window, object.color, rect);
            
        pygame.display.update()

    def get_direction(self):
        direction = None
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            direction = (-1, 0)
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            direction = (1, 0)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]):
            direction = (0, -1)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            direction = (0, 1)
        return direction

    def game_loop(self):
        self.running = True
        while self.running:
            msg = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    msg = pickle.dumps(comm.Message.QUIT)
                    self.running = False
            
            # Send input or quit signal to server
            if msg == None:
                msg = pickle.dumps(self.get_direction())
            comm.send_data(self.client.socket, comm.size_as_bytes(msg))
            comm.send_data(self.client.socket, msg)

            # If the player decided to quit, exit the game loop after notifying server
            if not self.running: break
            
            # Receive game data from server, use it to render
            size_as_bytes = comm.receive_data(self.client.socket, comm.MSG_LEN)
            length = comm.size_as_int(size_as_bytes)
            game_data = pickle.loads(comm.receive_data(self.client.socket, length))
            self.render(game_data)
        pygame.quit()

def main():
    client = Client()
    client.input_addr()
    if not client.connect():
        return

    game = Game(client)
    menu = PauseMenu(game)

    game.start()
    game.game_loop()

if __name__ == "__main__":
    main()
