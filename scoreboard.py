import pygame
from ship import Ship


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game) -> None:
        """Initialize the scorekeeping attributes."""

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_highest_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into rendered image."""

        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_highest_score(self):
        highest_score_str = "{:,}".format(self.stats.highest_score)
        self.highest_score_image = self.font.render(highest_score_str, True, self.text_color)

        # Display the score at the top of the screen
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score to the screen."""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highest_score_image, self.highest_score_rect)
        self.screen.blit(self.current_level_image, self.current_level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check if current score is the new highest score."""

        if self.stats.score > self.stats.highest_score:
            self.stats.highest_score = self.stats.score
            self.prep_highest_score()

    def prep_level(self):
        """Turn the level into the rendered image."""

        current_level_str = f"Level {self.stats.current_level}"
        self.current_level_image = self.font.render(current_level_str, True, self.text_color)

        # Position the level below the score
        self.current_level_rect = self.current_level_image.get_rect()
        self.current_level_rect.left = 20
        self.current_level_rect.top = self.score_rect.top

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = pygame.sprite.Group()

        for ship_number in range(self.stats.ships_left + 1):
            ship = Ship(self.ai_game)
            ship.rect.x = 20 + self.current_level_rect.right + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
