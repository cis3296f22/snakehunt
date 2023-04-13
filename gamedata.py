class CellData():
    """
    A class containing info needed to render a block.

    A block is a generic rectangle that can represent anything.

    Attributes
    ----------
    position (tuple[int, int]):
        Position of the block
    
    color (tuple[int, int, int]):
        Color of the block

    width (int):
        Width of the block

    direction (tuple[int, int]):
        Direction of the block
    """

    def __init__(self, position, color, width, direction=None):
        """Initialize CellData."""
        self.position = position
        self.color = color
        self.width = width
        self.direction = direction

class LeaderboardEntry():
    """
    A class representing a leaderboard entry.

    Attributes
    ----------
    name (str):
        Name of a player

    score (int):
        Score of the player
    """

    def __init__(self, name, score):
        """Create leaderboard entry."""
        self.name = name
        self.score = score

class GameData():
    """
    Class holding everything that is needed to render the game.

    Attributes
    ----------
    snake (Snake):
        Receiving client's snake

    snakes (list):
        List of other snakes in game (excluding receiver)

    pellets (list):
        List of pellets in the game

    leaderboard (list):
        List of top players and their scores

    sound (comm.Message):
        The sound file to play during this frame
    """

    def __init__(self, snake, snakes, pellets, leaderboard, sound=None):
        """Initialize game data."""
        self.snake = snake
        self.snakes = snakes
        self.pellets = pellets
        self.leaderboard = leaderboard
        self.sound = sound
