import pygame
from random import randint
from math import floor as flr

BOARD = (500,500)
CELL = 10
SPEED = CELL
COLS = BOARD[0]/CELL
ROWS = BOARD[1]/CELL

class Player():
    def __init__(self, name, snake):
        self.name = name
        self.snake = snake
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
    def __init__(self, position, length, xdir, ydir, bounds):
        #(west,north,east,south) points
        self.bounds = bounds
        self.color = (0, 255, 0)
        self.body = []
        self.turns = {}
        self.position = position
        self.length = length
        self.initialize(self.position, xdir, ydir)

    # Initializes all parts of the snake based on length
    def initialize(self, position, xdir, ydir):
        posx = position[0]
        for i in range(self.length):
            self.body.append(BodyPart((posx, position[1]), xdir, ydir, self.color))
            posx -= SPEED
        self.head = self.body[0]

    # Reset snake so player can play again once they die
    def reset(self, position):
        self.body = []
        self.turns = {}
        self.position = position
        self.body.append(self.head)
        self.length = 1
        self.dirnx = 0
        self.dirny = 1
        
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
            print(part.position)
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
    def grow(self, amount):
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
                self.body.append(BodyPart((previous.position[0]-(i+1)*width,previous.position[1]), xdir, ydir, self.color))
            # if the previous part is moving left, append
            # this part to the right of it with the same direction
            elif xdir == -1 and ydir == 0:
                self.body.append(BodyPart((previous.position[0]+(i+1)*width,previous.position[1]), xdir, ydir, self.color))
            # if the previous part is moving up, append
            # this part to the bottom of it with the same direction
            elif xdir == 0 and ydir == 1:
                self.body.append(BodyPart((previous.position[0],previous.position[1]-(i+1)*width), xdir, ydir, self.color))
            # if the previous part is moving down, append
            # this part to the top of it with the same direction
            elif xdir == 0 and ydir == -1:
                self.body.append(BodyPart((previous.position[0],previous.position[1]+(i+1)*width), xdir, ydir, self.color))
    
    def check_body_collision(self):
        #Snake dies and game is over for user when snake collides with itself
        for part in range(len(self.body)):
            if self.body[part].position in list(map(lambda z:z.position,self.body[part+1:])):
                self.reset(self.position)
                break

#pellet object control
class Pellet():
    def __init__(self):
        self.position = self.setPos()
        self.eaten = False
        self.color = (50, 200, 255)
        self.width = CELL
        self.height = CELL

    def setPos(self):
        xpos = randint(1, COLS-1)*CELL
        ypos = randint(1,ROWS-1)*CELL
        return (xpos, ypos)

    def getPos(self):
        return self.position[0], self.position[1]

    def destroy(self):
        self.position = self.setPos()
        
    # set a pellet's position to a value passed in
    def setDetPos(self,xpos,ypos):
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
    def __init__(self, numPellets):
        self.numPellets = numPellets
        self.availablePositions = self.setPositions()
        self.pellets = self.genPellets()
        
    def genPellets(self):
        pellets = []
        for i in range(self.numPellets):
            pel = Pellet()
            # get a random available position then remove it from the list of 
            # available positions (-1 added to avoid error by popping out of range)
            pos = self.availablePositions.pop(randint(0,len(self.availablePositions)-1))
            # manually set the position of the pellet to the random position
            pel.setDetPos(pos[0],pos[1])
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
        pos = self.availablePositions.pop(randint(0,len(self.availablePositions)))
        pel2 = Pellet()
        # generate a new pellet
        pel2.setDetPos(pos[0], pos[1])
        # add the deleted pellet's position back to the available positions
        self.availablePositions.append(pel.position)
        self.pellets.append(pel2)