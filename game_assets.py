import pygame
import game_config as gc


class GameAssets:
    """
    Represents objects such as images and sounds for the game.
    """

    def __init__(self) -> None:
        # Start screen images
        self.start_screen = self.load_image_assets(
            filename='start_screen',
            scale=True,
            size=(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        self.start_screen_token = self.load_image_assets(
            filename='token',
            scale=True,
            size=(gc.IMAGE_SIZE, gc.IMAGE_SIZE)
        )

        # Spritesheet images
        spritesheet_filenames = [
            'battle_city',
            'numbers_black_white',
            'numbers_black_orange'
        ]
        self.spritesheet_images = {
            image: self.load_image_assets(image)
            for image in spritesheet_filenames
        }

        # TODO: Images related to the characters
        self.tank_images = self._load_all_tank_sprites()

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
        self.scoresheet_images = {
            image: self.load_image_assets(image)
            for image in scoresheet_filenames
        }

    def _load_all_tank_sprites(self):
        """
        Gets all the tank sprites from the spritesheet and
        sort them into a dictionary.
        """
        tank_dict = self._create_tank_sprite_dict()

        for row in range(16):
            for col in range(16):
                surface = self._create_tank_surfaces(row, col)
                level = self._sort_tanks_into_levels(row)
                group = self._sort_tanks_into_groups(row, col)
                direction = self._sort_tanks_by_direction(col)
                tank_dict[level][group][direction].append(surface)

        return tank_dict

    def _create_tank_sprite_dict(self):
        """
        Generates a dictionary as base for loading tank surface images.
        """
        directions = {
            direction: []
            for direction in ['Up', 'Down', 'Left', 'Right']
        }

        groups = {
            group: directions
            for group in ['Gold', 'Silver', 'Green', 'Special']
        }

        tanks = {
            f'Tank_{tank}': groups
            for tank in range(8)
        }

        return tanks

    def _create_tank_surfaces(self, row: int, col: int):
        """
        Creates a new surface image for each of the sprites
        from a given spritesheet.
        """
        surface = pygame.Surface(size=(gc.SPRITE_SIZE, gc.SPRITE_SIZE))
        surface.fill(color=gc.RGB_BLACK)
        surface.blit(
            source=self.spritesheet_images['battle_city'],
            dest=(0, 0),
            area=(
                col * gc.SPRITE_SIZE,
                row * gc.SPRITE_SIZE,
                gc.SPRITE_SIZE,
                gc.SPRITE_SIZE
            )
        )
        surface.set_colorkey(gc.RGB_BLACK)
        surface = self.scale_sprite(surface=surface, scale=gc.IMAGE_SIZE)

        return surface

    def _sort_tanks_into_levels(self, row: int):
        """
        Sorts the tanks according to their given row in the spritesheet.

        If the row number being passed is higher than seven,
        the % operator converts it back down to within the 0 to 7 range
        and return the level from the tank's level dictionary.
        """
        tank_levels = {
            level: f'Tank_{level}'
            for level in range(8)
        }

        return tank_levels[row % 8]

    def _sort_tanks_into_groups(self, row: int, col: int):
        """
        Returns each tank sprite into its proper color group.
        """
        if (0 <= row <= 7) and (0 <= col <= 7):
            return 'Gold'
        elif (8 <= row <= 15) and (0 <= col <= 7):
            return 'Green'
        elif (0 <= row <= 7) and (8 <= col <= 15):
            return 'Silver'
        else:
            return 'Special'

    def _sort_tanks_by_direction(self, col: int):
        """
        Returns each tank sprite by direction.
        """
        if (col % 7 <= 1):
            return 'Up'
        elif (col % 7 <= 3):
            return 'Left'
        elif (col % 7 <= 5):
            return 'Down'
        else:
            return 'Right'

    def scale_sprite(self, surface: pygame.Surface, scale: int):
        """
        Scales any given surface-type image (sprite),
        according to the scale passed in.
        """
        surface = pygame.transform.scale(surface, (scale, scale))
        return surface

    def load_image_assets(
            self,
            filename: str,
            scale: bool = False,
            size: tuple = (0, 0)
            ):
        """
        Loads (and transforms) the individual image as needed.

        NOTE: All images must be in the "assets/img/" folder and
        be in PNG format in order to work!
        """
        try:
            path = f'./assets/img/{filename}.png'
            image = pygame.image.load(path).convert_alpha()
        except FileNotFoundError as e:
            print(f'File {filename}.png not found: {e}')

        if scale:
            image = pygame.transform.scale(image, size)

        return image
