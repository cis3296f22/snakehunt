# This class contains the properties needed to render a cell
# A cell is a generic rectangle that can represent anything
# In this game, it is used for snakes' body parts and food pellets
class CellData():
    def __init__(self, position, color, width, direction=None):
        self.position = position
        self.color = color
        self.width = width
        self.direction = direction

class LeaderboardEntry():
    def __init__(self, name, score):
        self.name = name
        self.score = score

# This class holds every single data item that we need to be able to render game objects in client side
class GameData():
    def __init__(self, snake, snakes, pellets, leaderboard, sound=None):
        self.snake = snake
        self.snakes = snakes
        self.pellets = pellets
        self.leaderboard = leaderboard
        self.sound = sound
