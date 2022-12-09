import pygame
import button

'''actions for buttons'''
def quitGame(args=None):
    pygame.quit()


class MenuScreen():
    def __init__(self, dimensions, buttons):
        self.buttons = buttons
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.prev_s=None
        self.next_s=None


class Button():
    def __init__(self, action=None, actionArgs=None, origin=(0,0), dimensions=(0,0), text_input=False):
        self.action = action
        self.args = actionArgs
        self.x_root = origin[0]
        self.y_root = origin[1]
        self.x_bound = origin[0] + dimensions[0]
        self.y_bound = origin[1] + dimensions[1]
        self.rect = pygame.Rect(self.x_root, self.y_root, self.x_bound, self.y_bound)
        self.input = text_input
        self.text = None
        self.unclick_color = (100,100,100)
        self.clicked_color = (200,200,200)
        
        
        
    def draw(self, surface):
        #draw base
        pygame.draw(surface, (255,0,0), self.rect)

        #if self.input, get self.text and display it

    def checkClick(self, mousePos):
        #check the location of the mouse click and perform the action if true
        if self.rect.collidepoint(mousePos):
            self.click()
        return False

    def click(self):
        #called by checkClick, but maybe also elsewhere?
        self.action(self.args)

    
    
class Menu():


    def __init__(self, surface):
        self.screens = []
        self.currentScreen = None
        self.previousScreen = None
        self.surface = surface
        self.x, self.y, self.w, self.h = surface.get_rect()

    def start(self):
        #initialize
        screen = display.blit(self.surface, self.dimensions)
        #make all of the possible screens
        exitButton = Button(action=quitGame, origin=( int(self.w - 40), int(self.y + 20), dimensions = ( 20,20 ) )
        backButton = Button()
        
        main_s = MenuScreen(self.dimensions,
                            Button(action= ),
                            Button(),
                            exitButton)
        ip_s = None
        single_s = None
        name_s = None
        start_s = None
        pause_s = None
        leader_board_s = None
        
        #display current screen

        #wait for user input

        #change current screen

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
    
