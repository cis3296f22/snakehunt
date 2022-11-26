import pygame
import pygame.gfxdraw


pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
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

# actions when buttons clicked
def on_quit():
    print("Quitting, goodbye")

def on_start():
    print("Starting server")

def on_name():
    print("Bring up naming")

def buttons_def():
    b0 = Button((10, 10), "Quit Game", 55, "black on white", command=on_quit)
    b1 = Button((10, 100), "Start Server", 40, "black on red", command=on_start)
    b2 = Button((10, 170), "Enter Name", 36, "red on yellow", command=on_name)

# ======================= this code is just for example, start the program from the main file
# in the main folder, I mean, you can also use this file only, but I prefer from the main file
# 29.8.2021

if __name__ == '__main__':
    pygame.init()
    game_on = 0
    def loop():
        # BUTTONS ISTANCES
        game_on = 1
        buttons_def()
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    game_on = 0
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        game_on = 0
            if game_on:
                buttons.update()
                buttons.draw(screen)
            else:
                pygame.quit()
                sys.exit()
            buttons.draw(screen)
            clock.tick(60)
            pygame.display.update()
        pygame.quit()




    loop()