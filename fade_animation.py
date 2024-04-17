import pygame
from pygame import Surface, Rect

import game_config as gc


class Fade:

    def __init__(self, game, assets, speed: int = 5) -> None:
        self.game = game
        self.assets = assets

        self.level: int = self.game.level_num - 1
        self.images: dict[str, Surface] = self.assets.hud_images
        self.speed: int = speed

        self.is_fade_active: bool = False
        self.is_fade_in: bool = True

        self.top_rect: Rect = Rect(
            0,
            0 - gc.SCREEN_HEIGHT // 2,
            gc.SCREEN_WIDTH,
            gc.SCREEN_HEIGHT // 2
        )
        self.top_rect_start_y: int = 0 - gc.SCREEN_HEIGHT // 2
        self.top_rect_end_y: int = gc.SCREEN_HEIGHT // 2
        self.top_y: int = self.top_rect.bottom

        self.bottom_rect: Rect = Rect(
            0,
            gc.SCREEN_HEIGHT,
            gc.SCREEN_WIDTH,
            gc.SCREEN_HEIGHT // 2
        )
        self.bottom_rect_start_y: int = self.bottom_rect.top
        self.bottom_rect_end_y: int = gc.SCREEN_HEIGHT // 2
        self.bottom_y: int = self.bottom_rect.top

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

    def draw(self, window: Surface) -> None:
        pygame.draw.rect(window, gc.RGB_GREY, self.top_rect)
        pygame.draw.rect(window, gc.RGB_GREY, self.bottom_rect)

    def make_y_coord_fade(self, y_coord, start_pos, end_pos, speed: int):
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
