import pygame
from settings import Settings


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    screen: pygame.Surface

    def __init__(self) -> None:
        """Initalize the game and create game resources."""

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self) -> None:
        """Start the main loop of the game."""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()

            self.screen.fill(self.settings.bg_color)

            # Make the most recently drawn screen visible.
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
