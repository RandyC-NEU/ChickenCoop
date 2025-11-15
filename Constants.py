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
    BLUE = (30, 144, 255)
    BROWN = (139, 69, 19)
    TAN = (210, 180, 140)
    LIGHT_BROWN = (160, 82, 45)
    DARK_BROWN = (120, 60, 30)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    ORANGE = (255, 165, 0)

# Game constants
class GameConstants:
    """General game constants."""
    COOP_SIZE = 40
    CHICKEN_SIZE = 20
    LAND_SIZE = 100
    BLIGHT_CHANCE = 0.002  # Base chance per second for blight to occur in a coop
    
    class CoopTypes:
        """Different coop types with different properties."""
        CLASSIC = {
            "name": "Classic Coop",
            "capacity": 10,  # Max chickens
            "blight_multiplier": 1.0,  # Blight chance multiplier
            "land_slots": 1,  # Number of land tiles occupied
            "cost": 100,
        }
        DELUXE = {
            "name": "Deluxe Coop",
            "capacity": 20,  # Higher capacity
            "blight_multiplier": 0.5,  # Lower blight chance (50% of normal)
            "land_slots": 2,  # Occupies 2 land tiles
            "cost": 200,
        }
    
    class GameEconomyConstants:
        """Game economy related constants."""
        COOP_COST = 100
        CHICKEN_COST = 30
        LAND_COST = 150
        EGG_SELL_PRICE = 5
        FEED_COST = 40  # Cost per feed bag
        # Production rates (eggs per second)
        CHICKEN_PRODUCTION_RATE = 0.3  # Chickens produce less than coops
        BLIGHT_PENALTY = -0.5  # Production penalty during blight
    
    class FeedConstants:
        """Feed and starvation mechanics."""
        INITIAL_FEED_LEVEL = 100.0  # Starting feed % (0-100)
        FEED_CAPACITY = 100.0  # Max feed level
        FEED_CONSUMPTION_RATE = 5.0  # Feed % consumed per chicken per minute
        STARVATION_THRESHOLD = 10.0  # Feed % below which chickens start dying
        STARVATION_DEATH_RATE = 0.1  # Chickens killed per second when starving (per chicken)

class LightingConstants:
    """Lighting and visual effect constants."""
    # Shadow parameters
    SHADOW_ALPHA = 80  # Transparency of shadows (0-255)
    SHADOW_BLUR = 2    # How blurred/soft shadows appear
    
    # Day cycle parameters (in game seconds)
    DAY_CYCLE_LENGTH = 60.0  # Full day cycle duration
    
    # Lighting color presets for different times of day
    MORNING_TINT = (255, 200, 150)    # Warm golden light
    MIDDAY_TINT = (255, 255, 255)     # Neutral white light
    EVENING_TINT = (255, 150, 100)    # Warm orange light
    NIGHT_TINT = (100, 150, 200)      # Cool blue light
    
    # Vignette effect
    VIGNETTE_STRENGTH = 0.3  # How dark edges get (0-1)
