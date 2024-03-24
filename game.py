import pickle
import comm
from random import randint
from math import floor as flr
from pygame.time import Clock
from gamedata import *
from socket import SHUT_RDWR
from reddit_request import reddit as red

BOARD = (1000,1000)
CELL = 10
SPEED = 10
COLS = BOARD[0]/CELL
ROWS = BOARD[1]/CELL
MAX_NAME_LENGTH = 32

class Player():
    """
    A connected player.

    Attributes
    ----------
    id (int):
        A unique identifyer
    
    snake (Snake):
        The player's snake

    socket (socket.socket):
        Player's connection
    
    name (str):
        Keeps track of the current name entered by user
    """

    def __init__(self, id, snake, socket):
        """Create player."""
        self.id = id
        self.snake = snake
        self.socket = socket
        self.name = None

    def set_name(self, name):
        """
        Set the player's name

        Parameters
        ----------
        name (str):
            The name to set

        Return
        ------
        None
        """
        self.name = name

class BodyPart():
    """
    A part of a snake.

    Attributes
    ----------
    position (tuple[int, int]):
        x and y positions, respectively

    xdir (int):
        Horizontal direction (-1 left, 0 still, 1 right)

    ydir (int):
        Vertical direction (-1 up, 0 still, 1 down)

    color (tuple[int, int, int]):
        Values for red, green, and blue (RGB), respectively

    Methods
    -------
    set_direction(xdir, ydir)
    move()
    """

    width = CELL
    def __init__(self, position, xdir, ydir, color):
        """Create body part."""
        self.position = position
        self.xdir = xdir
        self.ydir = ydir
        self.color = color

    def set_direction(self, xdir, ydir):
        """
        Set the horizontal and veritcal direction

        Parameters
        ----------
        xdir (int):
            The horizontal direction (see BodyPart's documentation for details)
        ydir (int):
            The vertical direction (see BodyPart's documentation for details)

        Return
        ------
        None
        """
        self.xdir = xdir
        self.ydir = ydir

    def move(self):
        """
        Move the part based on speed and direction.

        Return
        ------
        None
        """
        self.position = (self.position[0] + SPEED * self.xdir, self.position[1] + SPEED * self.ydir)    
    
