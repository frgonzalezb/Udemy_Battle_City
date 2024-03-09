import pygame
import game_config as gc


class GameAssets:
    '''
    Objects such as images and sounds for the game.
    '''
    ARROW = 'assets/img/arrow.png'
    BATTLE_CITY = 'assets/img/battle_city.png'
    HI_SCORE = 'assets/img/hi_score.png'
    NUMBERS_BLACK_ORANGE = 'assets/img/numbers_black_orange.png'
    NUMBERS_BLACK_WHITE = 'assets/img/numbers_black_white.png'
    PLAYER_1 = 'assets/img/player_1.png'
    PLAYER_2 = 'assets/img/player_2.png'
    PTS = 'assets/img/pts.png'
    SCORESHEET = 'assets/img/scoresheet.png'
    STAGE = 'assets/img/stage.png'
    START_SCREEN = 'assets/img/start_screen.png'
    TOKEN = 'assets/img/token.png'
    TOTAL = 'assets/img/total.png'

    def __init__(self):
        '''
        Initializes all the game assets.
        '''
        self.start_screen = pygame.image.load(self.START_SCREEN)
    