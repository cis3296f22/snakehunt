import pygame


class Button():

    def __init__(self, text_color, background_color,rect, font, text, screen, state):

        self.text = text
        self.font = font
        self.background_color = background_color
        self.text_color = text_color
        self.width = rect[2]
        self.height = rect[3]
        self.rect = pygame.Rect(rect)
        self.origin = (rect[0], rect[1])
        self.clicked = False
        self.background = pygame.Surface((self.width, self.height))
        self.screen = screen
        self.return_state = state


    def check(self, pos):
        if self.rect.collidepoint(pos):
            return self.return_state

    def draw(self):

        #draw background
        self.background.fill(self.background_color)

        #img is the surface holding the text only, to be placed on the background of the button
        words = self.font.render(self.text, True, self.text_color)

        #place the image on the background
        self.background.blit(words, (0,0))

        #place the button on the display surface
        self.screen.blit(self.background, self.origin)

    
    
class MenuScreen():

    def __init__(self, screen,background_color, edge_offset, state):
        self.screen = screen
        self.background_color = background_color
        self.background = pygame.Surface((screen.get_width() - edge_offset*2, screen.get_height() - edge_offset*2))
        self.menu_state = state
        self.buttons = None
        self.edge_offset = edge_offset
        
    def set_buttons(self, buttons):
        self.buttons = buttons
        

    def draw(self):
        self.background.fill(self.background_color)
        self.screen.blit(self.background, (self.edge_offset,self.edge_offset))
        for button in self.buttons:
            button.draw()

    def check(self, pos):
        for button in self.buttons:
            if button.check(pos):
                return button.return_state
        return self.menu_state
    

def test():
    
    #start pygame
    pygame.init()

    #create game window
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    #variables NOTE: some things, like font, need to be built after a display
    font = pygame.font.SysFont("signpainter", 40)
    game_paused = False
    game_state = "play"
    TEXT_COL = (255, 255, 255)
    BKGRD_COL = (100,100,100)
    run = True

    #make banner
    banner_text = "Press SPACE to pause"
    banner_pos = (100, 100)
    banner_words = font.render(banner_text, True, TEXT_COL)
    

    #make buttons
    '''
    Button(text_color, background_color, (rectangle_of_button), font, display_text)
    Menu(screen,background_color, edge_offset, state)
    '''
    pause_menu = MenuScreen(screen, (150,150,150), 50, "pause")
    resume_button = Button(TEXT_COL, (200,200,200), (100,90,100,100), font, "resume", screen, "play")
    quit_button = Button(TEXT_COL, (200,200,200), (210,90,200,100), font, "quit", screen, "quit")
    pause_menu.set_buttons((resume_button, quit_button))

    quitting = Button(TEXT_COL, BKGRD_COL, (50,50,SCREEN_WIDTH-100,SCREEN_HEIGHT-100), font, "quitting", screen, "quitting")

    #menu loop
    while run is True:

        screen.fill((255,0,0))

        #get position of the mouse and if it was clicked
        pos = pygame.mouse.get_pos()
        clicked = True if pygame.mouse.get_pressed()[0] == 1 else False

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "pause"
            if event.type == pygame.QUIT:
                run = False

        #check for state to display menus
        if game_state == "play":
            screen.blit(banner_words, (0,0))

        elif game_state == "pause":
            pause_menu.draw()
            if clicked:
                game_state = pause_menu.check(pos)

        elif game_state == "quit":
            quitting.draw()
            run = False

            
        print(game_state)
        pygame.display.flip()


    pygame.event.get()
    pygame.quit()


if __name__ == '__main__':
    test()
    