class Snake():
    """
    A class representing a snake game object.

    Attributes
    ----------
    bounds (tuple[int, int, int, int]):
        Borders of the playable area. Left, right, up and down respectively
    
    color (tuple[int, int, int]):
        Initial color of the snake in RGB

    body (list):
        List of BodyPart objects representing the snake's body parts

    turns (dict):
        Dictionary containing positions in which the head has turned. Used to turn remaining body parts

    length (int):
        Initial length of the snake
    
    Methods
    -------
    initialize(position, xdir, ydir)
    reset(position)
    change_direction(direction)
    move()
    grow(amount, color)
    collides_self()
    collides_other(other_snakes)
    collides_position(position)
    cook()
    get_visible_bodyparts(camera, camera_target)
    """

    MAX_INVINCIBLE_LENGTH = 3
    INITIAL_LENGTH = 1
    def __init__(self, position, length, xdir, ydir, bounds):
        """Create snake."""
        self.bounds = bounds
        self.color = RandomPellets.val_1[0]
        self.body = []
        self.turns = {}
        if length < 1: length = 1
        self.length = length
        self.initialize(position, xdir, ydir)

    def initialize(self, position, xdir, ydir):
        """
        Create all of the snake's body parts.

        Parameters
        ----------
        position (tuple[int, int]):
            The position of the snake's head

        xdir (int):
            Horizontal direction (see BodyPart's documentation for details)

        ydir (int):
            Vertical direction (see BodyPart's documentation for details)

        Return
        ------
        None
        """
        posx = position[0]
        posy = position[1]
        for i in range(self.length):
            self.body.append(BodyPart((posx, posy), xdir, ydir, self.color))
            if xdir == 1:
                posx -= SPEED
            elif xdir == -1:
                posx += SPEED
            elif ydir == 1:
                posy -= SPEED
            else:
                posy += SPEED
        self.head = self.body[0]

    def reset(self, position):
        """
        Restore snake to initial length and set its new position.

        Parameters
        ----------
        position (tuple[int, int]):
            New position

        Return
        ------
        None
        """
        self.body = []
        self.turns = {}
        self.length = self.INITIAL_LENGTH
        self.initialize(position, self.head.xdir, self.head.ydir)
        
    def change_direction(self, direction):
        """
        Change snake's head's direction.

        Parameters
        ----------
        direction (tuple[int, int]):
            New direction or None if direction hasn't changed.

        Return
        ------
        None
        """
        if direction == None: return

        if self.head.xdir != -direction[0] or self.head.ydir != -direction[1]:
            if self.head.xdir != -direction[0]:
                self.head.xdir = direction[0]
            if self.head.ydir != -direction[1]:
                self.head.ydir = direction[1]
            self.turns[self.head.position[:]] = [self.head.xdir, self.head.ydir]
    
    def move(self):
        """
        Move each body part of the snake.

        Head moves based on the direction, and so do other parts.

        Other parts are affected by the head's movement. When a part hits a position
        that the head has turned at, it mimics the head's turn.

        Return
        ------
        None
        """
        for i, part in enumerate(self.body):
            pos = part.position[:]
            if pos in self.turns:
                turn = self.turns[pos]
                part.set_direction(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(pos)
            part.move()
            if part.position[0] < self.bounds['left']:
                part.position = (self.bounds['right'] - CELL, part.position[1])
            elif part.position[0] > self.bounds['right'] - 1:
                part.position = (self.bounds['left'], part.position[1])
            elif part.position[1] > self.bounds['down'] - 1:
                part.position = (part.position[0], self.bounds['up'])
            elif part.position[1] < self.bounds['up']:
                part.position = (part.position[0], self.bounds['down'] - CELL)

    def grow(self, amount, color):
        """
        Add more BodyPart objects to the snake

        Parameters
        ----------
        amount (int):
            Number of parts to add

        color (tuple[int, int, int]):
            Color of the parts to add.

        Return
        ------
        None
        """
        size = self.length
        self.length = size + amount
        previous = self.body[size-1]
        
        xdir = previous.xdir
        ydir = previous.ydir
        width = previous.width
        # If the amount is less than 0, then it has eaten the "bad pellet", which removes one body part
        if amount >= 0:
            for i in range(amount):
                if xdir == 1 and ydir == 0:
                    self.body.append(BodyPart((previous.position[0]-(i+1)*width,previous.position[1]), xdir, ydir, color))
                elif xdir == -1 and ydir == 0:
                    self.body.append(BodyPart((previous.position[0]+(i+1)*width,previous.position[1]), xdir, ydir, color))
                elif xdir == 0 and ydir == 1:
                    self.body.append(BodyPart((previous.position[0],previous.position[1]-(i+1)*width), xdir, ydir, color))
                elif xdir == 0 and ydir == -1:
                    self.body.append(BodyPart((previous.position[0],previous.position[1]+(i+1)*width), xdir, ydir, color))
        else:
            self.body.pop()
            
    

    def collides_self(self):
        """
        Check if snake collided with its own body.

        Return
        ------
        True if the snake has collided with its own body, false otherwise.
        """
        if self.is_invincible():
            return False
        for part in range(len(self.body)):
            if self.body[part].position in list(map(lambda z:z.position,self.body[part+1:])):
                return True
        return False
    

    def collides_other(self, other_snakes):
        """
        Check if snake collided with another snake.

        Parameters
        ----------
        other_snakes (list):
            List of all other snakes in the game.

        Return
        ------
        True if the snake has collided with another snake, False otherwise.
        """
        if self.is_invincible():
            return False
        for snake in other_snakes:
            for part in snake.body:
                if self.head.position == part.position and not snake.is_invincible():
                    return True
        return False
        
    def collides_position(self, position):
        """
        Check if the snake collides with the given position.

        Parameters
        ----------
        position (tuple[int, int]):
            A position.

        Return
        ------
        True if the snake collides with the given position, False otherwise.
        """
        for part in self.body:
            if part.position == position:
                return True
        return False
    
    def is_invincible(self):
        """
        Check if the snake cannot die.

        Return
        ------
        True if the snake cannot die, False otherwise.
        """
        if len(self.body) <= self.MAX_INVINCIBLE_LENGTH:
            return True
        return False
    
    def cook(self):
        """
        Turn the snake's body into consumable food pellets.

        Return
        ------
        A list containing Pellet objects.
        """
        remains = []
        for i in range(1, len(self.body), 2):
            pel = Pellet(RandomPellets.val_1, is_remains=True)
            pel.setPos(self.body[i].position[0], self.body[i].position[1])
            remains.append(pel)
        return remains

    def get_visible_bodyparts(self, camera, camera_target):
        """
        Get the body parts of this snake that are visible by a given camera.

        Parameters
        ----------
        camera (Camera):
            The camera for which to check visibility of snake

        camera_target (tuple[int, int]):
            Position of the camera's target

        Return
        ------
        A list of body parts of this snake that are within the camera's lens
        """
        body_parts = []
        for body_part in self.body:
            if not camera.within_bounds(body_part.position, camera_target):
                continue
            body_parts.append(
                CellData(
                    body_part.position,
                    body_part.color,
                    body_part.width,
                    direction = (body_part.xdir, body_part.ydir) if body_part == self.head else None
                )
            )
        return body_parts

class Pellet():
    """
    A class representing a consumable food object.

    Attributes
    ----------
    position (tuple[int, int]):
        Position of the pellet

    color (tuple[int, int, int]):
        Color of the pellet

    val (int):
        Number of body parts that a snake gets by consuming this pellet

    is_remains (Boolean):
        Whether this pellet is the remains of a dead snake

    width (int):
        Width of pellet

    height (int):
        Height of pellet
    
    Methods
    -------
    setRandomPos()
    getPos()
    setPos()
    """
    def __init__(self, color_val, is_remains=False):
        """Create pellet object."""
        self.position = self.setRandomPos()
        self.color = color_val[0]
        self.val = color_val[1]
        self.is_remains = is_remains    # Is this pellet part of the remains of a dead snake?
        self.width = CELL
        self.height = CELL
        #self.id = iD

    def setRandomPos(self):
        """
        Give the pellet a random position.

        Return
        ------
        A tuple [int, int] representing the random position
        """
        xpos = randint(1, int(COLS)-1)*CELL
        ypos = randint(1,int(ROWS)-1)*CELL
        return (xpos, ypos)

    def getPos(self):
        """
        Get the pellet's position.

        Return
        ------
        A tuple [int, int] current position
        """
        return self.position[0], self.position[1]
        
    def setPos(self,xpos,ypos):
        """
        Set the pellet's position.

        Parameters
        ----------
        xpos (int):
            x position

        ypos (int):
            y position

        Return
        ------
        None
        """
        self.position = [xpos,ypos]

class RandomPellets():
    """
    A class that creates multiple pellets at random non-overlapping positions.

    This class maintains the pellets by restoring them at new positions when consumed.

    IMPORTANT NOTE
    For a 32 bit system, the maximum array size in python is 536,870,912
    elements. Since this implementation is dependent on the board and cell size,
    this will not work for anything larger than a 23170 by 23170 size board/cell 
    ratio for 32 bit systems.

    Attributes
    ----------
    numPellets (int):
        Number of pellets to generate

    availablePositions (list):
        List of available positions

    pellets (list):
        List of pellets
    
    Methods
    -------
    setColor()
    genPellets()
    setPositions()
    getPositions()
    resetPellet(pel)
    addPellets(pellets)
    """

    val_1 = ((150,255,150), 1)
    val_2 = ((150,150,255), 2)
    val_3 = ((255,150,150), 3)
    val_4 = ((0, 0, 150), 20)
    val_5 = ((150, 0, 0), -1) # the "poisonous pellets"
    #val_5 = ((0,200, 0), -2)

    def __init__(self, numPellets):
        """Create RandomPellets object."""
        self.numPellets = numPellets
        self.availablePositions = self.setPositions()
        self.pellets = self.genPellets()

    def setColor(self):
        """
        Give the pellet a random color and value.
    
        Return
        ------
        A tuple containing the color and the value
        """
        val = randint(-1, 20)
        if val == 20:
            #val_4 = ((0, 0, 150), randint(10, 69))
            return self.val_4
        elif val == 10:
            return self.val_3
        elif val > 7:
            return self.val_2
        elif val == -1:
            return self.val_5
        else:
            return self.val_1
        
    def genPellets(self):
        """
        Generate pellets at random positions.

        Return
        ------
        List of pellets generated
        """
        pellets = []
        for i in range(self.numPellets):
            #val = self.setColor()
            pel = Pellet(self.setColor())
            pos = self.availablePositions.pop(randint(0,len(self.availablePositions)-1))
            pel.setPos(pos[0],pos[1])
            pellets.append(pel)
        return(pellets)
    
    def setPositions(self):
        """
        Initialize all possible pellet positions

        Return
        ------
        List of all possible positions
        """
        positions = []
        for i in range(flr(ROWS)):
            for j in range(flr(COLS)):
                positions.append([i*CELL, j*CELL])
        return(positions)
    
    def getPositions(self):
        """
        Get a list of the positions of all pellets.

        Return
        ------
        List
        """
        positions = []
        for pellet in self.pellets:
            positions.append(pellet.position)
        return(positions)
    
    def resetPellet(self,pel):
        """
        Remove a pellet then generate a new one at a random position.

        Parameters
        ----------
        pel (Pellet):
            The pellet to remove

        Return
        ------
        None
        """

        self.pellets.remove(pel)
        pos = self.availablePositions.pop(randint(1,len(self.availablePositions)-1))
        color_val = self.setColor()
        pel2 = Pellet(color_val)
        pel2.setPos(pos[0], pos[1])
        self.availablePositions.append(pel.position)
        self.pellets.append(pel2)

    def addPellets(self, pellets):
        """
        Join the list of pellets with another list of pellets.

        Parameters
        ----------
        pellets (list):
            List of pellets to join

        Return
        ------
        None
        """
        
        self.pellets = self.pellets + pellets

class Camera():
    """
    A class representing a camera.

    This camera keeps its target in the middle.

    Attributes
    ----------
    dimensions (tuple[int, int]):
        Width and height of camera
    
    Methods
    -------
    within_bounds(object_pos, target_pos)
    """

    def __init__(self, width, height):
        """Create a camera object."""
        self.dimensions = (width, height)

    def within_bounds(self, object_pos, target_pos):
        """
        Check if an object is within the camera's sight

        Parameters
        ----------
        object_pos (tuple[int, int]):
            Position of object

        target_pos (tuple[int, int]):
            Position of camera's target

        Return
        ------
        True if object_pos is within camera's sight, False otherwise
        """
        camera_left_edge = target_pos[0] - self.dimensions[0] / 2
        camera_right_edge = target_pos[0] + self.dimensions[0] / 2
        camera_top_edge = target_pos[1] - self.dimensions[1] / 2
        camera_bottom_edge = target_pos[1] + self.dimensions[1] / 2

        if object_pos[0] < camera_left_edge:
            return False
        elif object_pos[0] > camera_right_edge:
            return False
        if object_pos[1] < camera_top_edge:
             return False
        elif object_pos[1] > camera_bottom_edge:
            return False
        return True

class Game():
    """
    Game class

    Attributes
    ----------
    server (Server):
        Game server
    
    players (list):
        List of current players

    camera (Camera):
        Camera object

    random_pellets (RandomPellets):
        Generates the game's pellets

    running (Boolean):
        Whether or not the game is running

    bounds (object):
        Left, right, up and down bounds of the playing field
    
    Methods
    -------
    add_player(player)
    remove_player(player)
    get_leaderboard()
    get_visible_snakes(receiver_player, camera_target)
    get_visible_pellets(camera_target)
    get_random_position()
    game_loop()
    """
    
    def __init__(self, server):
        """Initialize game."""
        self.server = server or None
        self.players = []
        self.camera = Camera(500, 500)
        self.random_pellets = RandomPellets(25)
        self.running = True
        self.bounds = {
            'left': 0,
            'right': BOARD[0],
            'up': 0,
            'down': BOARD[1]
        }

    def add_player(self, player):
        """
        Add player to list of players

        Parameters
        ----------
        player (Player):
            Player to add

        Return
        ------
        None
        """
        self.players.append(player)

    def remove_player(self, player):
        """
        Remove player from list of players and close their socket.

        Parameters
        ----------
        player (Player):
            Player to remove

        Return
        ------
        None
        """
        self.players.remove(player)
        player.socket.shutdown(SHUT_RDWR)
        player.socket.close()

    def get_leaderboard(self):
        """
        Retreive the current state of the leaderboard.

        Return
        ------
        List containing the names and lengths of the top 10 largest snakes
        """

        leaderboard = []
        for player in self.players:
            r = red.get_reddit('programming', 'new', 1, 'hour')
            title = red.get_results(r)
            leaderboard.append(LeaderboardEntry(title, 0))
            leaderboard.append(LeaderboardEntry(player.name, player.snake.length))
        leaderboard.sort(key=lambda x: x.score, reverse=True)
        if len(leaderboard) > 10:
            leaderboard = leaderboard[0:10]
        return leaderboard

    def get_visible_snakes(self, receiver_player, camera_target):
        """
        Get the parts of the snakes that are visible in camera.

        Parameters
        ----------
        receiver_player (Player):
            The receiver of the return value of this function

        camera_target (tuple[int, int]):
            Position of the camera's target, basis for what is and isn't visible

        Return
        ------
        List of snakes
        """
        snakes = []
        for player in self.players:
            if player != receiver_player:
                snakes.append(player.snake.get_visible_bodyparts(self.camera, camera_target))
        return snakes

    def get_visible_pellets(self, camera_target):
        """
        Get the pellets that are visible in camera.

        Parameters
        ----------
        camera_target (tuple[int, int]):
            Position of the camera's target, basis for what is and isn't visible

        Return
        ------
        List of pellets
        """
        pellets = []
        for pellet in self.random_pellets.pellets:
            if not self.camera.within_bounds(pellet.position, camera_target):
                continue
            pellets.append(
                CellData(
                    pellet.position,
                    pellet.color,
                    pellet.width
                )
            )
        return pellets
    
    def get_random_position(self):
        """
        Get a random position within playing field that does not collide with any snake.

        Return
        ------
        A tuple[int, int] containing the position
        """
        while True:
            x_pos = randint(0, int(COLS) - 1) * CELL
            y_pos = randint(0, int(ROWS) - 1) * CELL
            position = (x_pos, y_pos)
            for player in self.players:
                if player.snake.collides_position(position):
                    continue
            break
        return position

    def game_loop(self):
        """
        The game loop

        Return
        ------
        None
        """
        clock = Clock()
        while self.running:
            sound = None
            snakes = []
            dead_snakes = []

            for player in self.players:
                snakes.append(player.snake)

            for player in self.players:
                player.snake.move()

            for player in self.players:
                pos = self.random_pellets.getPositions()
                others = snakes[:]
                snake = player.snake
                others.remove(snake)
                if [snake.head.position[0], snake.head.position[1]] in pos:
                    sound = comm.Message.PELLET_EATEN
                    i = pos.index([snake.head.position[0],snake.head.position[1]])
                    pellet = self.random_pellets.pellets[i]
                    if pellet.is_remains:
                        self.random_pellets.pellets.pop(i)
                    else:
                        self.random_pellets.resetPellet(pellet)
                    snake.grow(pellet.val, pellet.color)
                if snake.collides_self():
                    sound = comm.Message.SELF_COLLISION
                    dead_snakes.append(snake)
                elif snake.collides_other(others):
                    sound = comm.Message.OTHER_COLLISION
                    dead_snakes.append(snake)

            for snake in dead_snakes:
                remains = snake.cook()
                self.random_pellets.addPellets(remains)
                random_pos = self.get_random_position()
                snake.reset(random_pos)

            leaderboard = self.get_leaderboard()
            for player in self.players:
                camera_target = player.snake.head.position
                snake = player.snake.get_visible_bodyparts(self.camera, camera_target)
                other_snakes = self.get_visible_snakes(player, camera_target)
                pellets = self.get_visible_pellets(camera_target)

                game_data = GameData(snake, other_snakes, pellets, leaderboard, sound)
                game_data_serialized = pickle.dumps(game_data)
                try:
                    self.server.send_game_data(player, game_data_serialized)
                except:
                    pass

            clock.tick(18)
