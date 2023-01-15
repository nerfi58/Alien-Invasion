class Settings:
    """A class to store all settings for Alien Invasion"""

    screen_width: int
    screen_height: int
    bg_color: tuple[int, int, int]

    ship_speed: float
    bottom_movement_limiter_percent: int

    bullet_speed: float
    bullet_width: int
    bullet_height: int
    bullet_color = tuple[int, int, int]
    bullets_allowed: int

    alien_speed: float
    fleet_drop_speed: float
    fleet_direction: int  # either 1 or -1

    ship_limit: int
    speedup_scale: float

    def __init__(self) -> None:
        """Initialize the game settings"""

        # Screen settings
        self.bg_color = (230, 230, 230)

        # Movement settings
        self.bottom_movement_limiter_percent = 30

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 15

        # Game settings
        self.ship_limit = 3
        self.speedup_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throghout the game."""

        # Speed settings
        self.ship_speed = 0.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.2

        # 1 represents right, -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
