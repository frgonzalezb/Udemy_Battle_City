import pygame
import game_config as gc


class GameAssets:
    '''
    Objects such as images and sounds for the game.
    '''
    ARROW = 'arrow'
    HI_SCORE = 'hi_score'
    PLAYER_1 = 'player_1'
    PLAYER_2 = 'player_2'
    PTS = 'pts'
    SCORESHEET = 'scoresheet'
    STAGE = 'stage'
    TOTAL = 'total'

    def __init__(self):
        '''
        Initializes all the game assets.
        '''
        # Start screen images
        self.start_screen = self.load_image_assets(
            'start_screen', 
            True, 
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        self.start_screen_token = self.load_image_assets(
            'token',
            True,
            (gc.IMG_SIZE, gc.IMG_SIZE)
        )

        # Spritesheet images
        spritesheet_filenames = [
            'battle_city', 
            'numbers_black_white', 
            'numbers_black_orange'
        ]
        self.spritesheet_images = {}
        for image in spritesheet_filenames:
            self.spritesheet_images[image] = self.load_image_assets(image)

        # TODO: Images related to the characters

        # TODO: Game-related images

        # TODO: Game HUD images

        # TODO: Tile images

        # TODO: Number images

        # Scoresheet images
        scoresheet_filenames = [
            'hi-score', 
            'arrow', 
            'player_1', 
            'player_2', 
            'pts', 
            'stage', 
            'total'
        ]
        self.scoresheet_images = {}
        for image in scoresheet_filenames:
            self.scoresheet_images[image] = self.load_image_assets(image)
        
    def load_image_assets(
            self, 
            filename: str, 
            scale: bool = False, 
            size: tuple = (0, 0)
        ):
        '''
        Loads (and transforms) the individual image as needed. 
        NOTE: All images must be in the "assets/img/" folder and 
        in PNG format in order to work!
        '''
        try:
            image = pygame.image.load(f'./assets/img/{filename}.png').convert_alpha()
        except FileNotFoundError as e:
            print(f'File {filename}.png not found: {e}')

        if scale:
            image = pygame.transform.scale(image, size)

        return image
