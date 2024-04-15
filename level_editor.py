from typing import KeysView

import pygame

import game_config as gc
from levels import LevelData


class LevelEditor:
    """
    Represents the level editor and all its closely-related objects.
    """

    def __init__(self, main, assets) -> None:
        self.main = main
        self.assets = assets
        self.active = True

        self.level_data = LevelData()
        self.all_levels = []
        for stage in self.level_data.level_data:
            self.all_levels.append(stage)

        self.overlay_screen = self.draw_screen()
        self.matrix = self.create_level_matrix()

        # NOTE: Tiles as numbers for matricial-like operations below!
        self.tile_type = {
            20: self.assets.brick_tiles['small'],
            21: self.assets.steel_tiles['small'],
            22: self.assets.forest_tiles['small'],
            23: self.assets.ice_tiles['small'],
            24: self.assets.water_tiles['small_1'],
            99: self.assets.flag_images['Phoenix_Alive']
        }
        self.inserts = self._get_insert_pieces(self.tile_type.keys())
        self.index = 0
        self.insert_tile = self.inserts[self.index]

        # Icon image as pointer
        self.icon_image = self.assets.tank_images['Tank_4']['Gold']['Up'][0]
        self.icon_rect = self.icon_image.get_rect(
            topleft=(gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP)
        )

    def input(self) -> None:
        # TODO: This seems too similar to Game's input class code
        # AND... too many nested conditional blocks!
        # So, a refactor may be done for the sake of cleanliness!

        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            # Keyboard shortcut for quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False
                self._handle_level_editor_events(event.key)

    def update(self) -> None:
        icon_grid_pos_row: int = (
            (self.icon_rect.top - gc.SCREEN_BORDER_TOP)
            // (gc.IMAGE_SIZE // 2)
        )
        icon_grid_pos_col: int = (
            (self.icon_rect.left - gc.SCREEN_BORDER_LEFT)
            // (gc.IMAGE_SIZE // 2)
        )

        row, col = icon_grid_pos_row, icon_grid_pos_col
        self.matrix[row][col] = self.insert_tile[0]
        self.matrix[row][col + 1] = self.insert_tile[1]
        row += 1
        self.matrix[row][col] = self.insert_tile[2]
        self.matrix[row][col + 1] = self.insert_tile[3]

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.overlay_screen, (0, 0))
        self.draw_grid_to_screen(window)

        for i, row in enumerate(self.matrix):
            for j, tile in enumerate(row):
                if tile == -1:
                    continue
                else:
                    window.blit(
                        self.tile_type[tile],
                        (
                            gc.SCREEN_BORDER_LEFT + (j * gc.IMAGE_SIZE // 2),
                            gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE // 2)
                        )
                    )

        window.blit(self.icon_image, self.icon_rect)
        pygame.draw.rect(window, gc.RGB_GREEN, self.icon_rect, 1)

    def draw_screen(self) -> pygame.Surface:
        """
        Creates the game screen for the level editor.
        """
        overlay_screen = pygame.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        overlay_screen.fill(gc.RGB_GREY)
        pygame.draw.rect(
            overlay_screen,
            gc.RGB_BLACK,
            tuple(value for value in gc.GAME_SCREEN.values())
        )
        return overlay_screen

    def draw_grid_to_screen(self, window) -> None:
        """
        Generates lines to make and print a grid on the game screen.
        """
        vertical_lines = (
            (gc.SCREEN_BORDER_RIGHT - gc.SCREEN_BORDER_LEFT) // gc.IMAGE_SIZE
        )
        horizontal_lines = (
            (gc.SCREEN_BORDER_BOTTOM - gc.SCREEN_BORDER_TOP) // gc.IMAGE_SIZE
        )

        for i in range(vertical_lines):
            pygame.draw.line(
                window,
                gc.RGB_RED,
                (
                    gc.SCREEN_BORDER_LEFT + (i * gc.IMAGE_SIZE),
                    gc.SCREEN_BORDER_TOP
                ),
                (
                    gc.SCREEN_BORDER_LEFT + (i * gc.IMAGE_SIZE),
                    gc.SCREEN_BORDER_BOTTOM
                )
            )
        for i in range(horizontal_lines):
            pygame.draw.line(
                window,
                gc.RGB_RED,
                (
                    gc.SCREEN_BORDER_LEFT,
                    gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE)
                ),
                (
                    gc.SCREEN_BORDER_RIGHT,
                    gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE)
                )
            )

    def create_level_matrix(self) -> list:
        rows: int = (
            (gc.SCREEN_BORDER_BOTTOM - gc.SCREEN_BORDER_TOP)
            // (gc.IMAGE_SIZE // 2)
        )
        cols: int = (
            (gc.SCREEN_BORDER_RIGHT - gc.SCREEN_BORDER_LEFT)
            // (gc.IMAGE_SIZE // 2)
        )
        matrix = []
        for row in range(rows):
            line = []
            for col in range(cols):
                line.append(-1)
            matrix.append(line)

        return matrix

    def _handle_level_editor_events(self, key: int) -> None:
        """
        Utility method that handles the key input events for the level
        editor, in order to clean up a little bit the original input()
        method here.
        """
        if key == pygame.K_d or key == pygame.K_RIGHT:
            self.icon_rect.x += gc.IMAGE_SIZE
            # Preventing the icon to escape
            if self.icon_rect.x >= gc.SCREEN_BORDER_RIGHT:
                self.icon_rect.x = gc.SCREEN_BORDER_RIGHT - gc.IMAGE_SIZE
        if key == pygame.K_a or key == pygame.K_LEFT:
            self.icon_rect.x -= gc.IMAGE_SIZE
            # Preventing the icon to escape
            if self.icon_rect.x <= gc.SCREEN_BORDER_LEFT:
                self.icon_rect.x = gc.SCREEN_BORDER_LEFT
        if key == pygame.K_s or key == pygame.K_DOWN:
            self.icon_rect.y += gc.IMAGE_SIZE
            # Preventing the icon to escape
            if self.icon_rect.y >= gc.SCREEN_BORDER_BOTTOM:
                self.icon_rect.y = gc.SCREEN_BORDER_BOTTOM - gc.IMAGE_SIZE
        if key == pygame.K_w or key == pygame.K_UP:
            self.icon_rect.y -= gc.IMAGE_SIZE
            # Preventing the icon to escape
            if self.icon_rect.y <= gc.SCREEN_BORDER_TOP:
                self.icon_rect.y = gc.SCREEN_BORDER_TOP
        # Cycle through insert pieces
        if key == pygame.K_SPACE:
            self.index += 1
            if self.index >= len(self.inserts):
                self.index = self.index % len(self.inserts)
            self.insert_tile = self.inserts[self.index]
        # Save level
        if key == pygame.K_RETURN:
            self.validate_level()
            self.all_levels.append(self.matrix)
            self.level_data.save(self.all_levels)
            self.main.levels.level_data = self.all_levels
            self.active = False

    def _define_insert_pattern(self, tile: int) -> list[list[int]]:
        """
        This is an utility method for the _get_inserts() one.

        It just returns the repeating matricial pattern for a given tile
        texture passed in as a integer identificator.

        Remember each full-sized grid quadrant is, in turn, divided in
        four quadrants, where the gamer can fill two of them as pieces
        of a tile texture (represented here as numbers for convenience)
        in a predefined cycling pattern.

        NOTE: The value of -1 simply means empty space.
        """
        return [
            [-1, tile, -1, tile],       # vertical right
            [-1, -1, tile, tile],       # bottom row
            [tile, -1, tile, -1],       # vertical left
            [tile, tile, -1, -1],       # top row
            [tile, tile, tile, tile]    # full
        ]

    def _get_insert_pieces(self, tile_numbers: KeysView) -> list[list[int]]:
        """
        Returns the texture inserts for the level editor as a matricial
        list object in a cleaner fashion, as improvement for the manual,
        long and boring way from the course.
        """
        inserts: list = []
        inserts.append([-1, -1, -1, -1])   # empty square

        tile_numbers: list[int] = list(tile_numbers)
        tile_numbers.pop(5)  # removes the Phoenix flag

        for tile in tile_numbers:
            for pattern in self._define_insert_pattern(tile):
                inserts.append(pattern)

        return inserts

    def validate_level(self):
        for cell in gc.ENEMY_TANK_SPAWNS:
            self.matrix[cell[1]][cell[0]] = -1
        for cell in gc.PLAYER_TANK_SPAWNS:
            self.matrix[cell[1]][cell[0]] = -1
        for cell in gc.BASE:
            self.matrix[cell[1]][cell[0]] = -1
        self.matrix[24][12] = 99
        for cell in gc.FORT:
            if self.matrix[cell[1]][cell[0]] == -1:
                self.matrix[cell[1]][cell[0]] = 20  # bricks
