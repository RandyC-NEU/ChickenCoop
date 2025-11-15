from Constants import ScreenDimensions, GameConstants, Color
from Ui import Button, CollapsiblePanel, SelectablePanel
from Entities import Land, Coop, Chicken
from Camera import Camera, grid_to_world
from Lighting import LightingSystem, VignetteEffect
import pygame
from enum import Enum
from typing import List
import random

class Game:
    class GameState(Enum):
        PLAYING = 1
        PAUSED = 2

    def __init__(self):
        self.screen = pygame.display.set_mode((ScreenDimensions.SCREEN_WIDTH, ScreenDimensions.SCREEN_HEIGHT))
        pygame.display.set_caption("Eggonomics")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        self.state = None
        self.state = self.GameState.PLAYING
        self.running = True

        # Game variables
        self.total_eggs = 0.0
        self.egg_capacity = 200.0
        self.expanded_capacity_price = 650
        self.money = 500.0
        self.lands: List[Land] = []
        self.game_time = 0.0
        self.selected_land = None
        # camera pan speed (world units/sec)
        self.pan_speed = Camera.PAN_SPEED

        # Initialize lighting system
        self.lighting_system = LightingSystem()
        self.vignette_effect = VignetteEffect(ScreenDimensions.SCREEN_WIDTH, ScreenDimensions.SCREEN_HEIGHT)

        # Initialize coop info panel
        self.coop_info_panel = CollapsiblePanel(10, 10, 250, 200, title="Coop Info")

        # Initialize coop selector panel (below coop info panel to avoid overlap)
        self.coop_selector_panel = SelectablePanel(
            10,
            220,
            250,
            150,
            title="Select Coop",
            options={
                "classic": GameConstants.CoopTypes.CLASSIC,
                "deluxe": GameConstants.CoopTypes.DELUXE,
            }
        )

        # initialize map
        self.setup_initial_plot()

        # create camera (centered on map centroid)
        # camera is set in setup_initial_plot

        # Create UI buttons
        self.setup_buttons()

    def setup_initial_plot(self):
        cols = 4
        rows = 3
        # create logical lands (store row/col)
        for row in range(rows):
            for col in range(cols):
                self.lands.append(Land(0, 0, row=row, col=col))
        # center camera on centroid
        wxs = []
        wys = []
        for land in self.lands:
            wx, wy = grid_to_world(land.row, land.col)
            wxs.append(wx)
            wys.append(wy)
        self.camera = Camera(x=sum(wxs) / len(wxs), y=sum(wys) / len(wys), zoom=1.0)

    def setup_buttons(self):
        button_y = 20
        button_height = 40
        button_width = 140
        button_x = ScreenDimensions.SCREEN_WIDTH - button_width - 20
        self.buttons = {
            'buy_land': Button(button_x, button_y, button_width, button_height, f"Buy Land ${GameConstants.GameEconomyConstants.LAND_COST}", Color.LIGHT_GREEN, Color.BLACK),
            'buy_chicken': Button(button_x, button_y + 100, button_width, button_height, f"Buy Chicken ${GameConstants.GameEconomyConstants.CHICKEN_COST}", Color.YELLOW, Color.BLACK),
            'upgrade_egg_capacity': Button(button_x, button_y + 150, button_width, button_height, f"Upgrade Capacity ${self.expanded_capacity_price}", Color.BLUE, Color.WHITE),
            'buy_feed': Button(button_x, button_y + 200, button_width, button_height, f"Buy Feed ${GameConstants.GameEconomyConstants.FEED_COST}", Color.ORANGE, Color.BLACK),
            'sell_eggs': Button(button_x, button_y + 250, button_width, button_height, "Sell All Eggs", Color.GREEN, Color.WHITE),
        }
        self.blight_buttons = {
            'buy_blight_cure': Button(button_x, button_y + 330, button_width, button_height, "Buy Blight Cure $200", Color.RED, Color.WHITE),
            'cull_blighted_chickens': Button(button_x, button_y + 370, button_width, button_height, "Cull Blighted Chickens", Color.RED, Color.WHITE)
        }

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update_hover(mouse_pos)
        for button in self.blight_buttons.values():
            button.update_hover(mouse_pos)
        self.coop_info_panel.update_hover(mouse_pos)
        self.coop_selector_panel.update_hover(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    if self.coop_info_panel.is_toggle_clicked(mouse_pos):
                        self.coop_info_panel.toggle()
                    elif self.coop_selector_panel.is_toggle_clicked(mouse_pos):
                        self.coop_selector_panel.toggle()
                    else:
                        self.handle_clicks(mouse_pos)
                # right-click: start drag (we'll implement pan later)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = self.GameState.PAUSED if self.state == self.GameState.PLAYING else self.GameState.PLAYING

    def handle_clicks(self, mouse_pos):
        # Check for coop selection first (highest priority)
        selected_coop_type = self.coop_selector_panel.get_clicked_option(mouse_pos)
        if selected_coop_type is not None:
            self.buy_coop(selected_coop_type)
            return
        
        # Check regular buttons
        if self.buttons['buy_land'].is_clicked(mouse_pos):
            self.buy_land()
            return
        elif self.buttons['buy_chicken'].is_clicked(mouse_pos):
            if self.selected_land:
                self.buy_chicken()
            return
        elif self.buttons['buy_feed'].is_clicked(mouse_pos):
            self.buy_feed()
            return
        elif self.buttons['sell_eggs'].is_clicked(mouse_pos):
            self.sell_eggs()
            return
        elif self.buttons['upgrade_egg_capacity'].is_clicked(mouse_pos):
            if self.money >= self.expanded_capacity_price:
                self.money -= self.expanded_capacity_price
                self.egg_capacity += 100.0
                self.expanded_capacity_price += 100
            return
        elif self.blight_buttons['buy_blight_cure'].is_clicked(mouse_pos):
            if any(land.coop.has_blight() for land in self.lands if land.coop) and self.money >= 200:
                self.money -= 200
                for land in self.lands:
                    if land.coop:
                        land.coop.blight_active = False
            return
        elif self.blight_buttons['cull_blighted_chickens'].is_clicked(mouse_pos):
            if any(land.coop.has_blight() for land in self.lands if land.coop):
                for land in self.lands:
                    if land.coop:
                        land.coop.chickens.clear()
                        land.coop.blight_active = False
            return
        else:
            # Convert screen→world and select land
            world_mouse = self.camera.screen_to_world(mouse_pos)
            for land in self.lands:
                if land.contains_point(world_mouse):
                    # If this land is occupied by a multi-tile coop, select the land that owns the coop
                    if land.coop_occupying_land:
                        # Find the land that owns this coop
                        for owner_land in self.lands:
                            if owner_land.coop is land.coop_occupying_land:
                                self.selected_land = owner_land
                                return
                    self.selected_land = land
                    return

    def buy_land(self):
        if self.money >= GameConstants.GameEconomyConstants.LAND_COST:
            land_count = len(self.lands)
            cols = 4
            row = land_count // cols
            col = land_count % cols
            self.lands.append(Land(0, 0, row=row, col=col))
            self.money -= GameConstants.GameEconomyConstants.LAND_COST

    def buy_coop(self, coop_type_key=None):
        if not self.selected_land or self.selected_land.coop or self.selected_land.coop_occupying_land:
            return
        
        # Get coop type from selector
        if coop_type_key is None:
            return
        
        coop_types = {
            "classic": GameConstants.CoopTypes.CLASSIC,
            "deluxe": GameConstants.CoopTypes.DELUXE,
        }
        coop_type = coop_types.get(coop_type_key)
        if coop_type is None:
            return
        
        coop_cost = coop_type.get("cost", 100)
        land_slots_needed = coop_type.get("land_slots", 1)
        
        # Check if we have enough adjacent slots for multi-slot coops
        if land_slots_needed > 1:
            # For deluxe coop, check if the land to the right is available
            adjacent_col = self.selected_land.col + 1
            adjacent_land = None
            for land in self.lands:
                if land.row == self.selected_land.row and land.col == adjacent_col:
                    adjacent_land = land
                    break
            
            if not adjacent_land or adjacent_land.coop or adjacent_land.coop_occupying_land:
                # Not enough free adjacent land
                return
        
        if self.money >= coop_cost:
            self.money -= coop_cost
            coop = Coop(coop_type=coop_type)
            self.selected_land.coop = coop
            
            # If multi-slot, mark adjacent land as occupied
            if land_slots_needed > 1:
                adjacent_col = self.selected_land.col + 1
                for land in self.lands:
                    if land.row == self.selected_land.row and land.col == adjacent_col:
                        land.coop_occupying_land = coop
                        break
            
            self.coop_selector_panel.toggle()  # Close the panel after selection

    def buy_chicken(self):
        if not self.selected_land:
            return
        if self.money >= GameConstants.GameEconomyConstants.CHICKEN_COST and self.selected_land.coop:
            tile_w = GameConstants.LAND_SIZE
            tile_h = GameConstants.LAND_SIZE // 2
            off_x = random.uniform(-tile_w * 0.25, tile_w * 0.25)
            off_y = random.uniform(0, tile_h * 0.4)
            self.selected_land.coop.chickens.append(Chicken(off_x, off_y))
            self.money -= GameConstants.GameEconomyConstants.CHICKEN_COST

    def sell_eggs(self):
        if self.total_eggs > 0:
            money_earned = self.total_eggs * GameConstants.GameEconomyConstants.EGG_SELL_PRICE
            self.money += money_earned
            self.total_eggs = 0

    def buy_feed(self):
        """Buy feed for the selected coop."""
        if not self.selected_land or not self.selected_land.coop:
            return
        if self.money >= GameConstants.GameEconomyConstants.FEED_COST:
            self.money -= GameConstants.GameEconomyConstants.FEED_COST
            self.selected_land.coop.buy_feed(50.0)  # Add 50% feed capacity

    def update(self, dt):
        if self.state == self.GameState.PAUSED:
            return
        # camera pan with WASD
        keys = pygame.key.get_pressed()
        dx = 0.0
        dy = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.pan_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.pan_speed * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.pan_speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.pan_speed * dt
        # apply camera movement
        self.camera.x += dx
        self.camera.y += dy

        self.game_time += dt
        self.lighting_system.update(self.game_time)

        for land in self.lands:
            if land.coop:
                land.coop.calculate_blight_chance(dt)
                land.coop.update_feed(dt)  # Update feed level and handle starvation
                production_rate = land.coop.get_total_production_rate()
                eggs_produced = int(production_rate * dt)
                land.coop.eggs_produced += eggs_produced
                if (self.total_eggs + eggs_produced <= self.egg_capacity):
                    self.total_eggs += eggs_produced
                else:
                    self.total_eggs = self.egg_capacity

    def draw(self):
        self.screen.fill(Color.LIGHT_BROWN)
        for land in self.lands:
            land.is_selected = (land is self.selected_land)
        for land in sorted(self.lands, key=lambda l: (l.row + l.col)):
            land.draw(self.screen, self.camera)

        # Apply lighting tint and vignette
        self.lighting_system.apply_tint_to_screen(self.screen)
        self.vignette_effect.apply_vignette(self.screen)

        # Draw coop info panel
        panel_metrics = {}
        if self.selected_land and self.selected_land.coop:
            coop = self.selected_land.coop
            panel_metrics = {
                "Chickens": str(len(coop.chickens)),
                "Eggs": f"{coop.eggs_produced:.1f}",
                "Feed": f"{coop.feed_level:.1f}%",
            }
        self.coop_info_panel.draw(self.screen, self.font_small, panel_metrics)

        pygame.draw.rect(self.screen, Color.GRAY, (ScreenDimensions.SCREEN_WIDTH - 180, 0, 180, ScreenDimensions.SCREEN_HEIGHT))
        
        # Draw coop selector panel AFTER the sidebar so it appears on top
        if self.selected_land and not self.selected_land.coop:
            self.coop_selector_panel.draw(self.screen, self.font_small)
        
        for button in self.buttons.values():
            button.draw(self.screen, self.font_small)
        if any(land.coop.has_blight() for land in self.lands if land.coop):
            for button in self.blight_buttons.values():
                button.draw(self.screen, self.font_small)


        money_text = self.font_medium.render(f"Money: ${self.money:.2f}", True, Color.YELLOW)
        self.screen.blit(money_text, (ScreenDimensions.SCREEN_WIDTH - 170, ScreenDimensions.SCREEN_HEIGHT - 150))
        eggs_text = self.font_medium.render(f"Eggs: {self.total_eggs:.1f}", True, Color.ORANGE)
        self.screen.blit(eggs_text, (ScreenDimensions.SCREEN_WIDTH - 170, ScreenDimensions.SCREEN_HEIGHT - 110))
        time_text = self.font_small.render(f"Time: {self.game_time:.1f}s", True, Color.WHITE)
        self.screen.blit(time_text, (ScreenDimensions.SCREEN_WIDTH - 170, ScreenDimensions.SCREEN_HEIGHT - 70))

        if any(land.coop.has_blight() for land in self.lands if land.coop):
            blight_text = self.font_medium.render("BLIGHT ACTIVE!", True, Color.RED)
            self.screen.blit(blight_text, (ScreenDimensions.SCREEN_WIDTH - 170, ScreenDimensions.SCREEN_HEIGHT - 200))
        if self.selected_land:
            info = "Selected"
            if self.selected_land.coop:
                chickens = len(self.selected_land.coop.chickens)
                info += f" Coop ({chickens}🐔)"
            else:
                info += " (empty)"
            selected_text = self.font_small.render(info, True, Color.YELLOW)
            self.screen.blit(selected_text, (ScreenDimensions.SCREEN_WIDTH - 170, ScreenDimensions.SCREEN_HEIGHT - 30))

        if self.state == self.GameState.PAUSED:
            pause_text = self.font_large.render("PAUSED", True, Color.RED)
            pause_rect = pause_text.get_rect(center=(ScreenDimensions.SCREEN_WIDTH // 2, ScreenDimensions.SCREEN_HEIGHT // 2))
            pygame.draw.rect(self.screen, Color.BLACK, pause_rect.inflate(20, 20))
            self.screen.blit(pause_text, pause_rect)

        instructions = [
            "1. Click on land to select",
            "2. Click Buy buttons to add",
            "3. Sell eggs to earn $",
            "Press SPACE to pause",
            f"Egg value: ${GameConstants.GameEconomyConstants.EGG_SELL_PRICE}"
        ]
        for i, instruction in enumerate(instructions):
            instr_text = self.font_small.render(instruction, True, Color.WHITE)
            self.screen.blit(instr_text, (10, ScreenDimensions.SCREEN_HEIGHT - 100 + i * 20))

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
