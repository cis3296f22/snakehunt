import pickle
import comm
from random import randint
from math import floor as flr
from pygame.time import Clock
from gamedata import *
from socket import SHUT_RDWR

BOARD = (1000,1000)
CELL = 10
SPEED = 10
COLS = BOARD[0]/CELL
ROWS = BOARD[1]/CELL
MAX_NAME_LENGTH = 32

class Player():
    def __init__(self, id, snake, socket):
        self.id = id
        self.snake = snake
        self.socket = socket
        self.dead = True
    def set_name(self, name):
        self.name = name

# A single part of a snake.
class BodyPart():
    width = CELL
    def __init__(self, position, xdir, ydir, color):
        self.position = position
        self.xdir = xdir
        self.ydir = ydir
        self.color = color

    def set_direction(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir

    def move(self):
        self.position = (self.position[0] + SPEED * self.xdir, self.position[1] + SPEED * self.ydir)    
    
class Snake():
    MAX_INVINCIBLE_LENGTH = 3
    INITIAL_LENGTH = 1
    def __init__(self, position, length, xdir, ydir, bounds):
        #(west,north,east,south) points
        self.bounds = bounds
        self.color = RandomPellets.val_1[0]
        self.body = []
        self.turns = {}
        if length < 1: length = 1
        self.length = length
        self.initialize(position, xdir, ydir)

    # Initializes all parts of the snake based on length
    def initialize(self, position, xdir, ydir):
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

    # Reset snake so player can play again once they die
    def reset(self, position):
        self.body = []
        self.turns = {}
        self.length = self.INITIAL_LENGTH
        self.initialize(position, self.head.xdir, self.head.ydir)
        
    # Change direction of head of snake based on input
    def change_direction(self, direction):
        if direction == None: return

        if self.head.xdir != -direction[0] or self.head.ydir != -direction[1]:
            if self.head.xdir != -direction[0]:
                self.head.xdir = direction[0]
            if self.head.ydir != -direction[1]:
                self.head.ydir = direction[1]
            self.turns[self.head.position[:]] = [self.head.xdir, self.head.ydir]
    
    # Move every part of the snake.
    # If a part is at a position where a previous turn occurred, set its direction to the
    # direction of the previous turn.
    # When the last part passes a turn, the turn is removed from the dictionary.
    def move(self):
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

    # Increase length by amount and add the corresponding
    # amount of body parts to the snake
    def grow(self, amount, color):
        size = self.length
        self.length = size + amount
        previous = self.body[size-1]
        
        # initialize elements from the previous part for readability
        xdir = previous.xdir
        ydir = previous.ydir
        width = previous.width
        
        for i in range(amount):
            # if the previous part is moving right, append
            # this part to the left of it with the same direction
            if xdir == 1 and ydir == 0:
                self.body.append(BodyPart((previous.position[0]-(i+1)*width,previous.position[1]), xdir, ydir, color))
            # if the previous part is moving left, append
            # this part to the right of it with the same direction
            elif xdir == -1 and ydir == 0:
                self.body.append(BodyPart((previous.position[0]+(i+1)*width,previous.position[1]), xdir, ydir, color))
            # if the previous part is moving up, append
            # this part to the bottom of it with the same direction
            elif xdir == 0 and ydir == 1:
                self.body.append(BodyPart((previous.position[0],previous.position[1]-(i+1)*width), xdir, ydir, color))
            # if the previous part is moving down, append
            # this part to the top of it with the same direction
            elif xdir == 0 and ydir == -1:
                self.body.append(BodyPart((previous.position[0],previous.position[1]+(i+1)*width), xdir, ydir, color))
    
    # Returns true if this snake's head collided with its own body, false otherwise.
    def collides_self(self):
        if self.is_invincible():
            return False
        for part in range(len(self.body)):
            if self.body[part].position in list(map(lambda z:z.position,self.body[part+1:])):
                return True
        return False
    
    # Returns true if this snake's head collided with another snake's body, false otherwise.
    def collides_other(self, other_snakes):
        if self.is_invincible():
            return False
        for snake in other_snakes:
            for part in snake.body:
                if self.head.position == part.position and not snake.is_invincible():
                    return True
        return False
        
    # Returns true if the given position would collide with the snake, false otherwise.
    def collides_position(self, position):
        for part in self.body:
            if part.position == position:
                return True
        return False
    
    # Returns true if this snake cannot die, false otherwise.
    def is_invincible(self):
        if len(self.body) <= self.MAX_INVINCIBLE_LENGTH:
            return True
        return False
    
    # Turn a snake into food pellets
    # Every other body part of the snake is converted to a food pellet
    def cook(self):
        remains = []
        for i in range(1, len(self.body), 2):
            pel = Pellet(RandomPellets.val_1, is_remains=True)
            pel.setPos(self.body[i].position[0], self.body[i].position[1])
            remains.append(pel)
        return remains

    # Get the body parts of this snake that are visible by the given camera.
    def get_visible_bodyparts(self, camera, camera_target):
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

#pellet object control
class Pellet():
    def __init__(self, color_val, is_remains=False):
        self.position = self.setRandomPos()
        self.color = color_val[0]
        self.val = color_val[1]
        self.is_remains = is_remains    # Is this pellet part of the remains of a dead snake?
        self.width = CELL
        self.height = CELL

    def setRandomPos(self):
        xpos = randint(1, COLS-1)*CELL
        ypos = randint(1,ROWS-1)*CELL
        return (xpos, ypos)

    def getPos(self):
        return self.position[0], self.position[1]
        
    # set a pellet's position to a value passed in
    def setPos(self,xpos,ypos):
        self.position = [xpos,ypos]

# Generates multiple pellets in random locations such that they do not
# overlap
#
# IMPORTANT NOTE
# For a 32 bit system, the maximum array size in python is 536,870,912
# elements. Since this implementation is dependent on the board and cell size,
# this will not work for anything larger than a 23170 by 23170 size board/cell 
# ratio for 32 bit systems.
class RandomPellets():
    val_1 = ((150,255,150), 1)
    val_2 = ((150,150,255), 2)
    val_3 = ((255,150,150), 3)

    def __init__(self, numPellets):
        self.numPellets = numPellets
        self.availablePositions = self.setPositions()
        self.pellets = self.genPellets()

    def setColor(self):
        val = randint(0, 10)
        if val == 10:
            return self.val_3
        elif val > 7:
            return self.val_2
        else:
            return self.val_1
        
    def genPellets(self):
        pellets = []
        for i in range(self.numPellets):
            pel = Pellet(self.setColor())
            # get a random available position then remove it from the list of 
            # available positions (-1 added to avoid error by popping out of range)
            pos = self.availablePositions.pop(randint(0,len(self.availablePositions)-1))
            # manually set the position of the pellet to the random position
            pel.setPos(pos[0],pos[1])
            pellets.append(pel)
        return(pellets)
    
    # initializes all possible pellet positions, i.e. every cell
    def setPositions(self):
        positions = []
        for i in range(flr(ROWS)):
            for j in range(flr(COLS)):
                positions.append([i*CELL, j*CELL])
        return(positions)
    
    def getPositions(self):
        positions = []
        for pellet in self.pellets:
            positions.append(pellet.position)
        return(positions)
    
    def resetPellet(self,pel):
        # delete the pellet
        self.pellets.remove(pel)
        # get a new position from the list of availble positions and remove it
        pos = self.availablePositions.pop(randint(1,len(self.availablePositions)-1))
        color_val = self.setColor()
        pel2 = Pellet(color_val)
        # generate a new pellet
        pel2.setPos(pos[0], pos[1])
        # add the deleted pellet's position back to the available positions
        self.availablePositions.append(pel.position)
        self.pellets.append(pel2)

    def addPellets(self, pellets):
        self.pellets = self.pellets + pellets

class Camera():
    def __init__(self, width, height):
        self.dimensions = (width, height)

    # Check if 'object_pos' is within the bounds of the camera
    # 'target_pos' is the position of the target of the camera,
    # that is, the object that the camera is following.
    # NOTE: this function assumes that the target is meant to
    # be centered, and does its checking based on that assumption.
    def within_bounds(self, object_pos, target_pos):
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
    def __init__(self, server):
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
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)
        player.socket.shutdown(SHUT_RDWR)
        player.socket.close()

    def get_leaderboard(self):
        leaderboard = []
        for player in self.players:
            leaderboard.append(LeaderboardEntry(player.name, player.snake.length))
        leaderboard.sort(key=lambda x: x.score, reverse=True)
        if len(leaderboard) > 10:
            leaderboard = leaderboard[0:10]
        return leaderboard

    def get_visible_snakes(self, receiver_player, camera_target):
        snakes = []
        for player in self.players:
            if player != receiver_player:
                snakes.append(player.snake.get_visible_bodyparts(self.camera, camera_target))
        return snakes

    def get_visible_pellets(self, camera_target):
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
    
    # Get a random position that does not collide with an existing snake
    def get_random_position(self):
        while True:
            x_pos = randint(0, COLS - 1) * CELL
            y_pos = randint(0, ROWS - 1) * CELL
            position = (x_pos, y_pos)
            for player in self.players:
                if player.snake.collides_position(position):
                    continue
            break
        return position

    def game_loop(self):
        clock = Clock()
        while self.running:
            sound = None
            pos = self.random_pellets.getPositions()
            snakes = []
            dead_snakes = []

            # List of all snakes. Each player will copy this list
            # and remove their own snake from it. This is so that
            # each player can detect collision with other snakes.
            for player in self.players:
                snakes.append(player.snake)

            # Move each player
            for player in self.players:
                player.snake.move()

            # Check for collision with pellets, self, and other snakes for each snake
            for player in self.players:
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

            # Turn the dead snakes to food and reset them
            for snake in dead_snakes:
                remains = snake.cook()
                self.random_pellets.addPellets(remains)
                random_pos = self.get_random_position()
                snake.reset(random_pos)

            # Gather data to send to each client
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

            # Framerate
            clock.tick(18)
