class ScreenDimensions:
    """Screen dimension constants."""
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

class Color:
    """Color constants."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (34, 139, 34)
    DARK_GREEN = (0, 100, 0)
    LIGHT_GREEN = (144, 238, 144)
    RED = (220, 20, 60)
    YELLOW = (255, 215, 0)
    BROWN = (139, 69, 19)
    TAN = (210, 180, 140)
    LIGHT_BROWN = (160, 82, 45)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    ORANGE = (255, 165, 0)

# Game constants
class GameConstants:
    """General game constants."""
    COOP_SIZE = 60
    CHICKEN_SIZE = 20
    LAND_SIZE = 80
    class GameEconomyConstants:
        """Game economy related constants."""
        COOP_COST = 100
        CHICKEN_COST = 30
        LAND_COST = 150
        EGG_SELL_PRICE = 5
        # Production rates (eggs per second)
        CHICKEN_PRODUCTION_RATE = 0.3  # Chickens produce less than coops
        BLIGHT_PENALTY = -0.5  # Production penalty during blight
