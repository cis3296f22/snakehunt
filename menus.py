import pygame, sys
import pygame.gfxdraw
from button import Button

screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
buttons = pygame.sprite.Group()

         
def on_quit():
    print("Quitting, goodbye")
    #pygame.quit()
    #sys.exit()
    
def on_play():
    print("playing game")
    # check if IP & Port valid
    # if they are, call nameloop()
    
def on_enterserver():
    print("entering game")
    
    # remove mainmenu buttons (quit & enter server)
    buttons.remove(quit_button)
    buttons.remove(enterserver_button)
    
    # add servermenu buttons (play & back)
    buttons.add(play_button)
    buttons.add(back_button)
    
    # inputfield IP
    
    # inputfield Port
    
def on_back():
    # go back to main menu
    
    # remove servermenu buttons (play & back)
    buttons.remove(play_button)
    buttons.remove(back_button)
    
    # add main menu buttons (quit & enter server)
    buttons.add(quit_button)
    buttons.add(enterserver_button)
    
def nameloop():
    print("name loop running")
    # inputfield Name
    # if name valid,
    # call game.start() & game.game_loop()
          # btw, in this screen, have Leave button in top right corner, 
          # on_leave() calls mainmenuloop()
      


      
def loop():
    # start with mainmenu buttons
    buttons.add(quit_button)
    buttons.add(enterserver_button)
    
    # main loop for drawing screen/buttons
    while True:
        for event in pygame.event.get():
            # if user clicks "x", completely exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        buttons.update()
        buttons.draw(screen)
        clock.tick(60)
        pygame.display.update()
          
    
if __name__ == '__main__':
    pygame.init()
    
    # Play button
    play_button = Button((10, 50), "Play", 55, "green on red", command=on_play)
    # Back button
    back_button = Button((10, 200), "Back", 55, "black on white", command=on_back)
    # Quit button
    quit_button = Button((10, 10), "Quit", 55, "black on white", command=on_quit)
    # Enter Server button
    enterserver_button = Button((10, 100), "Enter Server", 40, "black on red", command=on_enterserver)
    
    loop()
    
          