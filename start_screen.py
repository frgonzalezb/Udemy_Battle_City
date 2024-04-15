import pygame
import game_config as gc


class StartScreen:

    def __init__(self, main, assets) -> None:
        self.main = main
        self.assets = assets

        # Start screen coordinates
        self.start_y = gc.SCREEN_HEIGHT
        self.end_y = 0

        # Start screen images and rect
        self.image = self.assets.start_screen
        self.rect = self.image.get_rect(topleft=(0, 0))

        # Option positions
        self.option_position = [
            (4 * gc.IMAGE_SIZE, 7.75 * gc.IMAGE_SIZE),
            (4 * gc.IMAGE_SIZE, 8.75 * gc.IMAGE_SIZE),
            (4 * gc.IMAGE_SIZE, 9.75 * gc.IMAGE_SIZE)
        ]
        self.token_index = 0
        self.token_image = self.assets.start_screen_token
        self.token_rect = self.token_image.get_rect(
            topleft=self.option_position[self.token_index]
        )

        self.start_screen_active = True

    def input(self) -> None:
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
        window.blit(self.image, self.rect)

        if self.start_screen_active:
            window.blit(self.token_image, self.token_rect)
