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

from gamedata import *
import comm
import menu
from menu import *

#root = Tk()

def resource_path(relative_path):
    """
    Find the full path of a resource file.

    Pyinstaller executables place resource files (image, font, sound) 
    in a temporary directory.

    This helper function determines whether the program was launched as
    an executable. If so, it prepends the path of the temporary directory
    to the parameter 'relative_path'

    If the program was not launched as an executable, the current working
    directory is prepended to 'relative_path'

    Parameters
    ----------
    relative_path (string): The relative path of the resource file

    Return
    ------
    The full path to the resource file.
    """
    try:
        # This is just a temp directory that pyinstaller uses to store assets (images, font, etc...)
        base = sys._MEIPASS 
    except:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)

class Client():
    """
    Represents a client. Allows connection to a server of choice.

    Attributes
    ----------
    socket (socket.socket):
        A TCP socket

    addr (tuple[str, int]):
        A tuple that holds an IP address and port number of the server to connect to

    Methods
    -------
    input_addr()
    connect()
    """
    def __init__(self):
        """Initialize a TCP socket"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = None

    def connect(self, address):
        """
        Connect to the currently stored address
        
        Return
        ------
        True if connection succeeded, False otherwise.
        """

        try:
            print("address and port: ", address)
            
            self.socket.connect(address)
            return True
        except (ConnectionRefusedError, OSError) as error:
            self.socket.close()
            self.__init__()
            print("error connecting: ", error)
            return False

    def check_name(self, name):
        if name == None or len(name) == 0:
            print("invalid name: empty")
            return False
        

        
        if self.send_name(name):
            print("name is ok")
            return True
        else:
            print("bad name")
            return False

    def receive_name_feedback(self):
        feedback_size_bytes = comm.receive_data(self.socket, comm.MSG_LEN)
        feedback_size = comm.to_int(feedback_size_bytes)
        feedback = pickle.loads(comm.receive_data(self.socket, feedback_size))

        if feedback == comm.Message.NAME_OK:
            print("name is ok from the horse's mouth")
            return True
        
        elif feedback == comm.Message.NAME_TOO_LONG:
            size_bytes = comm.receive_data(socket, comm.MSG_LEN)
            size = comm.to_int(size_bytes)
            max_name_length = pickle.loads(comm.receive_data(socket, size))
            print("max name length: ", max_name_length)
            return False
        elif feedback == comm.Message.NAME_USED:
            print("name already taken")
            return False

    def send_name(self, name):
        name = pickle.dumps(name)
        size = comm.size_as_bytes(name)
        comm.send_data(self.socket, size)
        comm.send_data(self.socket, name)

        return self.receive_name_feedback()

    

# class Menu:
#     """
#     Menu that is displayed upon startup.

#     This menu allows the player to select a name and receive
#     validation from the server.

#     Upon selecting a valid name, the player can enter the game.

#     The player could also quit.

#     Attributes
#     ----------
#     game (Game):
#         A reference to the game object
    
#     current_name (tkinter.StringVar):
#         Keeps track of the current name entered by user

#     Methods
#     -------
#     receive_name_feedback()
#     send_name()
#     quit()
#     populate()
#     """

#     def __init__(self, game):
#         """Create the menu"""
#         #self.root = Tk()
#         root.geometry('275x125')
#         self.game = game
#         self.current_name = StringVar()
#         self.populate()
#         root.mainloop()

#     def receive_name_feedback(self):
#         """
#         Receive feedback on chosen name from server.

#         If the name is valid, destroy the menu and start the game.
#         If the name is invalid, prompt the user to select another name.

#         Return
#         ------
#         None
#         """
#         socket = self.game.client.socket

#         feedback_size_bytes = comm.receive_data(socket, comm.MSG_LEN)
#         feedback_size = comm.to_int(feedback_size_bytes)
#         feedback = pickle.loads(comm.receive_data(socket, feedback_size))

#         if feedback == comm.Message.NAME_OK:
#             root.destroy()
#         elif feedback == comm.Message.NAME_TOO_LONG:
#             size_bytes = comm.receive_data(socket, comm.MSG_LEN)
#             size = comm.to_int(size_bytes)
#             max_name_length = pickle.loads(comm.receive_data(socket, size))
#             self.name_feedback.config(text=f"Max name length is {max_name_length} characters.")
#         elif feedback == comm.Message.NAME_USED:
#             self.name_feedback.config(text=f"Name taken, please select another name.")

#     def send_name(self):
#         """
#         Send the current entered name to the server.

#         Returns
#         -------
#         None
#         """
#         socket = self.game.client.socket

