import pygame
import button

def menu():
    pygame.init()

    #create game window
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    #game variables
    game_paused = False
    menu_state = "main"

    #load button images
    resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
    options_img = pygame.image.load("images/button_options.png").convert_alpha()
    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
    back_img = pygame.image.load('images/button_back.png').convert_alpha()

    #create button instances
    resume_button = button.Button(304, 125, resume_img, 1)
    options_button = button.Button(297, 250, options_img, 1)
    quit_button = button.Button(336, 375, quit_img, 1)
    back_button = button.Button(332, 450, back_img, 1)

    #menu loop
    run = True
    while run:

        screen.fill((255,0,0))

        #check if game is paused
        if game_paused == True:
            #check menu state
            if menu_state == "main":
                #draw pause screen buttons
                if resume_button.draw(screen):
                    game_paused = False
                if options_button.draw(screen):
                    menu_state = "options"
                if quit_button.draw(screen):
                    run = False
            #check if the options menu is open
            if menu_state == "options":
                #draw the different options buttons
                if back_button.draw(screen):
                    menu_state = "main"
        else:
            print("Press ESCAPE to pause")

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    menu()
    