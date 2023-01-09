import pygame


ALLOWED_CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', \
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', \
                 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', \
                 ]



class MenuScreen():

    def __init__(self, screen,background_color, edge_offset, state):
        self.screen = screen
        self.background_color = background_color
        self.background = pygame.Surface((screen.get_width() - edge_offset*2, screen.get_height() - edge_offset*2))
        self.menu_state = state
        self.elements = None
        self.edge_offset = edge_offset
        
    def set_buttons(self, elements):
        self.elements = elements
        

    def draw(self):
        self.background.fill(self.background_color)
        self.screen.blit(self.background, (self.edge_offset,self.edge_offset))
        for ele in self.elements:
            ele.draw()

    def check(self, pos):
        for ele in self.elements:
            if ele.check(pos):
                return ele.return_state
        #return the current state if there is no button clicked. ie stay put
        return self.menu_state

class Element:

    def __init__(self, text, font, text_color, background_color, rect, screen):
        self.text = text
        self.font = font
        self.background_color = background_color
        self.text_color = text_color
        self.width = rect[2]
        self.height = rect[3]
        self.rect = pygame.Rect(rect)
        self.origin = (rect[0], rect[1])
        self.background = pygame.Surface((self.width, self.height))
        self.screen = screen


class Button(Element):

    def __init__(self, text, font, text_color, background_color, rect, screen, state):

        super().__init__(text, font, text_color, background_color, rect, screen)
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


class InputDisplay(Element):

    def __init__(self, text, font, text_color, background_color, rect, screen, maxLen = 5, allowedChars=None):
        super().__init__(text, font, text_color, background_color, rect, screen)
        self.maxLen = maxLen
        self.allowedChars = []
        self.firstRun = True
        self.return_state = "input"
        if allowedChars is not None:
            self.allowedChars = allowedChars
        else:
            self.allowedChars = ALLOWED_CHARS

    def check(self, pos):
        if self.rect.collidepoint(pos):
            if self.firstRun:
                self.text = ""
            return self.return_state

    def addChar(self, char):
        char = chr(char)
        if len(self.text) + 1 > self.maxLen:
            return self.text
        if self.validateChar(char):
            self.text = self.text + char
        return self.text

    def removeChar(self):
        if len(self.text) > 0:
            self.text = self.text[:len(self.text) - 1]
        
    def validateChar(self, char):
        if char in self.allowedChars:
            return True
        return False

    def draw(self):

        #draw background
        self.background.fill(self.background_color)

        #img is the surface holding the text only, to be placed on the background of the button
        words = self.font.render(self.text, True, self.text_color)

        #place the image on the background
        self.background.blit(words, (0,0))

        #place the button on the display surface
        self.screen.blit(self.background, self.origin)


    
    
        
    

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
    Button(text, font, text_color, background_color, rect, screen, state)
    Menu(screen,background_color, edge_offset, state)
    '''
    pause_menu = MenuScreen(screen, (150,150,150), 50, "pause")
    resume_button = Button("resume", font, TEXT_COL, (200,200,200), (100,90,100,100), screen, "play")
    quit_button = Button("quit", font, TEXT_COL, (200,200,200), (210,90,100,100), screen, "quit")
    input_ele = InputDisplay("name", font, TEXT_COL, (200,200,200), (100, 200, 200, 50), screen, maxLen = 10)
    pause_menu.set_buttons((resume_button, quit_button, input_ele))

    quitting = Button("quitting", font, TEXT_COL, BKGRD_COL, (50,50,SCREEN_WIDTH-100,SCREEN_HEIGHT-100), screen, "quitting")

    clock = pygame.time.Clock()
    #menu loop
    while run is True:

        screen.fill((255,0,0))

        #get position of the mouse and if it was clicked
        pos = pygame.mouse.get_pos()
        clicked = True if pygame.mouse.get_pressed()[0] == 1 else False

        #input character for the name input
        inputChar = 0

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "play":
                    game_state = "pause"
                else:
                    inputChar = event.key
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

        elif game_state == "input":
            pause_menu.draw()
            if clicked:
                game_state = pause_menu.check(pos)
            if inputChar == pygame.K_RETURN:
                game_state = "pause"
            if inputChar == pygame.K_BACKSPACE:
                input_ele.removeChar()
            else:
                print(input_ele.addChar(inputChar))
            
        
        print(game_state)
        pygame.display.flip()
        clock.tick(30)


    pygame.event.get()
    pygame.quit()


if __name__ == '__main__':
    test()
    
