from Constants import ScreenDimensions, GameConstants

class Camera:
    """Simple camera that transforms world coordinates to screen coordinates and back."""
    # Camera pan speed (world units per second)
    PAN_SPEED = 400

    def __init__(self, x=0.0, y=0.0, zoom=1.0, ui_width=200):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.ui_width = ui_width

    def world_to_screen(self, world_pos):
        wx, wy = world_pos
        # map world coordinates into left area (reserve ui_width on right)
        available_width = ScreenDimensions.SCREEN_WIDTH - self.ui_width
        screen_cx = available_width // 2
        screen_cy = ScreenDimensions.SCREEN_HEIGHT // 2
        sx = int((wx - self.x) * self.zoom + screen_cx)
        sy = int((wy - self.y) * self.zoom + screen_cy)
        return sx, sy

    def screen_to_world(self, screen_pos):
        sx, sy = screen_pos
        available_width = ScreenDimensions.SCREEN_WIDTH - self.ui_width
        screen_cx = available_width // 2
        screen_cy = ScreenDimensions.SCREEN_HEIGHT // 2
        wx = (sx - screen_cx) / self.zoom + self.x
        wy = (sy - screen_cy) / self.zoom + self.y
        return wx, wy


def grid_to_world(row, col, tile_w=GameConstants.LAND_SIZE, tile_h=GameConstants.LAND_SIZE//2):
    """Convert grid coordinates (row,col) to world (cartesian) coordinates for isometric layout.

    Optional tile_w/tile_h override; if not provided uses LAND_SIZE from constants.
    """
    wx = (col - row) * (tile_w / 2.0)
    wy = (col + row) * (tile_h / 2.0)
    return wx, wy
