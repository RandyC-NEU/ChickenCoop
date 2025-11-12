from Constants import ScreenDimensions, GameConstants, Color
from Ui import Button
from Entities import Land, Coop, Chicken
from Camera import Camera, grid_to_world
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
        pygame.display.set_caption("Chicken Coop Tycoon")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        self.state = None
        self.state = self.GameState.PLAYING
        self.running = True

        # Game variables
        self.money = 500.0
        self.total_eggs = 0.0
        self.lands: List[Land] = []
        self.game_time = 0.0
        self.selected_land = None
        # camera pan speed (world units/sec)
        self.pan_speed = Camera.PAN_SPEED

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
            'buy_coop': Button(button_x, button_y + 50, button_width, button_height, f"Buy Coop ${GameConstants.GameEconomyConstants.COOP_COST}", Color.TAN, Color.BLACK),
            'buy_chicken': Button(button_x, button_y + 100, button_width, button_height, f"Buy Chicken ${GameConstants.GameEconomyConstants.CHICKEN_COST}", Color.YELLOW, Color.BLACK),
            'sell_eggs': Button(button_x, button_y + 150, button_width, button_height, "Sell All Eggs", Color.GREEN, Color.WHITE),
        }
        self.blight_buttons = {
            'buy_blight_cure': Button(button_x, button_y + 220, button_width, button_height, "Buy Blight Cure $200", Color.RED, Color.WHITE),
            'cull_blighted_chickens': Button(button_x, button_y + 270, button_width, button_height, "Cull Blighted Chickens", Color.RED, Color.WHITE)
        }

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update_hover(mouse_pos)
        for button in self.blight_buttons.values():
            button.update_hover(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    self.handle_clicks(mouse_pos)
                # right-click: start drag (we'll implement pan later)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = self.GameState.PAUSED if self.state == self.GameState.PLAYING else self.GameState.PLAYING

    def handle_clicks(self, mouse_pos):
        if self.buttons['buy_land'].is_clicked(mouse_pos):
            self.buy_land()
        elif self.buttons['buy_coop'].is_clicked(mouse_pos):
            if self.selected_land:
                self.buy_coop()
        elif self.buttons['buy_chicken'].is_clicked(mouse_pos):
            if self.selected_land:
                self.buy_chicken()
        elif self.buttons['sell_eggs'].is_clicked(mouse_pos):
            self.sell_eggs()
        elif self.blight_buttons['buy_blight_cure'].is_clicked(mouse_pos):
            if any(land.coop.has_blight() for land in self.lands if land.coop) and self.money >= 200:
                self.money -= 200
                for land in self.lands:
                    if land.coop:
                        land.coop.blight_active = False
        elif self.blight_buttons['cull_blighted_chickens'].is_clicked(mouse_pos):
            if any(land.coop.has_blight() for land in self.lands if land.coop):
                for land in self.lands:
                    if land.coop:
                        land.coop.chickens.clear()
                        land.coop.blight_active = False
        else:
            # Convert screen→world and select land
            world_mouse = self.camera.screen_to_world(mouse_pos)
            for land in self.lands:
                if land.contains_point(world_mouse):
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

    def buy_coop(self):
        if not self.selected_land:
            return
        if self.money >= GameConstants.GameEconomyConstants.COOP_COST and not self.selected_land.coop:
            self.money -= GameConstants.GameEconomyConstants.COOP_COST
            self.selected_land.coop = Coop()

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
        for land in self.lands:
            if land.coop:
                land.coop.calculate_blight_chance(dt)
                production_rate = land.coop.get_total_production_rate()
                eggs_produced = production_rate * dt
                land.coop.eggs_produced += eggs_produced
                self.total_eggs += eggs_produced

    def draw(self):
        self.screen.fill(Color.LIGHT_BROWN)
        for land in self.lands:
            land.is_selected = (land is self.selected_land)
        for land in sorted(self.lands, key=lambda l: (l.row + l.col)):
            land.draw(self.screen, self.camera)

        pygame.draw.rect(self.screen, Color.GRAY, (ScreenDimensions.SCREEN_WIDTH - 180, 0, 180, ScreenDimensions.SCREEN_HEIGHT))
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
