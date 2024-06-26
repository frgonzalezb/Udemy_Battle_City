import pygame
from pygame.surface import Surface

import game_config as gc


class GameHUD:
    """
    Blueprint for the game HUD object.
    """

    def __init__(self, game, assets) -> None:
        self.game = game
        self.assets = assets
        self.images = self.assets.hud_images
        self.hud_overlay = self.generate_hud_overlay_screen()

        # Player 1 lives and display
        self.is_player_1_active: bool = False
        self.player_1_lives: int = 0
        self.player_1_lives_image: pygame.Surface = self.display_player_lives(
            self.player_1_lives, self.is_player_1_active
        )

        # Player 2 lives and display
        self.is_player_2_active: bool = False
        self.player_2_lives: int = 0
        self.player_2_lives_image: pygame.Surface = self.display_player_lives(
            self.player_2_lives, self.is_player_2_active
        )

        # Level information
        self.level = 1
        self.level_image = self.display_stage_number(self.level)
        self.level_image_rect = self.level_image.get_rect(
            topleft=(14.5 * gc.IMAGE_SIZE, 13 * gc.IMAGE_SIZE)
        )

    def update(self) -> None:
        # Update the number of enemies still remaining to spawn
        self.enemies = self.game.enemies

        # Update the number of player lives available
        self.is_player_1_active = self.game.is_player_1_active
        if (
            self.is_player_1_active and
            self.player_1_lives != self.game.player_1.lives
        ):
            self.player_1_lives = self.game.player_1.lives
            self.player_1_lives_image = self.display_player_lives(
                self.player_1_lives,
                self.is_player_1_active
            )

        self.is_player_2_active = self.game.is_player_2_active
        if (
            self.is_player_2_active and
            self.player_2_lives != self.game.player_2.lives
        ):
            self.player_2_lives = self.game.player_2.lives
            self.player_2_lives_image = self.display_player_lives(
                self.player_2_lives,
                self.is_player_2_active
            )

        # Update the stage number image
        if self.level != self.game.level_num:
            self.level = self.game.level_num
            self.level_image = self.display_stage_number(self.level)

    def draw(self, window: Surface) -> None:
        """
        Draws the HUD elements on the screen.
        """
        window.blit(
            self.hud_overlay,
            (0, 0)
        )

        self.draw_enemy_tanks_remaining(window)

        window.blit(
            self.player_1_lives_image,
            (14.5 * gc.IMAGE_SIZE, 9.5 * gc.IMAGE_SIZE)
        )

        window.blit(
            self.player_2_lives_image,
            (14.5 * gc.IMAGE_SIZE, 11 * gc.IMAGE_SIZE)
        )

        window.blit(
            self.level_image,
            self.level_image_rect
        )

    def draw_enemy_tanks_remaining(self, window: Surface) -> None:
        """
        Draws the little tank images on the HUD screen to represent the
        number of enemies still remaining to spawn in the game area.
        """
        row = 0
        offset_x_1, offset_x_2 = (14.5 * gc.IMAGE_SIZE), (15 * gc.IMAGE_SIZE)

        for num in range(gc.STD_ENEMIES):

            if num % 2 == 0:
                x, y = offset_x_1, (4 + row) * (gc.IMAGE_SIZE // 2)
            else:
                x, y = offset_x_2, (4 + row) * (gc.IMAGE_SIZE // 2)
                row += 1

            if num < self.enemies:
                window.blit(self.images['life'], (x, y))
            else:
                window.blit(self.images['grey_square'], (x, y))

    def generate_hud_overlay_screen(self) -> Surface:
        """
        Returns a fixed HUD overlay screen image for the game.
        """
        overlay_screen = Surface(
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        overlay_screen.fill(gc.RGB_GREY)
        game_screen_tuple = tuple(value for value in gc.GAME_SCREEN.values())

        pygame.draw.rect(
            overlay_screen,
            gc.RGB_BLACK,
            game_screen_tuple
        )

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
            ) -> Surface:
        """
        Shows the player lives icon and number on the screen.
        """
        width, height = gc.IMAGE_SIZE, gc.IMAGE_SIZE // 2
        surface = Surface((width, height))
        surface.fill(gc.RGB_BLACK)

        if player_lives > 99:
            player_lives = 99

        if not is_player_active:
            surface.blit(self.images['grey_square'], (0, 0))
            surface.blit(self.images['grey_square'], (gc.IMAGE_SIZE // 2, 0))
            return surface

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

    def display_stage_number(self, level: int) -> Surface:
        """
        Generates the stage level image, according to the level number
        passed in.
        """
        width, height = gc.IMAGE_SIZE, gc.IMAGE_SIZE // 2
        surface = Surface((width, height))
        surface.fill(gc.RGB_BLACK)

        if level < 10:
            image_1 = self.images['num_0']
        else:
            num = str(level)[0]
            image_1 = self.images[f'num_{num}']

        surface.blit(image_1, (0, 0))
        num = str(level)[-1]
        image_2 = self.images[f'num_{num}']
        surface.blit(image_2, (gc.IMAGE_SIZE // 2, 0))

        return surface
