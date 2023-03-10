import time
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


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

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run_game(self) -> None:
        """Start the main loop of the game."""

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

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

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""

        self.bullets.update()

        # Remove unnecessary bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create the fleet of aliens."""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width * 2)
        number_aliens_x = available_space_x // (alien_width * 2)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        availabe_space_y = self.settings.screen_height - ship_height - (alien_height * 4)
        number_rows = availabe_space_y // (alien_height * 2)

        # Create the full fleet of aliens
        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the position of all aliens in the fleet."""

        self._check_fleet_edges()
        self.aliens.update()

        # Detect player-alien collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Detect if any alien has reached bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):

        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collision"""

        # Check if any bullet hit any alien, if so delete this bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.scoreboard.prep_score()
                self.scoreboard.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.current_level += 1
            self.scoreboard.prep_level()

    def _ship_hit(self):
        """Respond to the ship collision with alien."""

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            time.sleep(0.15)

        else:
            pygame.mouse.set_visible(True)
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Check if any alien have reached bottom of the screen."""

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos) -> None:
        """Start a new game when the player clicks Play button."""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()


if __name__ == "__main__":
    ai_game = AlienInvasion()
    ai_game.run_game()
