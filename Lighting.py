"""Lighting and visual effects system."""
import pygame
from Constants import LightingConstants, ScreenDimensions
import math


class ShadowManager:
    """Handles drawing drop shadows beneath game entities."""
    
    @staticmethod
    def draw_shadow(screen, screen_x, screen_y, width, height, offset_y=0):
        """
        Draw a soft elliptical shadow beneath an entity.
        
        Args:
            screen: pygame surface to draw on
            screen_x: screen-space x coordinate of entity center
            screen_y: screen-space y coordinate of entity center
            width: width of the shadow ellipse
            height: height of the shadow ellipse
            offset_y: how far below the entity the shadow appears
        """
        shadow_y = screen_y + height // 2 + offset_y
        shadow_rect = pygame.Rect(
            screen_x - width // 2,
            shadow_y,
            width,
            max(2, height // 4)
        )
        
        # Create a surface for the shadow with per-pixel alpha
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_color = (0, 0, 0, LightingConstants.SHADOW_ALPHA)
        pygame.draw.ellipse(shadow_surface, shadow_color, shadow_surface.get_rect())
        
        # Blur effect: draw it twice to soften edges
        screen.blit(shadow_surface, shadow_rect)


class LightingSystem:
    """Manages time-of-day lighting and color tinting."""
    
    def __init__(self):
        self.game_time = 0.0
        self.current_tint = LightingConstants.MIDDAY_TINT
    
    def update(self, game_time):
        """Update lighting based on current game time."""
        self.game_time = game_time
        self.current_tint = self._calculate_tint(game_time)
    
    def _calculate_tint(self, game_time):
        """
        Calculate the lighting tint based on time of day.
        Returns RGB tuple representing current light color.
        """
        day_cycle = LightingConstants.DAY_CYCLE_LENGTH
        time_in_cycle = game_time % day_cycle
        progress = time_in_cycle / day_cycle  # 0 to 1
        
        # 4-point day cycle: morning -> midday -> evening -> night -> morning
        if progress < 0.25:
            # Morning (0 to 0.25): dawn to morning
            t = progress / 0.25
            return self._lerp_color(LightingConstants.NIGHT_TINT, LightingConstants.MORNING_TINT, t)
        elif progress < 0.5:
            # Midday (0.25 to 0.5): morning to noon
            t = (progress - 0.25) / 0.25
            return self._lerp_color(LightingConstants.MORNING_TINT, LightingConstants.MIDDAY_TINT, t)
        elif progress < 0.75:
            # Evening (0.5 to 0.75): noon to evening
            t = (progress - 0.5) / 0.25
            return self._lerp_color(LightingConstants.MIDDAY_TINT, LightingConstants.EVENING_TINT, t)
        else:
            # Night (0.75 to 1.0): evening back to night
            t = (progress - 0.75) / 0.25
            return self._lerp_color(LightingConstants.EVENING_TINT, LightingConstants.NIGHT_TINT, t)
    
    @staticmethod
    def _lerp_color(color1, color2, t):
        """Linear interpolation between two colors. t: 0 to 1."""
        return (
            int(color1[0] * (1 - t) + color2[0] * t),
            int(color1[1] * (1 - t) + color2[1] * t),
            int(color1[2] * (1 - t) + color2[2] * t)
        )
    
    def apply_tint_to_screen(self, screen):
        """
        Apply the current lighting tint to the entire screen.
        Creates a subtle color overlay for time-of-day effect.
        """
        # Create a tint surface
        tint_surface = pygame.Surface((screen.get_width(), screen.get_height()))
        tint_surface.fill(self.current_tint)
        tint_surface.set_alpha(15)  # Very subtle tint
        screen.blit(tint_surface, (0, 0))


class VignetteEffect:
    """Creates a darkened vignette around screen edges."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._create_vignette_surface()
    
    def _create_vignette_surface(self):
        """Pre-render the vignette effect surface."""
        self.vignette_surface = pygame.Surface(
            (self.screen_width, self.screen_height),
            pygame.SRCALPHA
        )
        
        # Create radial gradient from transparent center to dark edges
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        for x in range(self.screen_width):
            for y in range(self.screen_height):
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx**2 + dy**2)
                
                # Vignette strength increases toward edges
                vignette_strength = (distance / max_distance) ** 1.5
                vignette_strength = min(1.0, vignette_strength * LightingConstants.VIGNETTE_STRENGTH)
                
                alpha = int(255 * vignette_strength)
                self.vignette_surface.set_at((x, y), (0, 0, 0, alpha))
    
    def apply_vignette(self, screen):
        """Apply the vignette effect to the screen."""
        screen.blit(self.vignette_surface, (0, 0))
