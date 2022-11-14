# This class contains the properties needed to render a snake's body part
# This object is constructed by the server and sent in serialized format to the client
# It is possible to serialize a BodyPart object, however, since the server handles game logic, 
# lots of unnecessary data will be sent to the client in that case.
# 
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
    def __init__(self, snake, snakes, pellets, leaderboard):
        self.snake = snake
        self.snakes = snakes
        self.pellets = pellets
        self.leaderboard = leaderboard
