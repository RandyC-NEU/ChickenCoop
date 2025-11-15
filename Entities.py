from dataclasses import dataclass
from typing import List
from Constants import GameConstants, Color
from Camera import Camera, grid_to_world
from Lighting import ShadowManager
import random
import pygame

@dataclass
class Chicken:
    """Represents a single chicken with an offset relative to its coop's world position."""
    def __init__(self, offset_x: float, offset_y: float):
        self.offset_x: float = offset_x
        self.offset_y: float = offset_y
        self.eggs_produced: float = 0.0

    def draw(self, screen, world_x, world_y, camera: Camera):
        # compute screen position from coop world pos + offset
        wx = world_x + self.offset_x
        wy = world_y + self.offset_y
        cx, cy = camera.world_to_screen((wx, wy))
        # body (isometric-style ellipse)
        body_w = int(GameConstants.CHICKEN_SIZE * 1.6)
        body_h = int(GameConstants.CHICKEN_SIZE * 1.0)
        body_rect = pygame.Rect(cx - body_w // 2, cy - body_h // 2, body_w, body_h)
        
        # Draw shadow beneath chicken
        ShadowManager.draw_shadow(screen, cx, cy, body_w, body_h, offset_y=4)
        
        pygame.draw.ellipse(screen, Color.ORANGE, body_rect)
        # subtle highlight
        highlight_rect = pygame.Rect(body_rect.x + body_w // 6, body_rect.y + body_h // 8, body_w // 2, body_h // 2)
        pygame.draw.ellipse(screen, (255, 190, 100), highlight_rect)

        # head (slightly offset to give isometric perspective)
        head_x = cx + body_w // 4
        head_y = cy - body_h // 4
        pygame.draw.ellipse(screen, Color.ORANGE, (head_x - 6, head_y - 6, 12, 12))

        # beak (small triangle)
        pygame.draw.polygon(screen, Color.YELLOW, [
            (head_x + 6, head_y),
            (head_x + 10, head_y + 3),
            (head_x + 6, head_y + 4)
        ])


@dataclass
class Coop:
    """Represents a chicken coop (logical entity). Drawn by passing world coordinates and camera."""
    def __init__(self, coop_type=None):
        if coop_type is None:
            coop_type = GameConstants.CoopTypes.CLASSIC
        self.coop_type = coop_type
        self.chickens: List[Chicken] = []
        self.blight_active = False
        self.eggs_produced: float = 0.0
        self.feed_level: float = GameConstants.FeedConstants.INITIAL_FEED_LEVEL

    def draw(self, screen, world_x, world_y, camera: Camera):
        # For multi-tile coops, draw the model centered between the two tiles
        land_slots = self.coop_type.get("land_slots", 1)
        if land_slots > 1:
            # Assume horizontal placement (col + 1)
            # Find the midpoint between the two tiles
            tile_w = GameConstants.LAND_SIZE
            # Offset world_x by half a tile to center between two plots
            world_x = world_x + tile_w / 2
        # compute screen pos for center
        coop_world_y = world_y
        cx, cy = camera.world_to_screen((world_x, coop_world_y))
        # Make the deluxe coop larger
        size_mult = 1.6 if land_slots > 1 else 1.0
        half = int(GameConstants.COOP_SIZE * size_mult // 2)

        # Draw shadow beneath coop
        ShadowManager.draw_shadow(screen, cx, cy, int(GameConstants.COOP_SIZE * size_mult * 1.2), int(GameConstants.COOP_SIZE * size_mult // 2), offset_y=8)

        # Isometric coop building (like a tiny home)
        roof_peak_h = int(20 * size_mult)
        body_h = half + 4

        # Left side wall (darker for depth)
        left_wall_points = [
            (cx - half, cy - body_h),      # Top left
            (cx - half, cy),               # Bottom left
            (cx - half + 4, cy + 4),       # Bottom left corner
            (cx - half + 4, cy - body_h + 4)  # Top left corner (offset)
        ]
        left_color = (100, 150, 80) if self.blight_active else (100, 100, 80)
        pygame.draw.polygon(screen, left_color, left_wall_points)
        
        # Front wall (lighter/tan color)
        front_wall_points = [
            (cx - half, cy - body_h),      # Top left
            (cx + half, cy - body_h),      # Top right
            (cx + half, cy),               # Bottom right
            (cx - half, cy)                # Bottom left
        ]
        color = (100, 180, 100) if self.blight_active else (180, 140, 100)
        pygame.draw.polygon(screen, color, front_wall_points)

        # Right side wall (brown, very dark for depth)
        right_wall_points = [
            (cx + half, cy - body_h),      # Top right
            (cx + half, cy),               # Bottom right
            (cx + half + 4, cy + 4),       # Bottom right corner
            (cx + half + 4, cy - body_h + 4)  # Top right corner (offset)
        ]
        right_color = (120, 140, 80) if self.blight_active else (120, 100, 70)
        pygame.draw.polygon(screen, right_color, right_wall_points)

        # Roof front face (left triangle)
        left_roof_points = [
            (cx - half, cy - body_h),      # Bottom left
            (cx, cy - body_h - roof_peak_h),  # Peak
            (cx - half + 4, cy - body_h + 4)  # Bottom left (offset)
        ]
        left_roof_color = (150, 150, 80) if self.blight_active else (200, 50, 50)
        pygame.draw.polygon(screen, left_roof_color, left_roof_points)

        # Roof front face (right triangle)
        right_roof_points = [
            (cx + half, cy - body_h),      # Bottom right
            (cx, cy - body_h - roof_peak_h),  # Peak
            (cx + half + 4, cy - body_h + 4)  # Bottom right (offset)
        ]
        right_roof_color = (140, 140, 70) if self.blight_active else (180, 40, 40)
        pygame.draw.polygon(screen, right_roof_color, right_roof_points)

        # Roof side face (right side, darker)
        roof_side_points = [
            (cx, cy - body_h - roof_peak_h),  # Peak
            (cx + half, cy - body_h),         # Right edge bottom
            (cx + half + 4, cy - body_h + 4), # Right edge offset
            (cx + 2, cy - body_h - roof_peak_h + 2)  # Peak offset
        ]
        roof_side_color = (120, 120, 60) if self.blight_active else (140, 30, 30)
        pygame.draw.polygon(screen, roof_side_color, roof_side_points)

        # Draw chickens (they will compute their own screen pos using camera)
        for chicken in self.chickens:
            chicken.draw(screen, world_x, world_y, camera)

    def has_blight(self):
        """Check if any chicken in this coop has blight"""
        return self.blight_active

    def calculate_blight_chance(self, dt):
        if self.blight_active:
            return
        # Base chance scaled by chickens and coop type's blight multiplier
        base_chance = GameConstants.BLIGHT_CHANCE * len(self.chickens)
        multiplier = self.coop_type.get("blight_multiplier", 1.0)
        chance_per_second = base_chance * multiplier
        chance_this_frame = chance_per_second * dt
        if random.random() < chance_this_frame:
            self.blight_active = True

    def get_total_production_rate(self):
        """Calculate total eggs produced per second"""
        return (GameConstants.GameEconomyConstants.BLIGHT_PENALTY if self.blight_active else 1) * (len(self.chickens) * GameConstants.GameEconomyConstants.CHICKEN_PRODUCTION_RATE)

    def update_feed(self, dt):
        """Update feed level and handle starvation.
        
        Args:
            dt: Delta time in seconds
        """
        # Consume feed based on number of chickens
        # Feed consumption: FeedConstants.FEED_CONSUMPTION_RATE % per chicken per minute
        consumption_per_second = (len(self.chickens) * GameConstants.FeedConstants.FEED_CONSUMPTION_RATE) / 60.0
        self.feed_level -= consumption_per_second * dt
        self.feed_level = max(0, self.feed_level)  # Can't go below 0
        
        # Handle starvation if feed is critically low
        if self.feed_level < GameConstants.FeedConstants.STARVATION_THRESHOLD and len(self.chickens) > 0:
            # Calculate how many chickens die this frame
            deaths_this_frame = GameConstants.FeedConstants.STARVATION_DEATH_RATE * len(self.chickens) * dt
            
            # Remove chickens one at a time as deaths accumulate
            while deaths_this_frame >= 1.0 and len(self.chickens) > 0:
                self.chickens.pop()
                deaths_this_frame -= 1.0
    
    def buy_feed(self, amount: float = 50.0):
        """Add feed to this coop.
        
        Args:
            amount: Amount of feed to add (as % of capacity)
        """
        self.feed_level = min(
            GameConstants.FeedConstants.FEED_CAPACITY,
            self.feed_level + amount
        )


@dataclass
class Land:
    """Represents a plot of land that can hold coops"""
    def __init__(self, x, y, row=0, col=0):
        self.x: float = x
        self.y: float = y
        self.row: int = row
        self.col: int = col
        self.coop: Coop = None
        self.is_selected: bool = False
        self.coop_occupying_land = None  # If this land is occupied by a larger coop from another slot

    def draw(self, screen, camera: Camera):
        # Always draw land tile, even if occupied by a multi-slot coop from an adjacent land
        world_x, world_y = grid_to_world(self.row, self.col)
        sx, sy = camera.world_to_screen((world_x, world_y))
        tile_w = GameConstants.LAND_SIZE
        tile_h = GameConstants.LAND_SIZE // 2
        half_w = tile_w // 2
        half_h = tile_h // 2

        cx = int(sx)
        cy = int(sy)
        points = [
            (cx, cy - half_h),
            (cx + half_w, cy),
            (cx, cy + half_h),
            (cx - half_w, cy)
        ]
        pygame.draw.polygon(screen, Color.LIGHT_GREEN, points)

        # Draw border (highlight if selected)
        border_color = Color.YELLOW if self.is_selected else Color.GREEN
        border_width = 4 if self.is_selected else 2
        pygame.draw.polygon(screen, border_color, points, border_width)

        # Draw structure if present (pass world coords so Coop can draw chickens via camera)
        if self.coop:
            self.coop.draw(screen, world_x, world_y, camera)

    def contains_point(self, world_point):
        """Check whether a world-space point (wx,wy) is inside this diamond tile's world area.
        Returns False if this land is occupied by a multi-slot coop.
        """
        if self.coop_occupying_land:
            return False
            
        px, py = world_point
        tile_w = GameConstants.LAND_SIZE
        tile_h = GameConstants.LAND_SIZE // 2
        half_w = tile_w / 2.0
        half_h = tile_h / 2.0
        wx, wy = grid_to_world(self.row, self.col)
        dx = abs(px - wx)
        dy = abs(py - wy)
        # Diamond equation: |dx|/half_w + |dy|/half_h <= 1
        return (dx / half_w) + (dy / half_h) <= 1.0
