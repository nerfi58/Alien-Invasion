class Settings:
    """A class to store all settings for Alien Invasion"""

    screen_width: int
    screen_height: int
    bg_color: tuple[int, int, int]

    ship_speed: float
    bottom_movement_limiter_percent: int

    def __init__(self) -> None:
        """Initialize the game settings"""

        # Screen settings
        self.bg_color = (230, 230, 230)

        # Movement settings
        self.ship_speed = 0.5
        self.bottom_movement_limiter_percent = 30
