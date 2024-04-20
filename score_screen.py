import pygame
from pygame import Surface

import game_config as gc


class ScoreScreen:

    def __init__(self, game, assets) -> None:
        self.game = game
        self.assets = assets
        self.white_nums: dict[str, Surface] = self.assets.numbers_black_white
        self.orange_nums: dict[str, Surface] = self.assets.numbers_black_orange

        self.is_active = False
        self.timer = pygame.time.get_ticks()

        self.images: dict[str, Surface] = self.assets.scoresheet_images

        # Player score totals and score list
        self.player_1_score = 3000
        self.player_1_kill_list = []
        self.player_2_score = 2500
        self.player_2_kill_list = []

        self.scoresheet = self.generate_scoresheet_screen()
        self.update_player_score_images()

    def update(self) -> None:
        if not pygame.time.get_ticks() - self.timer >= 10000:
            return
        self.is_active = False
        self.game.change_level(self.player_1_score, self.player_2_score)

    def draw(self, window: Surface) -> None:
        window.fill(gc.RGB_BLACK)
        window.blit(self.scoresheet, (0, 0))

        if self.game.is_player_1_active:
            window.blit(self.player_1_score_img, self.player_1_score_rect)
        if self.game.is_player_2_active:
            window.blit(self.player_2_score_img, self.player_2_score_rect)

    def generate_scoresheet_screen(self) -> Surface:
        """
        Generates a basic template screen for the score card transition
        screen.
        """
        surface = Surface(
            (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        )
        surface.fill(gc.RGB_BLACK)

        arrow_left = self.images['arrow']
        arrow_right = pygame.transform.flip(arrow_left, True, False)

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

        # The "player" labels
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

        # Labels related to the actual scores for each player
        for num, pos_y in enumerate([12.5, 15.0, 17.5, 20.0]):
            if self.game.is_player_1_active:
                surface.blit(
                    self.images['pts'],
                    (new_base_size * 8, new_base_size * pos_y)
                )
                surface.blit(
                    arrow_left,
                    (new_base_size * 14, new_base_size * pos_y)
                )
            if self.game.is_player_2_active:
                surface.blit(
                    self.images['pts'],
                    (new_base_size * 26, new_base_size * pos_y)
                )
                surface.blit(
                    arrow_right,
                    (new_base_size * 17, new_base_size * pos_y)
                )
            # The following for all players
            surface.blit(
                self.assets.tank_images[f'Tank_{num + 4}']['Silver']['Up'][0],
                (new_base_size * 15, new_base_size * (pos_y - 0.5))
            )

        # The "total" label
        surface.blit(
            self.images['total'],
            (new_base_size * 6, new_base_size * 22)
        )

        return surface

    def generate_number_image(
            self,
            score: int,
            number_color: dict[str, Surface]
            ) -> Surface:
        """
        Converts a number into an image.
        """
        num = str(score)
        length = len(num)
        score_surface = Surface(
            (gc.IMAGE_SIZE // 2 * length, gc.IMAGE_SIZE // 2)
        )
        for index, number in enumerate(num):
            score_surface.blit(
                number_color[int(number)],
                (gc.IMAGE_SIZE // 2 * index, 0)
            )
        return score_surface

    def update_player_score_images(self) -> None:
        # Player 1
        self.player_1_score_img = self.generate_number_image(
            self.player_1_score, self.orange_nums
        )
        self.player_1_score_rect = self.player_1_score_img.get_rect(
            topleft=(
                gc.IMAGE_SIZE // 2 * 11 - self.player_1_score_img.get_width(),
                gc.IMAGE_SIZE // 2 * 10
            )
        )
        # Player 2
        self.player_2_score_img = self.generate_number_image(
            self.player_2_score, self.orange_nums
        )
        self.player_2_score_rect = self.player_2_score_img.get_rect(
            topleft=(
                gc.IMAGE_SIZE // 2 * 29 - self.player_2_score_img.get_width(),
                gc.IMAGE_SIZE // 2 * 10
            )
        )
