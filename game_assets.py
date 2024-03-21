import copy
import typing

import pygame

import game_config as gc


class GameAssets:
    """
    Represents objects such as images and sounds for the game.
    """

    def __init__(self) -> None:
        # Start screen images
        self.start_screen = self._load_image(
            filename='start_screen',
            resize=True,
            size=(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        self.start_screen_token = self._load_image(
            filename='token',
            resize=True,
            size=(gc.IMAGE_SIZE, gc.IMAGE_SIZE)
        )

        # Spritesheet images
        spritesheet_filenames = [
            'battle_city',
            'numbers_black_white',
            'numbers_black_orange'
        ]
        self.spritesheet_images = {
            image: self._load_image(image)
            for image in spritesheet_filenames
        }

        # Images related to the characters
        self.tank_images = self._load_all_tank_sprites()
        self.bullet_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.BULLETS,
            gc.RGB_BLACK,
        )
        self.shield_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.SHIELD,
            gc.RGB_BLACK,
        )
        self.spawn_star_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.SPAWN_STAR,
            gc.RGB_BLACK,
        )

        # Game-related images
        self.power_up_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.POWER_UPS,
            gc.RGB_BLACK,
        )
        self.flag_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.FLAGS,
            gc.RGB_BLACK,
        )
        self.explosions_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.EXPLOSIONS,
            gc.RGB_BLACK,
        )
        self.score_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.SCORES,
            gc.RGB_BLACK,
        )

        # Game HUD images
        self.hud_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.HUD_INFO,
            gc.RGB_BLACK,
            False
        )
        self.context_images = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.CONTEXT,
            gc.RGB_BLACK,
            False
        )

        # Tile images
        self.brick_tiles = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.MAP_TILES['bricks'],
            gc.RGB_BLACK,
        )
        self.steel_tiles = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.MAP_TILES['steel'],
            gc.RGB_BLACK,
        )
        self.forest_tiles = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.MAP_TILES['forest'],
            gc.RGB_BLACK,
        )
        self.ice_tiles = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.MAP_TILES['ice'],
            gc.RGB_BLACK,
        )
        self.water_tiles = self._get_specified_sprites(
            self.spritesheet_images['battle_city'],
            gc.MAP_TILES['water'],
            gc.RGB_BLACK,
        )

        # Number images
        self.numbers_black_white = self._get_specified_sprites(
            self.spritesheet_images['numbers_black_white'],
            gc.NUMBERS,
            gc.RGB_BLACK,
        )
        self.numbers_black_orange = self._get_specified_sprites(
            self.spritesheet_images['numbers_black_orange'],
            gc.NUMBERS,
            gc.RGB_BLACK,
        )

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
            image: self._load_image(image)
            for image in scoresheet_filenames
        }

    def _load_all_tank_sprites(self) -> dict[str, dict[str, dict[str, list]]]:
        """
        Loads all the tank sprites from the spritesheet and
        puts them into the blank tank dictionary.
        """
        tanks = self._create_tank_dict()

        for row in range(16):
            for col in range(16):
                surface = self._create_tank_surface(row, col)
                level = self._sort_tanks_into_levels(row)
                group = self._sort_tanks_into_groups(row, col)
                direction = self._sort_tanks_by_direction(col)
                tanks[level][group][direction].append(surface)

        return tanks

    def _create_tank_dict(self) -> dict[str, dict[str, dict[str, list]]]:
        """
        Creates a base dictionary which will consequently be filled
        with tank sprites from the spritesheet.
        """
        directions = {
            direction: []
            for direction in ['Up', 'Down', 'Left', 'Right']
        }
        groups = {
            group: copy.deepcopy(directions)
            for group in ['Gold', 'Silver', 'Green', 'Special']
        }
        tanks = {
            f'Tank_{tank}': copy.deepcopy(groups)
            for tank in range(8)
        }
        return tanks

    def _create_tank_surface(self, row: int, col: int) -> pygame.Surface:
        """
        Extracts a tank sprite from the spritesheet and then converts it
        into a Pygame Surface object, based on the given row and column
        values.
        """
        surface = pygame.Surface((gc.SPRITE_SIZE, gc.SPRITE_SIZE))
        surface.fill(gc.RGB_BLACK)
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
        surface = self._resize_sprite(
            surface,
            (gc.IMAGE_SIZE, gc.IMAGE_SIZE)
        )

        return surface

    def _sort_tanks_into_levels(self, row: int) -> str:
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

    def _sort_tanks_into_groups(
            self,
            row: int,
            col: int
            ) -> typing.Literal['Gold', 'Green', 'Silver', 'Special']:
        """
        Sorts each tank sprite into its proper color group, according
        to its row and column position.
        """
        if (0 <= row <= 7) and (0 <= col <= 7):
            return 'Gold'
        elif (8 <= row <= 15) and (0 <= col <= 7):
            return 'Green'
        elif (0 <= row <= 7) and (8 <= col <= 15):
            return 'Silver'
        else:
            return 'Special'

    def _sort_tanks_by_direction(
            self,
            col: int
            ) -> typing.Literal['Up', 'Left', 'Down', 'Right']:
        """
        Sorts each tank sprite by direction, according to its column
        position.
        """
        if (col % 7 <= 1):
            return 'Up'
        elif (col % 7 <= 3):
            return 'Left'
        elif (col % 7 <= 5):
            return 'Down'
        else:
            return 'Right'

    def _resize_sprite(
            self,
            surface: pygame.Surface,
            resize_values: tuple[int, int]
            ) -> pygame.Surface:
        """
        Resizes any given Pygame Surface object, according to the values
        passed in.
        """
        return pygame.transform.scale(surface, resize_values)

    def _load_image(
            self,
            filename: str,
            resize: bool = False,
            size: tuple[int, int] = (0, 0)
            ) -> pygame.Surface:
        """
        Loads an image and returns it as a Pygame Surface object.
        Resizing the image is optionally available through the given
        parameters.

        NOTE: All images must be in the "assets/img/" folder and
        be in PNG format in order to work!
        """
        try:
            path = f'./assets/img/{filename}.png'
            image = pygame.image.load(path).convert_alpha()
        except FileNotFoundError as e:
            print(f'File {filename}.png not found: {e}')

        if resize:
            image = self._resize_sprite(image, size)

        return image

    def _get_specified_sprites(
            self,
            spritesheet,
            sprite_coord_dict: dict,
            color,
            transparent: bool = True
            ) -> dict:
        """
        Adds the specified sprite from the spritesheet as per the
        coordinates received from the sprite dictionary.
        """
        sprites = {}
        for key, pos in sprite_coord_dict.items():
            image = self._get_image(
                spritesheet,
                pos['pos_x'],
                pos['pos_y'],
                pos['width'],
                pos['height'],
                color,
                transparent
            )
            sprites.setdefault(key, image)

        return sprites

    def _get_image(
            self,
            spritesheet,
            pos_x: int,
            pos_y: int,
            width: int,
            height: int,
            color: tuple[int, int, int],
            transparent: bool = True
            ) -> pygame.Surface:
        """
        Gets a sprite from a given spritesheet.
        """
        surface = pygame.Surface((width, height))
        surface.fill(color)
        surface.blit(spritesheet, (0, 0), (pos_x, pos_y, width, height))

        if not transparent:
            return surface

        surface.set_colorkey(color)
        surface = self._resize_sprite(surface, (gc.IMAGE_SIZE, gc.IMAGE_SIZE))

        return surface
