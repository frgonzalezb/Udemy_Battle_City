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

    def __init__(self, main, assets) -> None:
        """
        Non-defined-type params:
            game -- The Game class object.
            assets -- The GameAssets class object.
        """
        self.main = main
        self.assets = assets

        self.obj_groups = {'All_Tanks': pygame.sprite.Group()}

        self.hud = GameHUD(self, self.assets)

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

        FIXME: This function may need refactoring:
        1. Some lines below are direct duplicates from Main.input()
        2. Nested code
        """
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
        self.hud.update()
        self.player_1.update()
        self.player_2.update()

    def draw(self, window: pygame.Surface) -> None:
        """
        Draws the given window object on the screen.
        """
        self.hud.draw(window)
        self.player_1.draw(window)
        self.player_2.draw(window)
