import pygame, sys
import pygame.gfxdraw

screen = pygame.display.set_mode((600, 400))
buttons = pygame.sprite.Group()

class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, size, colors="white on blue", borderc=(255,255,255), command=lambda: print("No command defined")):
        super().__init__()
        self.text = text
        self.command = command
        
        # colors
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        self.hover_colors = f"{self.bg} on {self.fg}"
        self.borderc = borderc 
        
        # font
        self.font = pygame.font.SysFont("Arial", size)
        self.render()
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.position = position
        self.pressed = 1
        
        buttons.add(self)

    def draw_button(self):
        # draws border of button, 4 lines around plus background
        # horizontal up
        pygame.draw.line(screen, (150, 150, 150), (self.x, self.y), (self.x + self.w , self.y), 5)
        pygame.draw.line(screen, (150, 150, 150), (self.x, self.y - 2), (self.x, self.y + self.h), 5)
        # horizontal down
        pygame.draw.line(screen, (50, 50, 50), (self.x, self.y + self.h), (self.x + self.w , self.y + self.h), 5)
        pygame.draw.line(screen, (50, 50, 50), (self.x + self.w , self.y + self.h), [self.x + self.w , self.y], 5)
        # background
        pygame.draw.rect(screen, self.bg, (self.x, self.y, self.w , self.h))  

    def hover(self):
        # checks if mouse over button, and change color if true
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colors = self.hover_colors
        else:
            self.colors = self.original_colors
        self.render()

    def click(self):
        # checks if button clicked, and make call to action just once
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                print("Executing code for button '" + self.text + "'")
                self.command()
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1
                
    def render(self):
        self.text_render = self.font.render(self.text, 1, self.fg)
        self.image = self.text_render

    def update(self):
        self.fg, self.bg = self.colors.split(" on ")
        self.draw_button()
        self.hover()
        self.click()


         
def on_quit():
    print("Quitting, goodbye")
    #pygame.quit()
    #sys.exit()
    
    
def on_enterserver():
    print("entering game")
    
    # inputfield IP
    
    # inputfield Port
    

      


      
def mainmenu():
    buttons = pygame.sprite.Group()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    
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
    mainmenu()
    
          