#         name = pickle.dumps(self.current_name.get())
#         size = comm.size_as_bytes(name)
#         comm.send_data(socket, size)
#         comm.send_data(socket, name)

#         self.receive_name_feedback()

#     def quit(self):
#         """
#         Send a message to server indicating the intention to quit and then quit.
        
#         Returns
#         -------
#         None
#         """
#         self.game.running = False

#         socket = self.game.client.socket
#         quit_msg = pickle.dumps(comm.Message.QUIT)
#         size = comm.size_as_bytes(quit_msg)
#         comm.send_data(socket, size)
#         comm.send_data(socket, quit_msg)

#         root.destroy()

#     def populate(self):
#         """
#         Create the menu and its widgets

#         Return
#         ------
#         None
#         """
#         frame = ttk.Frame(root, padding=10)
#         frame.pack()

#         naming_frame = ttk.Frame(frame)
#         naming_frame.pack()
#         ttk.Label(naming_frame, text = "Display Name: ").pack(side=tkinter.LEFT)
#         naming_entry = Entry(naming_frame, width=25, textvariable=self.current_name)
#         naming_entry.pack(side=tkinter.LEFT)

#         self.name_feedback = ttk.Label(frame, text = "")
#         self.name_feedback.pack(pady=10)

#         buttons_frame = ttk.Frame(frame)
#         buttons_frame.pack(pady=5)
#         ttk.Button(buttons_frame, text='Play', command=self.send_name).pack(side=tkinter.LEFT, padx=3)
#         ttk.Button(buttons_frame, text='Quit', command=self.quit).pack(side=tkinter.LEFT, padx=3)

class Game():
    """
    Represents the client's view of the game.

    Attributes
    ----------
    camera (tuple[int, int]):
        The width and height of the player's camera

    board (tuple[int, int]):
        The width and height of the playing field

    client (Client):
        The connection to the server

    running (Boolean):
        Whether the game is running or not

    radio (MusicPlayer):
        Allows for audio playback

    leaderboard_font (pygame.font.Font):
        Font style and size

    Methods
    -------
    start()
    show_leaderboard(leaderboard)
    render_bounds(head)
    draw_eyes(head, rect)
    render(game_data)
    get_direction()
    game_loop()
    """

    def __init__(self, client, radio):
        """Initialize the game"""
        pygame.init()
        self.camera = (500, 500)
        self.board = (1000, 1000)
        self.client = client
        self.running = True
        self.radio = radio
        self.leaderboard_font = pygame.font.Font(resource_path('./fonts/arial_bold.ttf'), 10)

    def start(self):
        """Create the game window."""
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        flags = DOUBLEBUF
        self.window = pygame.display.set_mode(self.camera, flags, 16)

    def show_leaderboard(self, leaderboard):
        """
        Display the leaderboard.

        Parameters
        ----------
        leaderboard (list):
            A list of LeaderboardEntry objects. Used to display the leaderboard.

        Return
        ------
        None
        """
        top = 8
        for i, entry in enumerate(leaderboard):
            record_string = f'{i + 1}.   {entry.name}   {entry.score}'
            record = self.leaderboard_font.render(record_string, True, (255, 255, 255))
            record_rect = record.get_rect()
            record_rect.topleft = (8, top)
            self.window.blit(record, record_rect)
            top += 13
        
    def show_quit(self):
        quit_string = 'Press ESC to quit'
        quitmsg = self.leaderboard_font.render(quit_string, True, (255, 255, 255))
        quit_rect = quitmsg.get_rect()
        quit_rect.topleft = (410, 8)
        self.window.blit(quitmsg, quit_rect)
        
    def render_bounds(self, head):
        """
        Show unreachable area in a different color.

        This only occurs if the unreachable area is viewable in the player's camera.
        The head is used as a basis to determine the thickness of the rendered unreachable area.
        The closer the head is to the area, the thicker the rendered area will be.

        Parameters
        ----------
        head (CellData):
            A minimal representation of the head object in the server

        Return
        ------
        None
        """
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
        """
        Draw a pair of eyes for a snake

        Parameters
        ----------
        head (CellData):
            A minimal representation of head object
        rect (tuple[int, int, int, int]):
            A tuple with x positon, y position, x width, 
            and y width respectively. Represents the 
            position of the head according to the client's
            point of view (not the true position).

        Return
        ------
        None
        """
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
        """
        Render all objects viewable in the player's camera.

        Parameters
        ----------
        game_data (GameData):
            Minimal representation of the data needed to render the current frame

        Return
        ------
        None
        """
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
        self.show_quit()
        pygame.display.flip()

    def get_direction(self):
        """
        Get the direction based on user input.

        Direction is represented as a tuple of two ints.
        Each int has a value of either -1, 0, or 1.

        -1 means left in the first tuple element and up in the second.
        1 means right in the first tuple element and down in the second.
        0 means no horizontal movement in the first tuple element.
        0 means no vertical movement in the second tuple element.

        Return
        ------
        Tuple[int, int] with the first element representing horizontal direction
        and the second element representing vertical direction.
        """
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
        """
        Game loop.

        Note that the actual game loop occurs on the server side.
        This loop only detects input (such as movement and quitting),
        communicates with server, renders the game, and plays sound.

        Return
        ------
        None
        """
        while self.running:
            msg = None
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu()
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
    """
    A class that allows for audio playback.

    Attributes
    ----------
    pellet_sound (pygame.mixer.Sound):
        Sound for food pellet collision

    self_collision (pygame.mixer.Sound):
        Sound for collision with self or other snakes
    """

    def __init__(self, song):
        """
        Start a thread to play background music.

        Parameters
        ----------
        song (str):
            Filename of the music to be played

        Return
        ------
        None
        """
        pygame.mixer.init()

        #this could be generalized and made into a dictionary for each file so that more sounds could be added without affecting this class
        self.pellet_sound = pygame.mixer.Sound(resource_path("sound/pellet_sound.mp3"))
        self.self_collision = pygame.mixer.Sound(resource_path("sound/self_collision.mp3"))
        Thread(target=self.play_song, args=(song,)).start()
        
    def play_song(self, song):
        """
        Play background music indefinitely.

        Parameters
        ----------
        song (str):
            Filename of the music to be played

        Return
        ------
        None
        """
        pygame.mixer.music.load(song)
        #provide -1 so the song will loop
        pygame.mixer.music.play(-1)

    def play_sound(self, sound):
        """
        Play a sound once.

        Parameters
        ----------
        sound (comm.Message):
            An indicator of the type of sound to play

        Return
        ------
        None
        """
        if sound == comm.Message.PELLET_EATEN:
            self.pellet_sound.play()
        elif sound == comm.Message.SELF_COLLISION or sound == comm.Message.OTHER_COLLISION:
            self.self_collision.play()

