import pygame
from pygame.surface import Surface
from pygame.rect import Rect

import game_config as gc


class GameOver:

    def __init__(self, game, assets) -> None:
        self.game = game
        self.assets = assets

        self.image: Surface = self.assets.context_images['game_over']
        self.width, self.height = self.image.get_size()
        self.rect_center: tuple[int, int] = (
                gc.SCREEN_WIDTH // 2 - self.width // 2,
                gc.SCREEN_HEIGHT // 2 + self.height // 2,
            )
        self.rect: Rect = self.image.get_rect(center=self.rect_center)

        self.timer: int = pygame.time.get_ticks()
        self.is_active: bool = False

    def activate(self):
        self.is_active = True
        self.timer = pygame.time.get_ticks()

    def update(self) -> None:
        """
        Defines the animation behavior for the Game Over screen.
        """
        game_over_position: int = gc.SCREEN_HEIGHT // 4 - self.height // 2

        if self.rect.y > game_over_position:
            # Move image upwards
            self.rect.y -= 10
        elif self.rect.y < game_over_position:
            # Stop image in the desired position (screen center)
            self.rect.y = game_over_position
            self.timer = pygame.time.get_ticks()

        if (
            self.rect.y == game_over_position and
            pygame.time.get_ticks() - self.timer >= 3_000
        ):
            self.is_active = False
            self.game.create_stage_transition(True)

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)
