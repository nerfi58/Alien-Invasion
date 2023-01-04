class Settings:
    """A class to store all settings for Alien Invasion"""

    screen_width: int
    screen_height: int
    bg_color: tuple[int, int, int]

    def __init__(self) -> None:
        """Initialize the game settings"""

        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)
