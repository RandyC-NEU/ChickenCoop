import pygame
from Constants import Color


class Button:
    """UI Button class"""
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen, font):
        color = Color.LIGHT_GRAY if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, Color.BLACK, self.rect, 2)

        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)


class CollapsiblePanel:
    """A retractable panel that shows coop metrics with expandable/collapsible button."""
    
    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.is_expanded = False
        self.toggle_button = Button(x, y, width, 25, "▼ " + title, Color.GRAY, Color.WHITE)
        
    def toggle(self):
        """Toggle expanded/collapsed state."""
        self.is_expanded = not self.is_expanded
        self.toggle_button.text = ("▲ " if self.is_expanded else "▼ ") + self.title
    
    def draw(self, screen, font, metrics=None):
        """Draw the panel and its contents.
        
        Args:
            screen: Pygame surface to draw on
            font: Font to use for text
            metrics: Dict of metric_name -> value pairs to display
        """
        # Draw toggle button
        self.toggle_button.draw(screen, font)
        
        if not self.is_expanded or metrics is None:
            return
        
        # Draw expanded panel background
        panel_rect = pygame.Rect(self.x, self.y + 25, self.width, self.height - 25)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(screen, Color.BLACK, panel_rect, 2)
        
        # Draw metrics
        metric_font = pygame.font.Font(None, 16)
        y_offset = self.y + 35
        for metric_name, value in metrics.items():
            metric_text = f"{metric_name}: {value}"
            text_surface = metric_font.render(metric_text, True, Color.WHITE)
            screen.blit(text_surface, (self.x + 10, y_offset))
            y_offset += 20
    
    def update_hover(self, mouse_pos):
        """Update button hover state."""
        self.toggle_button.update_hover(mouse_pos)
    
    def is_toggle_clicked(self, mouse_pos):
        """Check if toggle button was clicked."""
        return self.toggle_button.is_clicked(mouse_pos)


class SelectablePanel(CollapsiblePanel):
    """A retractable panel with selectable options (inherits from CollapsiblePanel)."""
    
    def __init__(self, x, y, width, height, title="Select", options=None):
        """
        Args:
            x, y: Position
            width, height: Panel dimensions
            title: Panel title
            options: Dict of {option_key: {"name": str, "cost": int}}
        """
        super().__init__(x, y, width, height, title)
        self.options = options or {}
        self.selected_option = None
        
        # Create buttons for each option
        self.option_buttons = {}
        self._create_option_buttons()
    
    def _create_option_buttons(self):
        """Create clickable buttons for each option."""
        button_y = self.y + 30
        button_height = 35
        for option_key, option_data in self.options.items():
            button_text = f"{option_data['name']} ${option_data.get('cost', 0)}"
            button = Button(
                self.x + 5,
                button_y,
                self.width - 10,
                button_height,
                button_text,
                (100, 100, 100),
                Color.WHITE
            )
            self.option_buttons[option_key] = button
            button_y += button_height + 5
    
    def draw(self, screen, font):
        """Draw the panel and its options. Overrides parent to show buttons instead of metrics."""
        # Draw toggle button
        self.toggle_button.draw(screen, font)
        
        if not self.is_expanded:
            return
        
        # Draw expanded panel background
        panel_height = 30 + len(self.option_buttons) * 40
        panel_rect = pygame.Rect(self.x, self.y + 25, self.width, panel_height)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(screen, Color.BLACK, panel_rect, 2)
        
        # Draw option buttons
        for button in self.option_buttons.values():
            button.draw(screen, font)
    
    def update_hover(self, mouse_pos):
        """Update button hover states. Overrides parent to include option buttons."""
        self.toggle_button.update_hover(mouse_pos)
        if self.is_expanded:
            for button in self.option_buttons.values():
                button.update_hover(mouse_pos)
    
    def get_clicked_option(self, mouse_pos):
        """Return option key if an option was clicked, None otherwise."""
        if not self.is_expanded:
            return None
        for option_key, button in self.option_buttons.items():
            if button.is_clicked(mouse_pos):
                return option_key
        return None

