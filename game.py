import pygame

# import game_config as gc
from main import Main
from game_assets import GameAssets
from characters import PlayerTank


class Game:
    """
    The main Game object when playing.

    NOTE: The assets are passed here through the Main object, then the
    Game object can use those assets as itself, and when it pleases,
    it can reach one of those assets and use them.
    """

    def __init__(self, main: Main, assets: GameAssets) -> None:
        self.main = main
        self.assets = assets

        self.obj_groups = {'All_Tanks': pygame.sprite.Group()}

        self.player_1 = PlayerTank(
            self,
            self.assets,
            self.obj_groups,
            (200, 200),
            'Up',
            'Gold',
        )
        self.player_2 = PlayerTank(
            self,
            self.assets,
            self.obj_groups,
            (400, 200),
            'Up',
            'Green',
            1
        )

    def input(self) -> None:
        """
        Handles input events for the game when it's running.
        """
        # FIXME: This needs refactoring.
        # 1. Some lines below are direct duplicates from Main.input()
        # 2. Nested code
        key_pressed = pygame.key.get_pressed()
        self.player_1.input(key_pressed)
        self.player_2.input(key_pressed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            # Keyboard shortcut for quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self) -> None:
        self.player_1.update()
        self.player_2.update()

    def draw(self, window: pygame.Surface) -> None:
        """
        Draws the given window object on the screen.
        """
        self.player_1.draw(window)
        self.player_2.draw(window)