def main():
    #start pygame
    pygame.init()

    #start the music
    radio = MusicPlayer(resource_path("sound/snake_hunt.mp3"))

    #create game window
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    #variables NOTE: some things, like font, need to be built after a display
    font = pygame.font.SysFont("signpainter", 40)
    game_paused = False
    game_state = "title"
    TEXT_COL = (255, 255, 255)
    BUTTON_COL = (200,200,200)
    BKGD_COL = (100,100,100)
    run = True
    name = None
    ip = None
    port = None
    connected = False

    #make banner, menu, and elements
    '''
    SnakeBanner(screen,background_color, edge_offset,  points, xblocks, yblocks, font)
    Button(text, font, text_color, background_color, rect, screen, state)
    Menu(screen,background_color, edge_offset, state)

    '''
    #title
    snake_banner = SnakeBanner(screen, BKGD_COL, 10, POINTS, 14, 10, font)
    #menu
    pause_menu = MenuScreen(screen, (150,150,150), 50, "menu")
    #buttons
    title_button = Button("Title Screen", font, TEXT_COL, BUTTON_COL,              (100, 90, 200, 50), screen, "title")
    quit_button = Button("quit", font, TEXT_COL, BUTTON_COL,                (410, 90, 100, 50), screen, "quit")
    connect_button = Button("connect", font, TEXT_COL, BUTTON_COL,          (410, 260, 200, 50), screen, "connecting")
    name_checking_button = Button("check name", font, TEXT_COL, BUTTON_COL, (410, 400, 200, 50), screen, "name_checking")
    #inputs
    input_port = InputDisplay("port", font, TEXT_COL, BUTTON_COL, (100, 200, 200, 50), screen, "port_input", maxLen = 4,allowedChars= ['0','1','2','3','4','5','6','7','8','9'])
    input_ip = InputDisplay("ip", font, TEXT_COL, BUTTON_COL,     (100, 260, 200, 50), screen, "ip_input", maxLen = 15, allowedChars=['0','1','2','3','4','5','6','7','8','9','.'])
    input_name = InputDisplay("name", font, TEXT_COL, BUTTON_COL, (100, 400, 200, 50), screen, "name_input", maxLen = 10)



    #fill the pause menu with buttons
    pause_menu.set_elements((title_button, quit_button, input_name, input_ip, input_port, connect_button, name_checking_button))

    #place holder because it takes like 10 seconds to quit lol
    quitting = Button("quitting", font, TEXT_COL, BKGD_COL, (50,50,SCREEN_WIDTH-100,SCREEN_HEIGHT-100), screen, "quitting")

    #make a client
    client = Client()

    #start the clock
    clock = pygame.time.Clock()
    
    #main loop
    while run is True:

        #make background full red
        screen.fill((255,0,0))

        #get position of the mouse and if it was clicked
        pos = pygame.mouse.get_pos()
        clicked = False

        #input character for the input
        inputChar = 0

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "title":
                    game_state = "menu"
                else:
                    inputChar = event.key
            if event.type == pygame.QUIT:
                run = False

        #check for state to display menus
        if game_state == "title":
            #screen.blit(banner_words, (0,0))
            clock.tick(15)
            snake_banner.draw()
            
        #main menu
        elif game_state == "menu":
            pause_menu.draw()
            if clicked:
                game_state = pause_menu.check(pos)

        elif game_state == "quit":
            quitting.draw()
            run = False

        #each of the inputs
        elif game_state == "ip_input":
            pause_menu.draw()
            if clicked:
                game_state = pause_menu.check(pos)
            if inputChar == pygame.K_BACKSPACE:
                input_ip.removeChar()
            else:
                input_ip.addChar(inputChar)
                ip = input_ip.text
                #print("ip: ", ip)

            
        elif game_state == "port_input":
            pause_menu.draw()
            if clicked:
                game_state = pause_menu.check(pos)
            if inputChar == pygame.K_BACKSPACE:
                input_port.removeChar()
            else:
                input_port.addChar(inputChar)
                

        elif game_state == "connecting":
            pause_menu.draw()
            #connection works, get the name of the user
            if connected == True:
                game_state = "menu"
            elif client.connect((input_ip.text, int(input_port.text))):
                #print("connection success")
                game_state = "menu"
                connected = True
            else:
                game_state = "menu"

            
        elif game_state == "name_input":
            pause_menu.draw()
            if clicked:
                game_state = pause_menu.check(pos)
            if inputChar == pygame.K_BACKSPACE:
                input_name.removeChar()
            else:
                input_name.addChar(inputChar)
                name = input_name.text
                #print("name: ", name)

        elif game_state == "name_checking":
            pause_menu.draw()
            if connected:
                if client.check_name(name):
                    game_state = "play"
                    print("game state is now connected")
                else:
                    game_state = "menu"
                    print("name already taken")
            else:
                game_state = "menu"
                print("cannot enter name, not yet connected to the server")

        if game_state == "play":
            game = Game(client, radio)
            game.start()
            game.game_loop()
        

        #print(game_state)
        #print("clicked: ", clicked)
        pygame.display.flip()
        clock.tick(18)
        
    pygame.event.get()
    pygame.quit()


    
