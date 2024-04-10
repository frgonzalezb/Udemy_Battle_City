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
