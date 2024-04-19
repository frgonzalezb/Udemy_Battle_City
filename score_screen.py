import pygame
from pygame import Surface

import game_config as gc


class ScoreScreen:

    def __init__(self, game, assets) -> None:
        self.game = game
        self.assets = assets
        self.white_nums = self.assets.numbers_black_white
        self.orange_nums = self.assets.numbers_black_orange

        self.is_active = False
        self.timer = pygame.time.get_ticks()

        self.images: dict[str, Surface] = self.assets.scoresheet_images
        self.scoresheet = self.generate_scoresheet_screen()

    def update(self) -> None:
        if not pygame.time.get_ticks() - self.timer >= 10000:
            return
        self.is_active = False
        self.game.change_level()

    def draw(self, window: Surface) -> None:
        window.fill(gc.RGB_BLACK)
        window.blit(self.scoresheet, (0, 0))

    def generate_scoresheet_screen(self) -> Surface:
        """
        Generates a basic template screen for the score card transition
        screen.
        """
        surface = pygame.Surface(
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        surface.fill(gc.RGB_BLACK)

        # The "hi-score" label
        surface.blit(
            self.images['hi-score'],
            (gc.IMAGE_SIZE * 4, gc.IMAGE_SIZE * 2)
        )
        # The "stage" label
        surface.blit(
            self.images['stage'],
            (gc.IMAGE_SIZE * 6, gc.IMAGE_SIZE * 3)
        )

        # The player tanks
        new_base_size = gc.IMAGE_SIZE // 2
        if self.game.is_player_1_active:
            surface.blit(
                self.images['player_1'],
                (new_base_size * 3, new_base_size * 8)
            )
        if self.game.is_player_2_active:
            surface.blit(
                self.images['player_2'],
                (new_base_size * 21, new_base_size * 8)
            )

        # The "points" label
        surface.blit(
            self.images['pts'],
            (new_base_size * 8, new_base_size * 12.5)
        )

        # Arrows
        arrow_left = self.images['arrow']
        arrow_right = pygame.transform.flip(arrow_left, True, False)
        surface.blit(
            arrow_left,
            (new_base_size * 14, new_base_size * 12.5)
        )

        # Enemy tanks
        surface.blit(
            self.assets.tank_images['Tank_4']['Silver']['Up'][0],
            (new_base_size * 15, new_base_size * 12.5)
        )

        # The "total" label
        surface.blit(
            self.images['total'],
            (new_base_size * 6, new_base_size * 22)
        )

        return surface