##    pygame.init()
##    screen = pygame.display.set_mode((800, 800))
##    pygame.display.set_caption("Main Menu")

    #load button images
##    resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
##    options_img = pygame.image.load("images/button_options.png").convert_alpha()
##    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
##    back_img = pygame.image.load('images/button_back.png').convert_alpha()

    #create button instances
##    resume_button = button.Button(304, 125, resume_img, 1)
##    options_button = button.Button(297, 250, options_img, 1)
##    quit_button = button.Button(336, 375, quit_img, 1)
##    back_button = button.Button(332, 450, back_img, 1)

##    game_over = True
##    menu_state = "main"
##    run = True
##    while run:
##        screen.fill((255,0,0))
##
##        #check if game is over (or hasn't begun yet)
##        if game_over == True:
##            #check menu state
##            if menu_state == "main":
##                #draw pause screen buttons
##                if resume_button.draw(screen):
##                    game_over = False
##                if options_button.draw(screen):
##                    menu_state = "options"
##                if quit_button.draw(screen):
##                    run = False
##            #check if the options menu is open
##            if menu_state == "options":
##                #draw the different options buttons
##                if back_button.draw(screen):
##                    menu_state = "main"
##            pygame.display.update()
##        else: #if user decided to start game/enter server
##            runclient()
##
##
##        
##
##    pygame.quit()
##    sys.exit()
##
# def runclient(ip=None, port=None, name=None): 
#     client = Client()
#     client.input_addr()
#     if not client.connect():
#         return

#     game = Game(client, radio)
    
#     #PauseMenu(game)

#     game.start()
#     game.game_loop()
    
if __name__ == '__main__':
    main()
    
    



