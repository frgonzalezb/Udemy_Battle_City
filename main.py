import pygame
import game_config as gc


class Main:
    '''Everything starts here.'''

    def __init__(self) -> None:
        '''Initialize the main game loop object.'''
        pygame.init()

        # Set the display settings
        self.screen = pygame.display.set_mode(
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        pygame.display.set_caption('Battle City Clone')

        # A clock is needed to regulate the speed of the game...
        # ...in order to standarize the game performance.
        self.clock = pygame.time.Clock()

        # A simple check for the main game loop
        self.run = True
