import pygame
from random import randint
from tkinter import messagebox
#import math
##from math import floor as flr

BEYOND_BOARD = (500, 500)     #the bounds of what can be rendered visibly
BOARD = (250,250)               #the bounds of the playing field
CELL = 10                       #the width of a single object in the game world
SPEED = CELL                    #WHILE MOVEMENT IS PER-CELL, must be a multiple of CELL
COLS = BOARD[0]/CELL
ROWS = BOARD[1]/CELL

# A single part of a snake.





def main():
    pygame.init()
    max_render_dimensions = BEYOND_BOARD
    field_dimensions = BOARD
    outer_world = pygame.Surface(max_render_dimensions)
    world = pygame.Surface(field_dimensions)
    
    window = pygame.display.set_mode(max_render_dimensions)

    clock = pygame.time.Clock()
    
    running = True

    
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #window.fill((20,30,20),(0,0,max_render_dimensions[0], max_render_dimensions[1]))
        #window.fill((45,100,45),(max_render_dimensions[0]/4, max_render_dimensions[0]/4, field_dimensions[0], field_dimensions[1]))
        pygame.draw.rect(window,(20,30,20),(0,0,max_render_dimensions[0], max_render_dimensions[1]))
        pygame.draw.rect(window,(45,100,45),(max_render_dimensions[0]/4, max_render_dimensions[0]/4, field_dimensions[0], field_dimensions[1]))
        pygame.draw.rect(window, (200,100,45),((max_render_dimensions[0]/4 + 10, max_render_dimensions[0]/4 +10 , 10, 10)))

        

        pygame.display.flip()
        
        
        

        clock.tick(15)
        
    pygame.quit()
    

if __name__ == "__main__":
    main()
