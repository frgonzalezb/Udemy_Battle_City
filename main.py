import pygame
import game_assets as ga
import game_config as gc


class Main:
    """
    Everything starts here.
    """

    def __init__(self):
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

        # It might be nice to import our game assets here
        self.assets = ga.GameAssets()

    def run_game(self):
        """
        Runs the main game loop.
        """
        while self.run:
            self.input()
            self.update()
            self.draw()

    def input(self):
        """
        Handles input events for the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        """
        Handles all the game updates, which in turn will update all of
        the objects within.
        """
        self.clock.tick(gc.FPS)

    def draw(self):
        """
        Handles all of the screen updates, drawing all of the images to
        the screen and ensuring the screen is refreshed with each cycle.
        """
        self.screen.fill(gc.RGB_BLACK)  # Overall background
        self.screen.blit(
            self.assets.tank_images['Tank_4']['Green']['Down'][0],
            (400, 400)
        )  # dbg
        self.screen.blit(
            self.assets.brick_tiles['small'], (200, 200)
        )  # dbg
        pygame.display.update()


if __name__ == '__main__':
    # Start the game already!!
    battle_city = Main()
    battle_city.run_game()
    pygame.quit()
