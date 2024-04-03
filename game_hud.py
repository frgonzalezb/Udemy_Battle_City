import pygame
import game_config as gc


class GameHUD:
    """
    Blueprint for the game HUD object.
    """

    def __init__(self, game, assets) -> None:
        """
        Non-defined-type params:
            game -- The Game class object.
            assets -- The GameAssets class object.
        """
        self.game = game
        self.assets = assets
        self.images = self.assets.hud_images
        self.hud_overlay = self.generate_hud_overlay_screen()

        # Player lives and display
        self.is_player_1_active = False
        self.player_1_lives = 0
        self.player_1_lives_image = None
        self.is_player_2_active = False
        self.player_2_lives = 0
        self.player_2_lives_image = None

    def update(self):
        # Update the number of player lives available
        self.is_player_1_active = self.game.is_player_1_active

        if not self.is_player_1_active:
            return

        if self.player_1_lives != self.game.player_1.lives:
            self.player_1_lives = self.game.player_1.lives
            self.player_1_lives_image = self.display_player_lives(
                self.player_1_lives,
                self.is_player_1_active
            )

        self.is_player_2_active = self.game.is_player_2_active

        if not self.is_player_2_active:
            return

        if self.player_2_lives != self.game.player_2.lives:
            self.player_2_lives = self.game.player_2.lives
            self.player_2_lives_image = self.display_player_lives(
                self.player_2_lives,
                self.is_player_2_active
            )

    def draw(self, window: pygame.Surface):
        """
        Draws the HUD elements on the screen.
        """
        window.blit(
            self.hud_overlay,
            (0, 0)
        )

        if self.is_player_1_active:
            window.blit(
                self.player_1_lives_image,
                (14.5 * gc.IMAGE_SIZE, 9.5 * gc.IMAGE_SIZE)
            )

        if self.is_player_2_active:
            window.blit(
                self.player_2_lives_image,
                (14.5 * gc.IMAGE_SIZE, 11 * gc.IMAGE_SIZE)
            )

    def generate_hud_overlay_screen(self) -> pygame.Surface:
        """
        Returns a fixed HUD overlay screen image for the game.
        """
        overlay_screen = pygame.Surface(
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        overlay_screen.fill(gc.RGB_GREY)
        pygame.draw.rect(overlay_screen, gc.RGB_BLACK, (gc.GAME_SCREEN))
        overlay_screen.blit(
            self.images['info_panel'],
            (gc.INFO_PANEL_X, gc.INFO_PANEL_Y)
        )
        overlay_screen.set_colorkey(gc.RGB_BLACK)

        return overlay_screen

    def display_player_lives(
            self,
            player_lives: int,
            is_player_active: bool
            ) -> pygame.Surface:
        """
        Shows the player lives icon and number on the screen.
        """
        width, height = gc.IMAGE_SIZE, gc.IMAGE_SIZE // 2
        surface = pygame.Surface((width, height))
        surface.fill(gc.RGB_BLACK)

        if player_lives > 99:
            player_lives = 99

        if not is_player_active:
            surface.blit(self.images['grey_square'], (0, 0))
            surface.blit(self.images['grey_square'], (gc.IMAGE_SIZE // 2, 0))

        if player_lives < 10:
            image = pygame.transform.rotate(self.images['life'], 180)
        else:
            num = str(player_lives)[0]
            image = self.images[f'num_{num}']

        surface.blit(image, (0, 0))
        num = str(player_lives)[-1]
        image_2 = self.images[f'num_{num}']
        surface.blit(image_2, (gc.IMAGE_SIZE // 2, 0))

        return surface
