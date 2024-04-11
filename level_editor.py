import pygame
import game_config as gc


class LevelEditor:

    def __init__(self, main, assets) -> None:
        self.main = main
        self.assets = assets
        self.active = True

        self.level_data = None
        self.all_levels = []

        self.overlay_screen = self.draw_screen()
        self.matrix = self.create_level_matrix()

        self.tile_type = {
            'brick': self.assets.brick_tiles['small'],
            'steel': self.assets.steel_tiles['small'],
            'forest': self.assets.forest_tiles['small'],
            'ice': self.assets.ice_tiles['small'],
            'water': self.assets.water_tiles['small_1'],
            'flag': self.assets.flag_images['Phoenix_Alive']
        }
        self.icon_image = self.assets.tank_images['Tank_4']['Gold']['Up'][0]
        self.icon_rect = self.icon_image.get_rect(
            topleft=(gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP)
        )

    def input(self) -> None:
        # TODO: This seems too similar to Game's input class code
        # So, a refactor may be done for the sake of cleanliness!

        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            # Keyboard shortcut for quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self) -> None:
        pass

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.overlay_screen, (0, 0))
        self.draw_grid_to_screen(window)
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
        rows = (
            (gc.SCREEN_BORDER_BOTTOM - gc.SCREEN_BORDER_TOP)
            // (gc.IMAGE_SIZE // 2)
        )
        cols = (
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
