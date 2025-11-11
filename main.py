import pygame
import math
from enum import Enum
from dataclasses import dataclass

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
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
COOP_COST = 100
CHICKEN_COST = 30
LAND_COST = 150
EGG_SELL_PRICE = 5

COOP_SIZE = 60
CHICKEN_SIZE = 20
LAND_SIZE = 80

# Production rates (eggs per second)
COOP_PRODUCTION_RATE = 0.5  # Half an egg per second
CHICKEN_PRODUCTION_RATE = 0.3  # Chickens produce less than coops


class GameState(Enum):
    PLAYING = 1
    PAUSED = 2


class Button:
    """UI Button class"""
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen, font):
        color = LIGHT_GRAY if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)


@dataclass
class Chicken:
    """Represents a single chicken"""
    x: float
    y: float
    eggs_produced: float = 0.0
    
    def draw(self, screen):
        # Draw chicken body (circle)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), CHICKEN_SIZE // 2)
        # Draw chicken head
        pygame.draw.circle(screen, ORANGE, (int(self.x + 8), int(self.y - 5)), CHICKEN_SIZE // 3)
        # Draw beak
        pygame.draw.polygon(screen, YELLOW, [
            (int(self.x + 12), int(self.y - 5)),
            (int(self.x + 16), int(self.y - 4)),
            (int(self.x + 12), int(self.y - 6))
        ])


@dataclass
class Coop:
    """Represents a chicken coop"""
    x: float
    y: float
    chickens: list
    eggs_produced: float = 0.0
    
    def draw(self, screen):
        # Draw coop structure (rectangle)
        pygame.draw.rect(screen, BROWN, (int(self.x), int(self.y), COOP_SIZE, COOP_SIZE))
        # Draw roof (triangle)
        pygame.draw.polygon(screen, RED, [
            (int(self.x), int(self.y)),
            (int(self.x + COOP_SIZE // 2), int(self.y - 20)),
            (int(self.x + COOP_SIZE), int(self.y))
        ])
        # Draw door
        pygame.draw.rect(screen, DARK_GREEN, (int(self.x + 20), int(self.y + 30), 20, 30))
    
    def get_total_production_rate(self):
        """Calculate total eggs produced per second"""
        return COOP_PRODUCTION_RATE + (len(self.chickens) * CHICKEN_PRODUCTION_RATE)


@dataclass
class Land:
    """Represents a plot of land that can hold coops"""
    x: float
    y: float
    has_structure: bool = False
    structure: Coop = None
    is_selected: bool = False
    
    def draw(self, screen):
        # Draw land background
        pygame.draw.rect(screen, LIGHT_GREEN, (int(self.x), int(self.y), LAND_SIZE, LAND_SIZE))
        
        # Draw border (highlight if selected)
        border_color = YELLOW if self.is_selected else GREEN
        border_width = 4 if self.is_selected else 2
        pygame.draw.rect(screen, border_color, (int(self.x), int(self.y), LAND_SIZE, LAND_SIZE), border_width)
        
        # Draw structure if present
        if self.structure:
            self.structure.draw(screen)
            # Draw chickens
            for chicken in self.structure.chickens:
                chicken.draw(screen)


class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chicken Coop Tycoon")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        self.state = GameState.PLAYING
        self.running = True
        
        # Game variables
        self.money = 500.0
        self.total_eggs = 0.0
        self.lands = []
        self.game_time = 0.0
        self.selected_land = None  # Track which land is selected for coop placement
        self.max_lands = 12  # Start with 12 land plots
        
        # Initialize game board with empty lands
        self.setup_lands()
        
        # Create UI buttons
        self.setup_buttons()
    
    def setup_lands(self):
        """Create initial land plots"""
        spacing = LAND_SIZE + 20
        start_x = 20
        start_y = 20
        cols = 4
        rows = 3
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing
                y = start_y + row * spacing
                self.lands.append(Land(x, y))
    
    def setup_buttons(self):
        """Create UI buttons"""
        button_y = 20
        button_height = 40
        button_width = 140
        
        button_x = SCREEN_WIDTH - button_width - 20
        
        self.buttons = {
            'buy_land': Button(button_x, button_y, button_width, button_height, 
                             f"Buy Land ${LAND_COST}", LIGHT_GREEN, BLACK),
            'buy_coop': Button(button_x, button_y + 50, button_width, button_height,
                             f"Buy Coop ${COOP_COST}", TAN, BLACK),
            'buy_chicken': Button(button_x, button_y + 100, button_width, button_height,
                               f"Buy Chicken ${CHICKEN_COST}", YELLOW, BLACK),
            'sell_eggs': Button(button_x, button_y + 150, button_width, button_height,
                              "Sell All Eggs", GREEN, WHITE),
        }
    
    def handle_events(self):
        """Handle user input"""
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons.values():
            button.update_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_clicks(mouse_pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = GameState.PAUSED if self.state == GameState.PLAYING else GameState.PLAYING
    
    def handle_clicks(self, mouse_pos):
        """Handle button clicks"""
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
        
        else:
            # Check if clicking on a land to select it
            for land in self.lands:
                if (land.x <= mouse_pos[0] < land.x + LAND_SIZE and
                    land.y <= mouse_pos[1] < land.y + LAND_SIZE):
                    self.selected_land = land
                    return
    
    def buy_land(self):
        """Purchase a new land plot"""
        if self.money >= LAND_COST:
            # Add a new land plot
            spacing = LAND_SIZE + 20
            start_x = 20
            start_y = 20
            cols = 4
            
            # Calculate position for new land
            land_count = len(self.lands)
            row = land_count // cols
            col = land_count % cols
            
            x = start_x + col * spacing
            y = start_y + row * spacing
            
            # Check if position is within screen bounds
            if y + LAND_SIZE < SCREEN_HEIGHT - 200:
                self.lands.append(Land(x, y))
                self.money -= LAND_COST
    
    def buy_coop(self):
        """Purchase and place a new coop"""
        if not self.selected_land:
            return
        
        if self.money >= COOP_COST and not self.selected_land.structure:
            self.money -= COOP_COST
            self.selected_land.structure = Coop(
                self.selected_land.x + 10, 
                self.selected_land.y + 10, 
                []
            )
    
    def buy_chicken(self):
        """Purchase and add a chicken to a coop"""
        if not self.selected_land:
            return
        
        if self.money >= CHICKEN_COST and self.selected_land.structure:
            self.money -= CHICKEN_COST
            # Place chicken randomly in coop area
            import random
            chicken_x = self.selected_land.structure.x + random.randint(-15, 15)
            chicken_y = self.selected_land.structure.y + random.randint(20, 50)
            self.selected_land.structure.chickens.append(
                Chicken(chicken_x, chicken_y)
            )
    
    def sell_eggs(self):
        """Sell all eggs for money"""
        if self.total_eggs > 0:
            money_earned = self.total_eggs * EGG_SELL_PRICE
            self.money += money_earned
            self.total_eggs = 0
    
    def update(self, dt):
        """Update game state"""
        if self.state == GameState.PAUSED:
            return
        
        self.game_time += dt
        
        # Update egg production for all coops
        for land in self.lands:
            if land.structure:
                production_rate = land.structure.get_total_production_rate()
                eggs_produced = production_rate * dt
                land.structure.eggs_produced += eggs_produced
                self.total_eggs += eggs_produced
    
    def draw(self):
        """Render game state"""
        self.screen.fill(LIGHT_BROWN)
        
        # Update selection state for all lands
        for land in self.lands:
            land.is_selected = (land is self.selected_land)
        
        # Draw lands and structures
        for land in self.lands:
            land.draw(self.screen)
        
        # Draw UI panel background
        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 180, 0, 180, SCREEN_HEIGHT))
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(self.screen, self.font_small)
        
        # Draw money
        money_text = self.font_medium.render(f"Money: ${self.money:.2f}", True, YELLOW)
        self.screen.blit(money_text, (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 150))
        
        # Draw eggs
        eggs_text = self.font_medium.render(f"Eggs: {self.total_eggs:.1f}", True, ORANGE)
        self.screen.blit(eggs_text, (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 110))
        
        # Draw game time
        time_text = self.font_small.render(f"Time: {self.game_time:.1f}s", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70))
        
        # Draw selected land info
        if self.selected_land:
            info = "Selected"
            if self.selected_land.structure:
                chickens = len(self.selected_land.structure.chickens)
                info += f" Coop ({chickens}🐔)"
            else:
                info += " (empty)"
            selected_text = self.font_small.render(info, True, YELLOW)
            self.screen.blit(selected_text, (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 30))
        
        # Draw pause indicator
        if self.state == GameState.PAUSED:
            pause_text = self.font_large.render("PAUSED", True, RED)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(self.screen, BLACK, pause_rect.inflate(20, 20))
            self.screen.blit(pause_text, pause_rect)
        
        # Draw instructions
        instructions = [
            "1. Click on land to select",
            "2. Click Buy buttons to add",
            "3. Sell eggs to earn $",
            "Press SPACE to pause",
            f"Egg value: ${EGG_SELL_PRICE}"
        ]
        for i, instruction in enumerate(instructions):
            instr_text = self.font_small.render(instruction, True, WHITE)
            self.screen.blit(instr_text, (10, SCREEN_HEIGHT - 100 + i * 20))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()