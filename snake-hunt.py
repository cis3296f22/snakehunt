import pygame
from random import randint
##import math
##from math import floor as flr

BOARD = (500,500)
CELL = 25
COLS = BOARD[0]/CELL
ROWS = BOARD[1]/CELL


# A single part of a snake.
class BodyPart():
    speed = 25   # Number of pixels that the part moves per frame
    width = 25
    def __init__(self, position, xdir, ydir, color):
        self.position = position
        self.xdir = xdir
        self.ydir = ydir
        self.color = color

    def set_direction(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir

    def move(self):
        self.position = (self.position[0] + self.speed * self.xdir, self.position[1] + self.speed * self.ydir)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.width - 2, self.width - 2));




class Snake():
    def __init__(self, position, length, xdir, ydir, color, field_dimension):
        self.body = []
        self.turns = {}
        self.position = position
        self.length = length
        self.color = color
        self.field_dimension = field_dimension
        self.initialize(position, xdir, ydir, color)

    # Initializes all parts of the snake based on length
    def initialize(self, position, xdir, ydir, color):
        posx = position[0]
        for i in range(self.length):
            self.body.append(BodyPart((posx, position[1]), xdir, ydir, color))
            posx -= 25
        self.head = self.body[0]

    # Change direction of head of snake based on input
    def change_direction(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.head.xdir != 1:
            self.head.xdir = -1
            self.head.ydir = 0
            self.turns[self.head.position[:]] = [self.head.xdir, self.head.ydir]
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.head.xdir != -1:
            self.head.xdir = 1
            self.head.ydir = 0
            self.turns[self.head.position[:]] = [self.head.xdir, self.head.ydir]
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.head.ydir != 1:
            self.head.xdir = 0
            self.head.ydir = -1
            self.turns[self.head.position[:]] = [self.head.xdir, self.head.ydir]
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.head.ydir != -1:
            self.head.xdir = 0
            self.head.ydir = 1
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
                part.move()
                if i == len(self.body) - 1:
                    self.turns.pop(pos)
            else:
                if part.xdir == -1 and part.position[0] <= 0:
                    part.position = (self.field_dimension[0] - 25 - 1, part.position[1])
                elif part.xdir == 1 and part.position[0] >= self.field_dimension[0] - 1:
                    part.position = (0, part.position[1])
                elif part.ydir == 1 and part.position[1] >= self.field_dimension[1] - 1:
                    part.position = (part.position[0], 0)
                elif part.ydir == -1 and part.position[1] <= 0:
                    part.position = (part.position[0], self.field_dimension[0] - 25 - 1)
                else: 
                    part.move()

    def render(self, surface):
        for part in self.body:
            part.render(surface)


#pellet object control
class Pellet():

    def __init__(self):
        self.position = self.setPos()
        self.eaten = False
        self.color = (255, 0, 0)
        self.width = CELL
        self.height = CELL
        
        #self.image = 
    def setPos(self):
        xpos = randint(1, COLS-1)*CELL
        ypos = randint(1,ROWS-1)*CELL
        
        return (xpos, ypos)
    def getPos(self):
        return self.position[0], self.position[1]
    def render(self, surface):
        xpos, ypos = self.getPos()
        #pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.width - 2, self.width - 2))
        pygame.draw.rect(surface, self.color, (xpos, ypos, self.height-2, self.width-2))
    def destroy(self):
        self.position = self.setPos()
        

def render(surface, snake, pellet):
    surface.fill((0, 0, 0))
    snake.render(surface)
    pellet.render(surface)
    pygame.display.update()

def main():
    field_dimensions = BOARD
    win = pygame.display.set_mode(BOARD)
    initial_pos = (250, 250)
    color = (0, 255, 0)
    snake = Snake(initial_pos, 1, 1, 0, color, field_dimensions)
    pellet = Pellet()
    clock = pygame.time.Clock()
    running = True

    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        print(snake.head.position, pellet.getPos())
        if(snake.head.position == pellet.getPos()):
            print(snake.head.position, pellet.getPos())
            pellet.destroy()
        snake.change_direction()
        snake.move()

        render(win, snake, pellet)
        clock.tick(15)

    pygame.quit()
    

if __name__ == "__main__":
    main()
