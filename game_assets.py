import pygame
import game_config as gc


class GameAssets:
    '''
    Objects such as images and sounds for the game.
    '''
    def __init__(self):
        '''
        Initializes the game assets.
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
        self.tank_images = self.__load_all_tank_sprites()

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
        
    def __load_all_tank_sprites(self):
        '''
        Gets all the tank sprites from the spritesheet and 
        sort them into a dictionary.
        '''
        tank_dict = self.__create_tank_sprite_dict()

        for row in range(16):
            for col in range(16):
                surface = self.__create_tank_surfaces(row, col)
                level = self.__sort_tanks_into_levels(row)
                group = self.__sort_tanks_into_groups(row, col)
                direction = self.__sort_tanks_by_direction(col)
                tank_dict[level][group][direction].append(surface)
        
        return tank_dict
    
    def __create_tank_sprite_dict(self):
        '''
        Generates a dictionary as base for loading tank surfaces (sprites).
        '''
        dict = {}
        
        for tank in range(8):
            tank_key = f'Tank_{tank}'
            dict[tank_key] = {}
            
            for group in ['Gold', 'Silver', 'Green', 'Special']:
                dict[tank_key][group] = {}
                
                for direction in ['Up', 'Down', 'Left', 'Right']:
                    dict[tank_key][group][direction] = []

        return dict
    
    def __create_tank_surfaces(self, row: int, col: int):
        '''
        Creates a new image for each of the sprites in a given spritesheet.
        '''
        surface = pygame.Surface((gc.SPRITE_SIZE, gc.SPRITE_SIZE))
        surface.fill(gc.BLACK)
        surface.blit(
            self.spritesheet_images['battle_city'], 
            (0, 0), 
            (
                col * gc.SPRITE_SIZE, 
                row * gc.SPRITE_SIZE, 
                gc.SPRITE_SIZE, 
                gc.SPRITE_SIZE
            )
        )
        surface.set_colorkey(gc.BLACK)
        surface = self.scale_sprite(surface, gc.IMG_SIZE)

        return surface

    def __sort_tanks_into_levels(self, row: int):
        '''
        Sorts the tanks according to their given row in the spritesheet.

        If the row number being passed is higher than seven, 
        the % operator converts it back down to within the 0 to 7 range 
        and return the level from the tank's level dictionary.
        '''
        tank_levels = {}
        for level in range(8):
            tank_levels[level] = f'Tank_{level}'
        return tank_levels[row % 8]
    
    def __sort_tanks_into_groups(self, row: int, col: int):
        '''
        Returns each tank sprite into its proper color group.
        '''
        if (0 <= row <= 7) and (0 <= col <= 7):
            return 'Gold'
        elif (8 <= row <= 15) and (0 <= col <= 7):
            return 'Green'
        elif (0 <= row <= 7) and (8 <= col <= 15):
            return 'Silver'
        else:
            return 'Special'

    def __sort_tanks_by_direction(self, col: int):
        '''
        Returns each tank sprite by direction.
        '''
        if (col % 7 <= 1):
            return 'Up'
        elif (col % 7 <= 3):
            return 'Left'
        elif (col % 7 <= 5):
            return 'Down'
        else:
            return 'Right'

    def scale_sprite(self, surface: pygame.Surface, scale: int):
        '''
        Scales any given sprite (a surface-type image) according to 
        the scale passed in.
        '''
        surface = pygame.transform.scale(surface, (scale, scale))
        return surface

    def load_image_assets(
            self, 
            filename: str, 
            scale: bool = False, 
            size: tuple = (0, 0)
        ):
        '''
        Loads (and transforms) the individual image as needed. 
        
        NOTE: All images must be in the "assets/img/" folder and 
        be in PNG format in order to work!
        '''
        try:
            path = f'./assets/img/{filename}.png'
            image = pygame.image.load(path).convert_alpha()
        except FileNotFoundError as e:
            print(f'File {filename}.png not found: {e}')

        if scale:
            image = pygame.transform.scale(image, size)

        return image
