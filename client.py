import pygame
import socket
import pickle
import sys


class Client:
    def __init__(self, HOST='localhost', PORT=5556):
        self.HOST = HOST
        self.PORT = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def Connect(self):
        self.s.connect((self.HOST, self.PORT))
    def Send(self, player):
        data = pickle.dumps(player)
        self.s.sendall(data)
    def Receive(self):
        data = self.s.recv(1024)
        opponent = pickle.loads(data)
        return opponent


class Square():
    def __init__(self, HOST='localhost', PORT=5556):
        pygame.init()
        self.width = 500
        self.height = 500
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Square Client")
        self.running = True
        self.client = Client(HOST, PORT)
        self.client.Connect()
        self.opponent = []
        self.square = self.GetStartPos()
        self.vel = 3
        self.Loop()
    
    def GetStartPos(self):
        x = 0
        y = 0
        return [[x,y], [x+20,y]]
    
    def KeyPressed(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel
            
    def Loop(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            #read position
            #update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.KeyPressed()
            self.win.fill((0,0,0)) #make window black
            
            self.DrawSquare(self.square, (0,255,0)) #my square is green
            
            self.client.Send(self.square)
            self.opponent = self.client.Receive()
            self.DrawSquare(self.opponent, (0,0,255)) #opponent's square is red

            pygame.display.flip()
            

    def DrawSquare(self, square, color):
        pygame.draw.rect(self.win, color, (self.square.x,self.square.y,10,10))

player1 = Square()
player1.Loop()
