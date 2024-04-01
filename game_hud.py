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

    def update(self):
        pass

    def draw(self, window):
        window.blit(
            self.hud_overlay,
            (0, 0)
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
