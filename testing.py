import unittest
from snake_hunt import *

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

pygame.init()
test_field_dimensions = BOARD
test_world_dimensions = BEYOND_BOARD
test_camera_dimensions = (500, 500)
test_win = pygame.display.set_mode(test_camera_dimensions)
test_world = pygame.Surface(test_world_dimensions)

test_title_font = pygame.font.Font('freesansbold.ttf', 32)
test_leaderboard_font = pygame.font.Font('freesansbold.ttf', 10)
test_title_text = test_title_font.render('Snake Hunt', True, (255, 255, 255))
test_title_rect = test_title_text.get_rect()

test_players = []
test_initial_pos = (250, 250)
test_snake = Snake(test_initial_pos, 1, 1, 0, test_field_dimensions, test_world_dimensions)
test_players.append(Player('Anonymous', test_snake))

test_camera = Camera(test_snake, test_camera_dimensions)
test_title_rect.center = (test_camera_dimensions[0] // 2, test_camera_dimensions[1] // 2)

test_pellets = RandomPellets(25, test_world)
test_clock = pygame.time.Clock()
test_running = False


class Test(unittest.TestCase):
    
    # tests that the grow method increases snake size
    def test_SnakeGrowIncreasesSize(self):
        ilength = test_snake.length
        test_snake.grow(1)
        self.assertEqual(ilength + 1, test_snake.length)
    
    # tests that the grow method actually ads a bodypart
    def test_SnakeGrowIncreasesBody(self):
        ilength = len(test_snake.body)
        test_snake.grow(1)
        self.assertEqual(ilength + 1, len(test_snake.body))
    
    # tests that the snake has its size set back to 1 after reset method is called
    def test_resetSnakeSize(self):
        test_snake.reset(test_snake.position)
        self.assertEqual(1,test_snake.length)
    
    # tests that reset actually reduces the snake to one bodypart
    def test_resetSnakeBody(self):
        test_snake.reset(test_snake.position)
        self.assertEqual(1,len(test_snake.body))
        
    # tests that the addPellet method accurately adds the pellet to the array
    def test_addPelletAddsToPellets(self):
        p = Pellet(test_world)
        test_pellets.addPellet(p)
        self.assertTrue(p in test_pellets.pellets)
    
    # tests that addPellet increases the size of the pellet array
    def test_addPelletIncreasesSize(self):
        size = test_pellets.numPellets
        p = Pellet(test_world)
        test_pellets.addPellet(p)
        self.assertEqual(size+1,test_pellets.numPellets)
        
    # tests that calling resetPellet doesn't change size of randomPellets
    def test_resetPelletKeepsSize(self):
        ilength = test_pellets.numPellets
        test_pellets.resetPellet(test_pellets.pellets[0])
        self.assertEqual(ilength,test_pellets.numPellets)
        
    # tests that calling resetPellet doesn't change the amount of pellets
    def test_resetPelletKeepsTotalPellets(self):
        ilength = len(test_pellets.pellets)
        test_pellets.resetPellet(test_pellets.pellets[0])
        self.assertEqual(ilength,len(test_pellets.pellets))    
        
    # tests that calling resetPellet doesn't add to an existing position
    def test_resetPelletAddsNewPosition(self):
        p = test_pellets.pellets[0]
        pos = p.position
        test_pellets.resetPellet(p)
        self.assertFalse(pos in  test_pellets.getPositions())
        
    # tests that setDirection in BodyPart accurately sets direction to the left
    def test_setDirectionLeft(self):
        test_snake.body[0].set_direction(-1,0)
        self.assertEqual([-1,0],[test_snake.body[0].xdir,test_snake.body[0].ydir])
        
    # tests that setDirection in BodyPart accurately sets direction to the right
    def test_setDirectionRight(self):
        test_snake.body[0].set_direction(1,0)
        self.assertEqual([1,0],[test_snake.body[0].xdir,test_snake.body[0].ydir])  
        
    # tests that setDirection in BodyPart accurately sets direction to up
    def test_setDirectionUp(self):
        test_snake.body[0].set_direction(0,1)
        self.assertEqual([0,1],[test_snake.body[0].xdir,test_snake.body[0].ydir])  
        
    # tests that setDirection in BodyPart accurately sets direction to down
    def test_setDirectionDown(self):
        test_snake.body[0].set_direction(0,-1)
        self.assertEqual([0,-1],[test_snake.body[0].xdir,test_snake.body[0].ydir])          
        
    # tests that move in BodyPart accurately moves the part to the left
    def test_moveLeft(self):
        test_snake.reset(test_snake.position)
        test_snake.body[0].position = (50,50)
        test_snake.body[0].set_direction(-1,0)
        test_snake.body[0].move()
        self.assertEqual((40,50), test_snake.body[0].position)
        test_snake.reset(test_snake.position)

    # tests that move in BodyPart accurately moves the part to the right
    def test_moveRight(self):
        test_snake.reset(test_snake.position)
        test_snake.body[0].position = (50,50)
        test_snake.body[0].set_direction(1,0)
        test_snake.body[0].move()
        self.assertEqual((60,50), test_snake.body[0].position)
        test_snake.reset(test_snake.position)

    # tests that move in BodyPart accurately moves the part down
    def test_moveDown(self):
        test_snake.reset(test_snake.position)
        test_snake.body[0].position = (50,50)
        test_snake.body[0].set_direction(0,-1)
        test_snake.body[0].move()
        self.assertEqual((50,40), test_snake.body[0].position)
        test_snake.reset(test_snake.position)
        
    # tests that move in BodyPart accurately moves the part up
    def test_moveUp(self):
        test_snake.reset(test_snake.position)
        test_snake.body[0].position = (50,50)
        test_snake.body[0].set_direction(0,1)
        test_snake.body[0].move()
        self.assertEqual((50,60), test_snake.body[0].position)
        test_snake.reset(test_snake.position)
        
if __name__ == '__main__':
    unittest.main()

pygame.quit()