import pygame
from pygame.math import Vector2


class Ship:
    """A class to manage ship."""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        self.position = Vector2(self.rect.x, self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme(self) -> None:
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self) -> None:
        """Update ship position based on the movement flag."""
        # Update the ships x value, NOT the rect
        right = self.moving_right and self.rect.right < self.screen_rect.right
        left = self.moving_left and self.rect.left > 0
        up = (
            self.moving_up
            and self.rect.top >= (100 - self.settings.bottom_movement_limiter_percent) * 0.01 * self.screen_rect.bottom
        )
        down = self.moving_down and self.rect.bottom < self.screen_rect.bottom

        move = Vector2(right - left, down - up)
        if move.length_squared() > 0:
            move.scale_to_length(self.settings.ship_speed)
            self.position += move

        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)
