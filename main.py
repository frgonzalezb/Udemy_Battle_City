import pygame
from pygame.surface import Surface
from pygame.time import Clock

import game_config as gc
from game import Game
from game_assets import GameAssets
from screens.level_editor import LevelEditor
from levels import LevelData
from screens.start_screen import StartScreen


class Main:
    """
    Everything starts here.
    """

    def __init__(self) -> None:
        pygame.init()

        # A good game starts with some display settings
        self.screen: Surface = pygame.display.set_mode(
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        pygame.display.set_caption('Battle City Clone')

        # A clock is needed to regulate the speed of the game...
        # ...in order to standarize the game performance.
        self.clock: Clock = Clock()

        # A simple check for the main game loop
        self.run: bool = True

        # All the assets and data for the game
        self.assets: GameAssets = GameAssets()
        self.levels: LevelData = LevelData()

        # Game start screen object and check
        self.start_screen: StartScreen = StartScreen(self, self.assets)
        self.is_start_screen_active: bool = True

        # Game object check and loading
        self.is_game_on: bool = False
        self.game: Game | None = None

        # Level editor check and loading
        self.is_level_editor_on: bool = False
        self.level_creator: LevelEditor | None = None

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
        if self.is_game_on:
            self.game.input()

        if self.is_start_screen_active:
            self.start_screen.input()

        if self.is_level_editor_on:
            self.level_creator.input()

        if (
            not self.is_game_on and
            not self.is_level_editor_on and
            not self.is_start_screen_active
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

        if self.is_start_screen_active:
            self.start_screen.update()

        if self.is_game_on:
            self.game.update()

        if self.game and not self.game.is_active:
            self.start_screen = StartScreen(self, self.assets)
            self.is_start_screen_active = True
            self.is_game_on = False
            self.game = None

        if self.is_level_editor_on:
            self.level_creator.update()

        if self.level_creator and not self.level_creator.is_active:
            self.start_screen = StartScreen(self, self.assets)
            self.is_start_screen_active = True
            self.is_level_editor_on = False
            self.level_creator = None

    def draw(self) -> None:
        """
        Handles all of the screen updates, drawing all of the images to
        the screen and ensuring the screen is refreshed with each cycle.
        """
        self.screen.fill(gc.RGB_BLACK)  # Overall background

        if self.is_start_screen_active:
            self.start_screen.draw(self.screen)

        if self.is_game_on:
            self.game.draw(self.screen)

        if self.is_level_editor_on:
            self.level_creator.draw(self.screen)

        pygame.display.update()

    def start_new_game(self, player_1: bool, player_2: bool) -> None:
        """
        This method is called from the start screen, and then starts
        the game.
        """
        self.is_game_on = True
        self.game = Game(
            self,
            self.assets,
            is_player_1_active=player_1,
            is_player_2_active=player_2
        )  # The actual game!!
        self.is_start_screen_active = False

    def start_level_editor(self) -> None:
        """
        This method is called from the start screen, and then starts
        the level editor.
        """
        self.is_level_editor_on = True
        self.level_creator = LevelEditor(self, self.assets)
        self.is_start_screen_active = False


if __name__ == '__main__':
    # Start the game already!!
    battle_city: Main = Main()
    battle_city.run_game()
    pygame.quit()
