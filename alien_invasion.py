import pygame
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    screen: pygame.Surface

    def __init__(self) -> None:
        """Initalize the game and create game resources."""

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self) -> None:
        """Start the main loop of the game."""

        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouses events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event) -> None:
        """Respond to keypresses."""
        # Movement
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True

        elif event.key == pygame.K_q:
            raise SystemExit()

    def _check_keyup_events(self, event) -> None:
        """Respond to releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == "__main__":
    ai_game = AlienInvasion()
    ai_game.run_game()
