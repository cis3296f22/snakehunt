import pygame
from network import Network

WIDTH = 500
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

class Window:
    def __init__(self, window_display):
        self._window = window_display

    @property
    def window(self):
        return self._window

    def redrawWindow(self, player, playerlist):
        self.window.fill((0,0,0))
        player.draw(self.window)
        for playerNum in playerlist:
            player_to_draw = playerlist[playerNum]
            player_to_draw.draw(self.window)
        pygame.display.update()
        
class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update_rect()

    def update_rect(self):
        self.rect = (self.x, self.y, self.width, self.height)


def main():
    run = True
    win = Window(window)
    n = Network()
    clock = pygame.time.Clock()
    player = n.player
    
    while run:
        clock.tick(60)
        playerlist = n.send(player)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        win.redrawWindow(player, playerlist)

if __name__ == '__main__':
    main()
