# Imports from standard/third-party modules
import os
import socket
import pickle
import pygame
import pygame.font
from pygame.locals import *
import tkinter
from threading import Thread
from tkinter import *
from tkinter import ttk
import sys

# Imports from local modules
from gamedata import *
import comm

root = Tk()

# Find the full path of 'relative_path'
# If we are running the code directly, the current dir joined with 'relative_path' is the full path
# If we are running the executable, the full path is the temp directory that pyinstaller creates joined with 'relative_path'
def resource_path(relative_path):
    try:
        # This is just a temp directory that pyinstaller uses to store assets (images, font, etc...)
        base = sys._MEIPASS 
    except:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)

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
        #self.root = Tk()
        root.geometry('275x125')
        self.game = game
        self.current_name = StringVar()
        self.populate()
        root.mainloop()

    def receive_name_feedback(self):
        socket = self.game.client.socket

        feedback_size_bytes = comm.receive_data(socket, comm.MSG_LEN)
        feedback_size = comm.to_int(feedback_size_bytes)
        feedback = pickle.loads(comm.receive_data(socket, feedback_size))

        if feedback == comm.Message.NAME_OK:
            root.destroy()
        elif feedback == comm.Message.NAME_TOO_LONG:
            size_bytes = comm.receive_data(socket, comm.MSG_LEN)
            size = comm.to_int(size_bytes)
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

        socket = self.game.client.socket
        quit_msg = pickle.dumps(comm.Message.QUIT)
        size = comm.size_as_bytes(quit_msg)
        comm.send_data(socket, size)
        comm.send_data(socket, quit_msg)

        root.destroy()

    def populate(self):
        frame = ttk.Frame(root, padding=10)
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
    def __init__(self, client, radio):
        pygame.init()
        self.camera = (500, 500)
        self.board = (1000, 1000)
        self.client = client
        self.running = True
        self.radio = radio
        self.leaderboard_font = pygame.font.Font(resource_path('./fonts/arial_bold.ttf'), 10)


    def start(self):
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        flags = DOUBLEBUF
        self.window = pygame.display.set_mode(self.camera, flags, 16)

    def show_leaderboard(self, leaderboard):
        top = 8
        for i, entry in enumerate(leaderboard):
            record_string = f'{i + 1}.   {entry.name}   {entry.score}'
            record = self.leaderboard_font.render(record_string, True, (255, 255, 255))
            record_rect = record.get_rect()
            record_rect.topleft = (8, top)
            self.window.blit(record, record_rect)
            top += 13

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

    def draw_eyes(self, head, rect):
        color = (255,0,0)
        x = rect[0]
        y = rect[1]
        w = rect[2] -3
        h = rect[3] -3 
        left_eye = right_eye = None
        if head.direction[0] == 0:  #parallel to y axis
            if head.direction[1] == 1:  #going down
                left_eye = (x + w, y + h-3, 2, 4)
                right_eye = (x + 1, y + h-3, 2, 4)
            else:                       #going up
                left_eye = (x + 1 , y + 1, 2, 4)
                right_eye = (x + w, y + 1, 2, 4)
                
        if head.direction[1] == 0:  #parallel to x axis
            if head.direction[0] == 1:  #going right
                left_eye = (x + w -2, y + 1, 4, 2)
                right_eye = (x + w-2, y + h, 4, 2)
            else:                       #going left
                left_eye = (x + 1 , y + h, 4, 2)
                right_eye = (x + 1, y + 1, 4, 2)
                
        pygame.draw.rect(self.window, color, left_eye)
        pygame.draw.rect(self.window, color, right_eye)

    def render(self, game_data):
        def make_rect(headRect, headPos, objPos, objWidth):
            left = headRect[0] + objPos[0] - headPos[0]
            top = headRect[1] + objPos[1] - headPos[1]
            return (left, top, objWidth-2, objWidth-2)
        
        snake = game_data.snake
        snakes = game_data.snakes
        pellets = game_data.pellets

        self.window.fill((0, 0, 0))
        my_head = snake[0]

        self.render_bounds(my_head)
    
        head_rect = (self.camera[0] / 2, self.camera[1] / 2, my_head.width - 2, my_head.width - 2)

        for pellet in pellets:
            pygame.draw.rect(self.window, pellet.color, make_rect(head_rect, my_head.position, pellet.position, pellet.width))
            
        for this_snake in snakes:
            for body_part in this_snake:
                rect = make_rect(head_rect, my_head.position, body_part.position, body_part.width)
                pygame.draw.rect(self.window, body_part.color, rect)
                if body_part.direction is not None:
                    self.draw_eyes(body_part, rect)
            
        pygame.draw.rect(self.window, my_head.color, head_rect)
        self.draw_eyes(my_head, head_rect)
        for body_part in snake[1:]:
            pygame.draw.rect(self.window, body_part.color, make_rect(head_rect, my_head.position, body_part.position, body_part.width))
            
        self.show_leaderboard(game_data.leaderboard)
        pygame.display.flip()

    def get_direction(self):
        direction = None
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            direction = (-1, 0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            direction = (1, 0)
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            direction = (0, -1)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            direction = (0, 1)
        return direction

    def game_loop(self):
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
            if not self.running:
                break
            
            # Receive game data from server, use it to render
            # If an exception occurs it is likely that the server has shut down, in which case
            # we exit the client.
            try:
                size_as_bytes = comm.receive_data(self.client.socket, comm.MSG_LEN)
                length = comm.to_int(size_as_bytes)
                game_data = pickle.loads(comm.receive_data(self.client.socket, length))
            except:
                break

            if game_data == comm.Message.SERVER_SHUTDOWN:
                print("Server shutting down")
                break

            self.render(game_data)

            if game_data.sound is not None:
                self.radio.play_sound(game_data.sound)

        pygame.quit()
        
class MusicPlayer():
    def __init__(self, song):
        pygame.mixer.init()
        
        self.pellet_sound = pygame.mixer.Sound("sound/pellet_sound.mp3")
        self.self_collision = pygame.mixer.Sound("sound/self_collision.mp3")
##        self.other_collision = pygame.mixer.Sound()
        Thread(target=self.play_song, args=(song,)).start()
        
    def play_song(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)

    def play_sound(self, sound):
        if sound == comm.Message.PELLET_EATEN:
            self.pellet_sound.play()
        elif sound == comm.Message.SELF_COLLISION or sound == comm.Message.OTHER_COLLISION:
            self.self_collision.play()

def main():
    
    client = Client()
    client.input_addr()
    if not client.connect():
        return

    radio = MusicPlayer("sound/snake_hunt.mp3")
    game = Game(client, radio)
    PauseMenu(game)

    game.start()
    game.game_loop()

if __name__ == '__main__':
    main()
