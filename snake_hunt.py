import pygame
from random import randint
from math import floor as flr
import tkinter
from tkinter import *
from tkinter import ttk
root = Tk()

BEYOND_BOARD = (2000, 2000)
BOARD = (1000,1000)
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

class PauseMenu:
    def __init__(self, game, player):
        root.geometry('275x100')
        self.game = game
        self.player = player
        self.current_name = StringVar()
        self.current_name.trace_add('write', self.rename)
        self.populate()
        root.mainloop()

    def rename(self, x, y, z):
        self.player.name = self.current_name.get()

    def quit(self):
        self.game.running = False
        root.destroy()

    def populate(self):
        frame = ttk.Frame(root, padding=10)
        frame.pack()

        naming_frame = ttk.Frame(frame)
        naming_frame.pack()
        ttk.Label(naming_frame, text = "Display Name: ").pack(side=tkinter.LEFT)
        naming_entry = Entry(naming_frame, width=25, textvariable=self.current_name)
        naming_entry.pack(side=tkinter.LEFT)

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=10)
        ttk.Button(buttons_frame, text='Play', command=root.destroy).pack(side=tkinter.LEFT, padx=3)
        ttk.Button(buttons_frame, text='Quit', command=self.quit).pack(side=tkinter.LEFT, padx=3)

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

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.width - 2, self.width - 2));

class Snake():
    def __init__(self, position, length, xdir, ydir, field_dimensions, world_dimensions):
        #(west,north,east,south) points
        self.bounds = {"west":world_dimensions[0]/4, "north":world_dimensions[1]/4, "east":3*world_dimensions[0]/4+field_dimensions[0], "south":3*world_dimensions[1]/4+field_dimensions[1]}
        self.color = (0, 255, 0)
        self.body = []
        self.turns = {}
        self.position = position
        self.length = length
        self.field_dimensions = field_dimensions
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
                if i == len(self.body) - 1:
                    self.turns.pop(pos)
            part.move()
            
            if part.position[0] < BEYOND_BOARD[0]/4:
                part.position = (part.position[0]+self.field_dimensions[0], part.position[1])
            elif part.position[0] > 3*BEYOND_BOARD[0]/4 - 1:
                part.position = (part.position[0]-self.field_dimensions[0], part.position[1])
                
            elif part.position[1] > 3*BEYOND_BOARD[1]/4 - 1:
                part.position = (part.position[0], part.position[1]-self.field_dimensions[1])
            elif part.position[1] < BEYOND_BOARD[1]/4:
                part.position = (part.position[0], part.position[1]+self.field_dimensions[1])
            '''
            if part.position[0] < self.bounds['east']:
                part.position = (self.bounds['west'], part.position[1])
            elif part.position[0] > self.bounds['west']:
                part.position = (self.bounds['east'], part.position[1])
                
            elif part.position[1] > self.bounds['north']:
                part.position = (part.position[0], self.bounds['south'])
            elif part.position[1] < self.bounds["south"]:
                part.position = (part.position[0], self.bounds["north"])
                '''

    def render(self, surface):
        for part in self.body:
            part.render(surface)

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
            if self.body[part].position in list(map(lambda z:z.position,self.body[part+1:])): # This will check if any of the positions in our body list overlap
                #font = pygame.font.Font('freesansbold.ttf', 32)
                #text = font.render("hello", True, (255, 0, 0))
                #win.blit(text, [WIDTH/2, HEIGHT/2])
                self.reset(self.position)
                break

#pellet object control
class Pellet():
    def __init__(self, world):
        self.world = world
        self.position = self.setPos()
        self.eaten = False
        self.color = (50, 200, 255)
        self.width = CELL
        self.height = CELL
        #self.image =

    def setPos(self):
        xpos = self.world.get_width()/4 + randint(1, COLS-1)*CELL
        ypos = self.world.get_height()/4 + randint(1,ROWS-1)*CELL
        return (xpos, ypos)

    def getPos(self):
        return self.position[0], self.position[1]

    def render(self, surface):
        xpos, ypos = self.getPos()
        #pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.width - 2, self.width - 2))
        pygame.draw.rect(surface, self.color, (xpos, ypos, self.height-2, self.width-2))

    def destroy(self):
        self.position = self.setPos()
        
    # set a pellet's position to a value passed in
    def setDetPos(self,xpos,ypos):
        self.position = [xpos,ypos]

class Camera():
    def __init__(self, player, dimensions):
        self.target = player
        self.position = player.head.position
        self.dimensions = dimensions

    def render(self, window, world):
        self.position = self.target.head.position
        window.blit(world, (5,5), (self.position[0] - self.dimensions[0]/2, self.position[1] - self.dimensions[1]/2, self.dimensions[0]-10, self.dimensions[1]-10))

