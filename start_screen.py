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
        self.option_positions = [
            (4 * gc.IMAGE_SIZE, 7.75 * gc.IMAGE_SIZE),
            (4 * gc.IMAGE_SIZE, 8.75 * gc.IMAGE_SIZE),
            (4 * gc.IMAGE_SIZE, 9.75 * gc.IMAGE_SIZE)
        ]
        self.token_index = 0
        self.token_image = self.assets.start_screen_token
        self.token_rect = self.token_image.get_rect(
            topleft=self.option_positions[self.token_index]
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
                self._handle_start_screen_events(event.key)

    def update(self) -> None:
        pass

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)

        if self.start_screen_active:
            window.blit(self.token_image, self.token_rect)

    def _handle_start_screen_events(self, key: int) -> None:
        """
        Utility method that handles the key input events for the start
        screen, in order to clean up a little bit the original input()
        method here.
        """
        if key == pygame.K_UP or key == pygame.K_w:
            self.token_index -= 1
            self.token_index = self.token_index % len(self.option_positions)
            self.token_rect.topleft = self.option_positions[self.token_index]
        if key == pygame.K_DOWN or key == pygame.K_s:
            self.token_index += 1
            self.token_index = self.token_index % len(self.option_positions)
            self.token_rect.topleft = self.option_positions[self.token_index]

        if key == pygame.K_RETURN:
            self._do_selected_option()

    def _do_selected_option(self):
        match self.token_index:
            case 0:
                print('Start new one player game')  # dbg
            case 1:
                print('Start new two players game')  # dbg
            case 2:
                print('Start the level editor')  # dbg
