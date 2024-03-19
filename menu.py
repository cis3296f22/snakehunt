
import pygame

#basic to InputDisplay objects.  can be replaced
ALLOWED_CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', \
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', \
                 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', \
                 ]

#basic to SnakeBanner objects.  can be replaced
POINTS = [(6,0), (6,1), (6,2), (5,2), (5,1), (4,1), (3,1), (2,1), (1,1), \
          (1,2), (1,3), (1,4), (1,5), \
          (2,5), (3,5), (4,5), (5,5),  \
          (5,6), (5,7), (5,8), (5,9), \
          (4,9), (3,9), (2,9), (1,9), (1,8), (0,8),\
          \
          (8,10), (8,9), (8,8), (8,7), (8,6), \
          (9,6), (10,6), (11,6), (12,6), \
          (12,7), (12,8), (12,9), \
          (13,9), (13,8), (13,7), (13,6), (13,5), (13,4), (13,3),(13,2), (13,1), \
          (12,1), (12,2), (12,3), (12, 4),(12,5), \
          (11,5), (10,5), (9,5), (8,5), \
          (8,4), (8,3), (8,2), (8,1), (8,0)
          ] 
          


class SnakeBanner():

    def __init__(self, screen,background_color, edge_offset, points, xblocks, yblocks, font):
        self.screen = screen
        self.background_color = background_color
        self.head = 0
        self.tail = 1
        self.points = points
        self.length = len(points)
        self.edge_offset = edge_offset
        self.mainColor = (50, 200, 50)
        self.headColor = (225, 225, 100)
        self.gap = 4
        
        bkgd_width = screen.get_width() - edge_offset*2
        self.blockWidth = int(bkgd_width/xblocks)
        self.blockHeight = self.blockWidth
        self.background = pygame.Surface((bkgd_width - self.gap, self.blockWidth*yblocks + self.gap))
        #Element(text, font, text_color, background_color, rect, screen)
        self.press_start = Element("press space to start", font, (200,200,200), (background_color), (250, 600, 265, 45), screen)

    def draw(self):
        #draw background
        self.press_start.draw()
        self.background.fill(self.background_color)
        x = self.blockWidth
        y = self.blockHeight
        off = self.gap

        for block in self.points:
            pygame.draw.rect(self.background, self.mainColor, (block[0]*x+off, block[1]*y+off, x-off, y-off))
        pygame.draw.rect(self.background, self.headColor, (self.points[self.head][0]*x+off, self.points[self.head][1]*y+off, x-off,y-off))
        for i in range(1, 4):
            tail = self.points[(self.head + i)%self.length]
            rect = (tail[0]*x+off, tail[1]*y+off, x-off,y-off)
            pygame.draw.rect(self.background, self.background_color, rect)
        self.head = (self.head + 1) % self.length
        

        #place the button on the display surface
        self.screen.blit(self.background, (self.edge_offset,self.edge_offset))

class MenuScreen():

    def __init__(self, screen,background_color, edge_offset, state):
        self.screen = screen
        self.background_color = background_color
        self.background = pygame.Surface((screen.get_width() - edge_offset*2, screen.get_height() - edge_offset*2))
        self.menu_state = state
        self.elements = []
        self.edge_offset = edge_offset
        
    def set_elements(self, elements):
        self.elements = elements

    def add_elements(self, elements):
        for element in elements:
            self.elements.append(element)

    def remove_element(self, element_to_remove):
        for element in self.elements:
            if element == element_to_remove:
                self.elements.remove(element)
                return True
        return False
    
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

    def draw(self):

        #draw background
        self.background.fill(self.background_color)

        #words is the surface holding the text only, to be placed on the background of the button
        words = self.font.render(self.text, True, self.text_color)

        #place the image on the background
        self.background.blit(words, (0,0))

        #place the button on the display surface
        self.screen.blit(self.background, self.origin)

class Button(Element):

    def __init__(self, text, font, text_color, background_color, rect, screen, state):

        super().__init__(text, font, text_color, background_color, rect, screen)
        self.return_state = state


    def check(self, pos):
        if self.rect.collidepoint(pos):
            return self.return_state

class InputDisplay(Element):

    def __init__(self, text, font, text_color, background_color, rect, screen, state, maxLen = 5, allowedChars=None):
        super().__init__(text, font, text_color, background_color, rect, screen)
        self.maxLen = maxLen
        self.allowedChars = []
        self.firstRun = True
        self.return_state = state
        if allowedChars is not None:
            self.allowedChars = allowedChars
        else:
            self.allowedChars = ALLOWED_CHARS

    def getText(self):
        return self.text

    def check(self, pos):
        if self.rect.collidepoint(pos):
            if self.firstRun:
                self.firstRun = False
                self.text = ""
                
            return self.return_state

    def addChar(self, char):
        try:
            char = chr(char)
        except:
            pass
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

def test():

    #start pygame
    pygame.init()

    #create game window
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    #variables NOTE: some things, like font, need to be built after a display
    font = pygame.font.SysFont("signpainter", 40)
    game_paused = False
    game_state = "title"
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
    SnakeBanner(screen,background_color, edge_offset, points)
    '''
    snake_banner = SnakeBanner(screen, (0,0,0), 10, POINTS, 14, 10, font)
    pause_menu = MenuScreen(screen, (150,150,150), 50, "pause")
    resume_button = Button("resume", font, TEXT_COL, (200,200,200), (100,90,100,100), screen, "title")
    quit_button = Button("quit", font, TEXT_COL, (200,200,200), (210,90,100,100), screen, "quit")
    input_ele = InputDisplay("name", font, TEXT_COL, (200,200,200), (100, 200, 200, 50), screen, "input", maxLen = 10)
    pause_menu.set_elements((resume_button, quit_button, input_ele))

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
                if event.key == pygame.K_SPACE and game_state == "title":
                    game_state = "pause"
                else:
                    inputChar = event.key
            if event.type == pygame.QUIT:
                run = False

        #check for state to display menus
        if game_state == "title":
            #screen.blit(banner_words, (0,0))
            clock.tick(15)
            snake_banner.draw()
            

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
            
        
        # print(game_state)
        pygame.display.flip()
        


    pygame.event.get()
    pygame.quit()


if __name__ == '__main__':
    test()
    
