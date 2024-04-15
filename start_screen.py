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
        self.rect = self.image.get_rect(topleft=(0, self.start_y))
        self.x, self.y = self.rect.topleft
        self.speed = gc.SCREEN_SCROLL_SPEED

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

        self.is_start_screen_active = False

    def input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            # Keyboard shortcut for quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

                # This prevents to enter an option automatically when
                # the RETURN key is pressed during the start screen
                # scrolling!
                if not self.is_start_screen_active:
                    self._defeat_screen_animation()
                else:
                    self._handle_start_screen_events(event.key)

    def update(self) -> None:
        # Check to see if screen is in position
        if not self._animate_screen_into_position():
            return
        self.is_start_screen_active = True

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)

        if self.is_start_screen_active:
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

    def _do_selected_option(self) -> None:
        match self.token_index:
            case 0:
                self.main.start_new_game(player_1=True, player_2=False)
            case 1:
                self.main.start_new_game(player_1=True, player_2=True)
            case 2:
                self.main.start_level_editor()
            case _:
                raise ValueError

    def _animate_screen_into_position(self) -> bool:
        """
        Slides the start screen form the bottom up to the top.
        """
        if self.y == self.end_y:
            return True

        self.y -= self.speed
        if self.y < self.end_y:
            self.y = self.end_y
        self.rect.topleft = (0, self.y)

        return False

    def _defeat_screen_animation(self):
        """
        Complete the screen scrolling animation immediately by pressing
        any key, just as in the original game.
        """
        self.y = self.end_y
        self.rect.topleft = (0, self.y)