# Generates multiple pellets in random locations such that they do not
# overlap
#
# IMPORTANT NOTE
# For a 32 bit system, the maximum array size in python is 536,870,912
# elements. Since this implementation is dependent on the board and cell size,
# this will not work for anything larger than a 23170 by 23170 size board/cell 
# ratio for 32 bit systems.
class RandomPellets():
    def __init__(self, numPellets, world):
        self.world = world
        self.numPellets = numPellets
        self.availablePositions = self.setPositions(self.world)
        self.pellets = self.genPellets()
        
    def genPellets(self):
        pellets = []
        for i in range(self.numPellets):
            pel = Pellet(self.world)
            # get a random available position then remove it from the list of 
            # available positions (-1 added to avoid error by popping out of range)
            pos = self.availablePositions.pop(randint(0,len(self.availablePositions)-1))
            # manually set the position of the pellet to the random position
            pel.setDetPos(pos[0],pos[1])
            pellets.append(pel)
        return(pellets)
    
    # initializes all possible pellet positions, i.e. every cell
    def setPositions(self, world):
        positions = []
        for i in range(flr(ROWS)):
            for j in range(flr(COLS)):
                positions.append([world.get_width()/4 + i*CELL,world.get_width()/4 + j*CELL])
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
        pel2 = Pellet(self.world)
        # generate a new pellet
        pel2.setDetPos(pos[0], pos[1])
        # add the deleted pellet's position back to the available positions
        self.availablePositions.append(pel.position)
        self.pellets.append(pel2)
        
    def addPellet(self,pel):
        self.pellets.append(pel)
        self.numPellets = self.numPellets+1
        
    def render(self,surface):
        for pellet in self.pellets:
            pellet.render(surface)

class Game():
    def __init__(self):
        pygame.init()
        self.field_dimensions = BOARD
        self.world_dimensions = BEYOND_BOARD
        self.camera_dimensions = (500, 500)
        self.win = pygame.display.set_mode(self.camera_dimensions)
        self.world = pygame.Surface(self.world_dimensions)

        self.title_font = pygame.font.Font('freesansbold.ttf', 32)
        self.leaderboard_font = pygame.font.Font('freesansbold.ttf', 10)
        self.title_text = self.title_font.render('Snake Hunt', True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect()

        self.players = []
        initial_pos = (250, 250)
        snake = Snake(initial_pos, 1, 1, 0, self.field_dimensions, self.world_dimensions)
        self.players.append(Player('Anonymous', snake))

        self.camera = Camera(snake, self.camera_dimensions)
        self.title_rect.center = (self.camera_dimensions[0] // 2, self.camera_dimensions[1] // 2)

        self.pellets = RandomPellets(25, self.world)
        self.clock = pygame.time.Clock()
        self.running = False

    def render(self):
        self.world.fill((20,30,20))
        pygame.draw.rect(self.world, (130,100,130),(BEYOND_BOARD[0]/4, BEYOND_BOARD[1]/4, BOARD[0], BOARD[1]))

        self.players[0].snake.render(self.world)
        self.pellets.render(self.world)
        self.camera.render(self.win, self.world)
        self.show_leaderboard()
    
        pygame.display.flip()
    
    def show_leaderboard(self):
        def takeSnakeSize(element):
            return element.snake.length
        list.sort(self.players, reverse=True, key=takeSnakeSize)
        topTen = min(10, len(self.players))
        top = 8
        for i in range(topTen):
            record_string = f"{i + 1}.   {self.players[i].name}   {self.players[i].snake.length}"
            record = self.leaderboard_font.render(record_string, True, (255, 255, 255))
            record_rect = record.get_rect()
            record_rect.topleft = (8, top)
            self.win.blit(record, record_rect)
            top += 11

    def pause(self):
        self.win.fill((0, 0, 0))
        self.win.blit(self.title_text, self.title_rect)
        pygame.display.update()
        self.pause_menu = PauseMenu(self, self.players[0])

    def game_loop(self):
        self.running = True

        self.pause()
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pos = self.pellets.getPositions()
            snake = self.players[0].snake
            if([snake.head.position[0], snake.head.position[1]] in pos):
                pellet = self.pellets.pellets[pos.index([snake.head.position[0],snake.head.position[1]])]
                # delete this pellet and generate a new random pellet
                self.pellets.resetPellet(pellet)
                snake.grow(1)

            snake.check_body_collision()
            snake.change_direction()
            snake.move()

            self.render()
            self.clock.tick(15)
            
        pygame.quit()

def main():
    game = Game()
    game.game_loop()

if __name__ == "__main__":
    main()
