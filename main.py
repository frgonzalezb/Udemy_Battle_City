import pygame

import game_config as gc
from game import Game
from game_assets import GameAssets
from level_editor import LevelEditor
from levels import LevelData
from start_screen import StartScreen


class Main:
    """
    Everything starts here.
    """

    def __init__(self) -> None:
        pygame.init()

        # A good game starts with some display settings
        self.screen = pygame.display.set_mode(
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        pygame.display.set_caption('Battle City Clone')

        # A clock is needed to regulate the speed of the game...
        # ...in order to standarize the game performance.
        self.clock = pygame.time.Clock()

        # A simple check for the main game loop
        self.run = True

        # All the assets and data for the game
        self.assets = GameAssets()
        self.levels = LevelData()

        # Game start screen object and check
        self.start_screen = StartScreen(self, self.assets)
        self.start_screen_active = True

        # Game object check and loading
        self.game_on = False
        self.game = Game(
            self,
            self.assets,
            is_player_1_active=True,
            is_player_2_active=True
        )  # The actual game!!

        # Level editor check and loading
        self.level_editor_on = False
        self.level_creator = LevelEditor(self, self.assets)

    def run_game(self) -> None:
        """
        Runs the main game loop.
        """
        while self.run:
            self.input()
            self.update()
            self.draw()

    def input(self) -> None:
        """
        Handles input events for the game.

        If the actual game is running, all keyboard and mouse events
        will be handled through the actual game object. Otherwise,
        events will be handled throught the level editor object.

        If something goes wrong (e.g. neither the actual game nor the
        level editor run), the QUIT option is available here.
        """
        if self.game_on:
            self.game.input()

        if self.start_screen_active:
            self.start_screen.input()

        if self.level_editor_on:
            self.level_creator.input()

        if (
            not self.game_on and
            not self.level_editor_on and
            not self.start_screen_active
        ):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

    def update(self) -> None:
        """
        Handles all the game updates, which in turn will update all of
        the objects within.
        """
        self.clock.tick(gc.FPS)

        if self.start_screen_active:
            self.start_screen.update()

        if self.game_on:
            self.game.update()

        if self.level_editor_on:
            self.level_creator.update()

    def draw(self) -> None:
        """
        Handles all of the screen updates, drawing all of the images to
        the screen and ensuring the screen is refreshed with each cycle.
        """
        self.screen.fill(gc.RGB_BLACK)  # Overall background

        if self.start_screen_active:
            self.start_screen.draw(self.screen)

        if self.game_on:
            self.game.draw(self.screen)

        if self.level_editor_on:
            self.level_creator.draw(self.screen)

        pygame.display.update()


if __name__ == '__main__':
    # Start the game already!!
    battle_city = Main()
    battle_city.run_game()
    pygame.quit()
