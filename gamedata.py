# This class contains the properties needed to render a snake's body part
# This object is constructed by the server and sent in serialized format to the client
# It is possible to serialize a BodyPart object, however, since the server handles game logic, 
# lots of unnecessary data will be sent to the client in that case.
# 
class BodyPartData():
    def __init__(self, position, color, width):
        self.position = position
        self.color = color
        self.width = width

# This class holds every single data item that we need to be able to render game objects in client side
class GameData():
    def __init__(self, snakes, pellets):
        self.snakes = snakes
        self.pellets = pellets
