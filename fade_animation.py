import pygame
from pygame import Surface

import game_config as gc


class Fade:

    def __init__(self, game, assets, speed: int = 5) -> None:
        self.game = game
        self.assets = assets

        self.level = self.game.level_num - 1
        self.images = self.assets.hud_images
        self.speed = speed

        self.is_fade_active = False
        self.is_fade_in = True
        self.is_fade_out = False
        self.transition = False
        self.timer = pygame.time.get_ticks()

        self.top_rect = pygame.Rect(
            0,
            0 - gc.SCREEN_HEIGHT // 2,
            gc.SCREEN_WIDTH,
            gc.SCREEN_HEIGHT // 2
        )
        self.top_rect_start_y = 0 - gc.SCREEN_HEIGHT // 2
        self.top_rect_end_y = gc.SCREEN_HEIGHT // 2
        self.top_y = self.top_rect.bottom

        self.bottom_rect = pygame.Rect(
            0,
            gc.SCREEN_HEIGHT,
            gc.SCREEN_WIDTH,
            gc.SCREEN_HEIGHT // 2
        )
        self.bottom_rect_start_y = self.bottom_rect.top
        self.bottom_rect_end_y = gc.SCREEN_HEIGHT // 2
        self.bottom_y = self.bottom_rect.top

        self.stage_pic_width, self.stage_pic_height = (
            self.images['stage'].get_size()
        )
        self.num_pic_width, self.num_pic_height = (
            self.images['num_0'].get_size()
        )

        self.stage_image = self.create_stage_image()
        self.stage_image_rect = self.stage_image.get_rect(
            center=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2)
        )

    def update(self) -> None:
        if not self.is_fade_active:
            return

        if self.is_fade_in:
            self.top_y = self.make_y_coord_fade(
                self.top_y,
                self.top_rect_start_y,
                self.top_rect_end_y,
                self.speed
            )
            self.top_rect.bottom = self.top_y
            self.bottom_y = self.make_y_coord_fade(
                self.bottom_y,
                self.bottom_rect_start_y,
                self.bottom_rect_end_y,
                self.speed
            )
            self.bottom_rect.top = self.bottom_y

            if (
                self.top_rect.bottom == self.top_rect_end_y and
                self.bottom_rect.top == self.bottom_rect_end_y
            ):
                self.is_fade_in = False
                self.is_fade_out = False
                self.transition = True
                self.timer = pygame.time.get_ticks()

        elif self.transition:
            if pygame.time.get_ticks() - self.timer >= 1000:
                self.is_fade_in = False
                self.is_fade_out = True
                self.transition = False

        elif self.is_fade_out:
            self.top_y = self.make_y_coord_fade(
                self.top_y,
                self.top_rect_end_y,
                self.top_rect_start_y,
                self.speed
            )
            self.top_rect.bottom = self.top_y
            self.bottom_y = self.make_y_coord_fade(
                self.bottom_y,
                self.bottom_rect_end_y,
                self.bottom_rect_start_y,
                self.speed
            )
            self.bottom_rect.top = self.bottom_y

            if (
                self.top_rect.bottom == self.top_rect_start_y and
                self.bottom_rect.top == self.bottom_rect_start_y
            ):
                self.is_fade_in = True
                self.is_fade_out = False
                self.transition = False
                self.is_fade_active = False
                self.game.is_game_on = True

    def draw(self, window: Surface) -> None:
        pygame.draw.rect(window, gc.RGB_GREY, self.top_rect)
        pygame.draw.rect(window, gc.RGB_GREY, self.bottom_rect)
        if self.transition:
            window.blit(self.stage_image, self.stage_image_rect)

    def make_y_coord_fade(
            self,
            y_coord: int,
            start_pos: int,
            end_pos: int,
            speed: int
            ) -> int:
        """
        Accepts the Y-coordinate of the fade rectangles, and updates
        their positions to the end position.
        """
        # Check to see if fade is in upward motion
        if start_pos > end_pos:
            y_coord -= speed
            if y_coord < end_pos:
                y_coord = end_pos
        # Check to see if fade is in downward motion
        elif start_pos < end_pos:
            y_coord += speed
            if y_coord > end_pos:
                y_coord = end_pos
        return y_coord

    def create_stage_image(self) -> Surface:
        """
        Generates a stage number to display during the transition phase.
        """
        surface = pygame.Surface(
            (
                self.stage_pic_width + (self.num_pic_width * 3),
                self.stage_pic_height
            )
        )
        surface.fill(gc.RGB_GREY)
        surface.blit(self.images['stage'], (0, 0))
        # Adding one digit if stage number < 10
        if self.level < 10:
            surface.blit(
                self.images['num_0'],
                (self.stage_pic_width + self.num_pic_width, 0)
            )
        else:
            surface.blit(
                self.images[f'num_{str(self.level)[0]}'],
                (self.stage_pic_width + self.num_pic_width, 0)
            )
        surface.blit(
            self.images[f'num_{str(self.level)[-1]}'],
            (self.stage_pic_width + (self.num_pic_width * 2), 0)
        )

        return surface
