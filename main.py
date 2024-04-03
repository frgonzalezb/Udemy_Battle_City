import pygame

import game
import game_assets as ga
import game_config as gc


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

        self.assets = ga.GameAssets()

        self.game_on = True
        self.game = game.Game(
            self,
            self.assets,
            is_player_1_active=True,
            is_player_2_active=False
        )  # The actual game!!

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

        If the game is running, all keyboard and mouse events will be
        handled through the actual game object.
        """
        if self.game_on:
            self.game.input()
        # else:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.run = False

    def update(self) -> None:
        """
        Handles all the game updates, which in turn will update all of
        the objects within.
        """
        self.clock.tick(gc.FPS)

        if self.game_on:
            self.game.update()

    def draw(self) -> None:
        """
        Handles all of the screen updates, drawing all of the images to
        the screen and ensuring the screen is refreshed with each cycle.
        """
        self.screen.fill(gc.RGB_BLACK)  # Overall background

        if self.game_on:
            self.game.draw(self.screen)

        pygame.display.update()


if __name__ == '__main__':
    # Start the game already!!
    battle_city = Main()
    battle_city.run_game()
    pygame.quit()
