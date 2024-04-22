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
        self.timer: int = pygame.time.get_ticks()
        self.score_timer: int = 100  # milliseconds

        self.images: dict[str, Surface] = self.assets.scoresheet_images

        self.y_coords_for_values: list[float] = [12.5, 15.0, 17.5, 20.0]
        self.score_size: int = gc.IMAGE_SIZE // 2

        # Player score totals and score list
        self.player_1_score: int = 0
        self.player_1_enemies_killed: list = []
        self.player_2_score: int = 0
        self.player_2_enemies_killed: list = []

        self.top_score: int = 0
        self.stage: int = 0

        self.scoresheet = self.generate_scoresheet_screen()
        self._create_top_score_images()
        self._create_stage_number_images()
        self.update_player_score_images()

        # line_n: list[number of tanks, tank score number]
        self.player_1_score_values: dict[str, list[int, int] | int] = {
            'line_1': [0, 0],
            'line_2': [0, 0],
            'line_3': [0, 0],
            'line_4': [0, 0],
            'total': 0
        }
        self.player_2_score_values: dict[str, list[int, int] | int] = {
            'line_1': [0, 0],
            'line_2': [0, 0],
            'line_3': [0, 0],
            'line_4': [0, 0],
            'total': 0
        }

        self.player_1_tank_num_images, self.player_1_tank_score_images = (
            self.generate_tank_kill_images(14, 7, self.player_1_score_values)
        )
        self.player_2_tank_num_images, self.player_2_tank_score_images = (
            self.generate_tank_kill_images(20, 25, self.player_2_score_values)
        )

    def update(self) -> None:
        if not pygame.time.get_ticks() - self.timer >= 2_000:
            return

        # Player 1
        if (
            len(self.player_1_enemies_killed) > 0 and
            pygame.time.get_ticks() - self.timer >= 100
        ):
            score = self.player_1_enemies_killed.pop(0)
            self.update_score(score, 'player_1')
            self.score_timer = pygame.time.get_ticks()
            return

        # Player 2
        if (
            len(self.player_2_enemies_killed) > 0 and
            pygame.time.get_ticks() - self.timer >= 100
        ):
            score = self.player_2_enemies_killed.pop(0)
            self.update_score(score, 'player_2')
            self.score_timer = pygame.time.get_ticks()
            return

        if pygame.time.get_ticks() - self.timer >= 4_000:
            self.is_active = False
            self.game.change_level(self.player_1_score, self.player_2_score)
            self.clear_score_for_new_stage()

    def update_score(self, score: int, player: str):
        score_dict: dict[int, str] = {
            100: 'line_1',
            200: 'line_2',
            300: 'line_3',
            400: 'line_4',
        }
        if player == 'player_1':
            self.player_1_score_values[score_dict[score]][0] += 1
            self.player_1_score_values[score_dict[score]][1] += score
            self.player_1_score_values['total'] += 1
            self.player_1_score += score
            # FIXME: This may be refactored, 'cause of no DRY!
            self.player_1_tank_num_images, self.player_1_tank_score_images = (
                self.generate_tank_kill_images(
                    14,
                    7,
                    self.player_1_score_values
                )
            )
        else:
            self.player_2_score_values[score_dict[score]][0] += 1
            self.player_2_score_values[score_dict[score]][1] += score
            self.player_2_score_values['total'] += 1
            self.player_2_score += score
            # FIXME: This may be refactored, 'cause of no DRY!
            self.player_2_tank_num_images, self.player_2_tank_score_images = (
                self.generate_tank_kill_images(
                    20,
                    25,
                    self.player_2_score_values
                )
            )
        self.update_player_score_images()

    def draw(self, window: Surface) -> None:
        window.fill(gc.RGB_BLACK)
        window.blit(self.scoresheet, (0, 0))
        window.blit(self.hi_score_nums_total, self.hi_score_nums_rect)
        window.blit(self.stage_num, self.stage_num_rect)

        if self.game.is_player_1_active:
            window.blit(self.player_1_score_img, self.player_1_score_rect)
            for value in self.player_1_tank_num_images.values():
                window.blit(value[0], value[1])
            for value in self.player_1_tank_score_images.values():
                window.blit(value[0], value[1])

        if self.game.is_player_2_active:
            window.blit(self.player_2_score_img, self.player_2_score_rect)
            for value in self.player_2_tank_num_images.values():
                window.blit(value[0], value[1])
            for value in self.player_2_tank_score_images.values():
                window.blit(value[0], value[1])

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
        if self.game.is_player_1_active:
            surface.blit(
                self.images['player_1'],
                (self.score_size * 3, self.score_size * 8)
            )
        if self.game.is_player_2_active:
            surface.blit(
                self.images['player_2'],
                (self.score_size * 21, self.score_size * 8)
            )

        # Labels related to the actual scores for each player
        for num, pos_y in enumerate(self.y_coords_for_values):
            if self.game.is_player_1_active:
                surface.blit(
                    self.images['pts'],
                    (self.score_size * 8, self.score_size * pos_y)
                )
                surface.blit(
                    arrow_left,
                    (self.score_size * 14, self.score_size * pos_y)
                )
            if self.game.is_player_2_active:
                surface.blit(
                    self.images['pts'],
                    (self.score_size * 26, self.score_size * pos_y)
                )
                surface.blit(
                    arrow_right,
                    (self.score_size * 17, self.score_size * pos_y)
                )
            # The following for all players
            surface.blit(
                self.assets.tank_images[f'Tank_{num + 4}']['Silver']['Up'][0],
                (self.score_size * 15, self.score_size * (pos_y - 0.5))
            )

        # The "total" label
        surface.blit(
            self.images['total'],
            (self.score_size * 6, self.score_size * 22)
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
            (self.score_size * length, self.score_size)
        )
        for index, number in enumerate(num):
            score_surface.blit(
                number_color[int(number)],
                (self.score_size * index, 0)
            )
        return score_surface

    def update_player_score_images(self) -> None:
        # Player 1
        self.player_1_score_img = self.generate_number_image(
            self.player_1_score, self.orange_nums
        )
        self.player_1_score_rect = self.player_1_score_img.get_rect(
            topleft=(
                self.score_size * 11 - self.player_1_score_img.get_width(),
                self.score_size * 10
            )
        )
        # Player 2
        self.player_2_score_img = self.generate_number_image(
            self.player_2_score, self.orange_nums
        )
        self.player_2_score_rect = self.player_2_score_img.get_rect(
            topleft=(
                self.score_size * 29 - self.player_2_score_img.get_width(),
                self.score_size * 10
            )
        )

    def _create_top_score_images(self) -> None:
        self.hi_score_nums_total = self.generate_number_image(
            self.top_score, self.orange_nums
        )
        self.hi_score_nums_rect = self.hi_score_nums_total.get_rect(
            topleft=(self.score_size * 19, self.score_size * 4)
        )

    def _create_stage_number_images(self) -> None:
        self.stage_num = self.generate_number_image(
            self.stage, self.white_nums
        )
        self.stage_num_rect = self.stage_num.get_rect(
            topleft=(self.score_size * 19, self.score_size * 6)
        )

    def update_basic_info(self, top_score, stage_number):
        self.top_score = top_score
        self.stage = stage_number
        self._create_top_score_images()
        self._create_stage_number_images()

    def generate_tank_kill_images(
            self,
            x1_coord: int,
            x2_coord: int,
            player_score_values: dict[str, list[int, int] | int]
            ) -> tuple[dict[str, list], dict[str, list]]:
        """
        Generates a tuple with dictionaries of images and X/Y coords
        for score values.
        """
        tank_num_images: dict = self._generate_tank_numbers(
            self.score_size,
            x1_coord,
            player_score_values
        )
        tank_score_images: dict = self._generate_tank_score_per_line(
            self.score_size,
            x2_coord,
            player_score_values
        )
        return tank_num_images, tank_score_images

    def _generate_tank_numbers(
            self,
            size: int,
            x1_coord: int,
            player_score_values: dict[str, list[int, int] | int]
            ) -> dict[str, list[Surface | tuple[int, float]]]:
        """
        Utility method for cleaning up the original
        generate_tank_kill_images() method.

        Ths generates the number image of the tank numbers.
        """
        tank_num_images: dict = {}
        for i in range(4):
            key = f'line_{i + 1}'
            tank_num_images[key] = []
            tank_num_images[key].append(
                self.generate_number_image(
                    player_score_values[key][0],
                    self.white_nums
                )
            )
            tank_num_images[key].append(
                (
                    size * x1_coord - tank_num_images[key][0].get_width(),
                    size * self.y_coords_for_values[i]
                )
            )
        tank_num_images['total'] = []
        tank_num_images['total'].append(
            self.generate_number_image(
                player_score_values['total'],
                self.white_nums
            )
        )
        tank_num_images['total'].append(
            (
                size * x1_coord - tank_num_images['total'][0].get_width(),
                size * 22.5
            )
        )
        return tank_num_images

    def _generate_tank_score_per_line(
            self,
            size: int,
            x2_coord: int,
            player_score_values: dict[str, list[int, int] | int]
            ) -> dict[str, list[Surface | tuple[int, float]]]:
        """
        Utility method for cleaning up the original and quite long
        generate_tank_kill_images() method.

        This generates images for tank score per line.
        """
        tank_score_images: dict = {}
        for i in range(4):
            key = f'line_{i + 1}'
            tank_score_images[key] = []
            tank_score_images[key].append(
                self.generate_number_image(
                    player_score_values[key][0],
                    self.white_nums
                )
            )
            tank_score_images[key].append(
                (
                    size * x2_coord - tank_score_images[key][0].get_width(),
                    size * self.y_coords_for_values[i]
                )
            )
        return tank_score_images

    def clear_score_for_new_stage(self):
        # FIXME: No DRY!
        self.player_1_enemies_killed = []
        self.player_2_enemies_killed = []
        self.player_1_score_values: dict[str, list[int, int] | int] = {
            'line_1': [0, 0],
            'line_2': [0, 0],
            'line_3': [0, 0],
            'line_4': [0, 0],
            'total': 0
        }
        self.player_2_score_values: dict[str, list[int, int] | int] = {
            'line_1': [0, 0],
            'line_2': [0, 0],
            'line_3': [0, 0],
            'line_4': [0, 0],
            'total': 0
        }
        self.player_1_tank_num_images, self.player_1_tank_score_images = (
            self.generate_tank_kill_images(14, 7, self.player_1_score_values)
        )
        self.player_2_tank_num_images, self.player_2_tank_score_images = (
            self.generate_tank_kill_images(20, 25, self.player_2_score_values)
        )
