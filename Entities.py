from dataclasses import dataclass
from typing import List
from Constants import GameConstants, Color
from Camera import Camera, grid_to_world
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

        # small shadow under chicken
        shadow_rect = pygame.Rect(cx - body_w // 3, cy + body_h // 2, body_w // 1, max(3, body_h // 6))
        pygame.draw.ellipse(screen, (50, 30, 20), shadow_rect)


@dataclass
class Coop:
    """Represents a chicken coop (logical entity). Drawn by passing world coordinates and camera."""
    def __init__(self):
        self.chickens: List[Chicken] = []
        self.blight_active = False
        self.eggs_produced: float = 0.0

    def draw(self, screen, world_x, world_y, camera: Camera):
        # compute screen pos for center
        # offset coop upward in world space so it sits on top of the land tile
        tile_h = GameConstants.LAND_SIZE // 2
        # shift up by half the tile height so coop bottom aligns with tile's lower point
        coop_world_y = world_y - tile_h * 0.5
        cx, cy = camera.world_to_screen((world_x, coop_world_y))
        half = GameConstants.COOP_SIZE // 2
        # roof/top (small diamond)
        roof_h = 16
        roof_points = [
            (cx, cy - half - roof_h),
            (cx + half, cy - half),
            (cx, cy - half + roof_h),
            (cx - half, cy - half)
        ]
        pygame.draw.polygon(screen, Color.RED, roof_points)

        # front face (slightly darker)
        front_points = [
            (cx - half, cy - half),
            (cx, cy - half + roof_h),
            (cx + half, cy - half),
            (cx + half, cy + half),
            (cx - half, cy + half)
        ]
        pygame.draw.polygon(screen, Color.GREEN if self.blight_active else Color.DARK_BROWN, front_points)

        # side face (lighter)
        side_points = [
            (cx + half, cy - half),
            (cx, cy - half + roof_h),
            (cx, cy + half + 4),
            (cx + half, cy + half)
        ]
        pygame.draw.polygon(screen, Color.DARK_GREEN if self.blight_active else Color.TAN, side_points)

        # # door as a trapezoid on the front face
        # front_top_y = cy - half + roof_h
        # front_bottom_y = cy + half
        # door_h = int((front_bottom_y - front_top_y) * 0.6)
        # door_w = int(GameConstants.COOP_SIZE * 0.28)
        # door_top_y = front_bottom_y - door_h - 6
        # door_points = [
        #     (cx - door_w // 2, door_top_y),
        #     (cx + door_w // 2, door_top_y),
        #     (cx + int(door_w * 0.9), front_bottom_y - 6),
        #     (cx - int(door_w * 0.9), front_bottom_y - 6)
        # ]
        # pygame.draw.polygon(screen, Color.DARK_GREEN, door_points)
        # knob_x = cx + door_w // 3
        # knob_y = door_top_y + door_h // 2
        # pygame.draw.circle(screen, Color.YELLOW, (knob_x, knob_y), 3)

        # Draw chickens (they will compute their own screen pos using camera)
        for chicken in self.chickens:
            chicken.draw(screen, world_x, world_y, camera)

    def has_blight(self):
        """Check if any chicken in this coop has blight"""
        return self.blight_active

    def calculate_blight_chance(self, dt):
        if self.blight_active:
            return
        # Simple chance: 10% chance every 10 seconds, scaled by number of chickens (more chickens = higher chance)
        chance_per_second = 0.01 * len(self.chickens)
        chance_this_frame = chance_per_second * dt
        if random.random() < chance_this_frame:
            self.blight_active = True

    def get_total_production_rate(self):
        """Calculate total eggs produced per second"""
        return (GameConstants.GameEconomyConstants.BLIGHT_PENALTY if self.blight_active else 1) * (len(self.chickens) * GameConstants.GameEconomyConstants.CHICKEN_PRODUCTION_RATE)


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

    def draw(self, screen, camera: Camera):
        # Draw isometric diamond tile centered at grid world position
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
        """Check whether a world-space point (wx,wy) is inside this diamond tile's world area."""
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
