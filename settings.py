class Settings:
    """A class to store all settings for Alien Invasion"""

    screen_width: int
    screen_height: int
    bg_color: tuple[int, int, int]

    movement_bg_color = tuple[int, int, int]

    ship_speed: float
    bottom_movement_limiter_percent: int

    def __init__(self) -> None:
        """Initialize the game settings"""

        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        self.movement_bg_color = (0, 0, 0)

        # Movement settings
        self.ship_speed = 0.5
        self.bottom_movement_limiter_percent = 30
