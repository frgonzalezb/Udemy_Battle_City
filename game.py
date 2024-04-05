import pygame

# import game_config as gc
from game_hud import GameHUD
from characters import PlayerTank


class Game:
    """
    The main Game object when playing.

    NOTE: The assets are passed here through the Main object, then the
    Game object can use those assets as itself, and when it pleases,
    it can reach one of those assets and use them.
    """

    def __init__(
            self,
            main,
            assets,
            is_player_1_active: bool = True,
            is_player_2_active: bool = False
            ) -> None:

        # Important files
        self.main = main
        self.assets = assets

        # Object groups
        self.obj_groups = {'All_Tanks': pygame.sprite.Group()}

        # Player attributes
        self.is_player_1_active = is_player_1_active
        self.is_player_2_active = is_player_2_active

        # Game HUD
        self.hud = GameHUD(self, self.assets)

        # Level information
        self.level_num = 1

        # Player objects
        if self.is_player_1_active:
            self.player_1 = PlayerTank(
                self,
                self.assets,
                self.obj_groups,
                position=(200, 200),
                direction='Up',
                color='Gold',
            )

        if self.is_player_2_active:
            self.player_2 = PlayerTank(
                self,
                self.assets,
                self.obj_groups,
                position=(400, 200),
                direction='Up',
                color='Green',
                tank_level=1
            )

    def input(self) -> None:
        """
        Handles input events for the game when it's running.
        """
        key_pressed = pygame.key.get_pressed()

        if self.is_player_1_active:
            self.player_1.input(key_pressed)

        if self.is_player_2_active:
            self.player_2.input(key_pressed)

        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            # Keyboard shortcut for quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self) -> None:
        self.hud.update()

        if self.is_player_1_active:
            self.player_1.update()

        if self.is_player_2_active:
            self.player_2.update()

    def draw(self, window: pygame.Surface) -> None:
        """
        Draws the given window object on the screen.
        """
        self.hud.draw(window)
        if self.is_player_1_active:
            self.player_1.draw(window)

        if self.is_player_2_active:
            self.player_2.draw(window)
