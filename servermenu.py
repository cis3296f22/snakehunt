def on_back():
    print("main menu")
    # go back to main menu
    
def on_play():
    print("playing game")
    # check if IP & Port valid
    # if they are, call nameloop()
    
def nameloop():
    print("name loop running")
    # inputfield Name
    # if name valid,
    # call game.start() & game.game_loop()
          # btw, in this screen, have Leave button in top right corner, 
          # on_leave() calls mainmenuloop()
          
def servermenu():
    buttons = pygame.sprite.Group()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    
    # Play button
    play_button = Button(buttons, screen, (10, 50), "Play", 55, "green on red", command=on_play)
    # Back button
    back_button = Button(buttons, screen, (10, 200), "Back", 55, "black on white", command=on_back)
    # Quit button
    quit_button = Button(buttons, screen, (10, 10), "Quit", 55, "black on white", command=on_quit)
    # Enter Server button
    enterserver_button = Button(buttons, screen, (10, 100), "Enter Server", 40, "black on red", command=on_enterserver)
    
    # main loop for drawing screen/buttons
    while True:
        for event in pygame.event.get():
            # if user clicks "x", completely exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Button.buttons.update()
        Button.buttons.draw(Button.screen)
        clock.tick(60)
        pygame.display.update()
          
    
if __name__ == '__main__':
    pygame.init()
    servermenu()