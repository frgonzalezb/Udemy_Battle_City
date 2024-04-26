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
        self.position: tuple[int, int] = (
                gc.SCREEN_WIDTH // 2 - self.width // 2,
                gc.SCREEN_HEIGHT // 2 + self.height // 2,
            )
        self.rect: Rect = self.image.get_rect(center=self.position)

        self.timer: int = pygame.time.get_ticks()
        self.is_active: bool = False

    def activate(self):
        self.is_active = True
        self.timer: int = pygame.time.get_ticks()

    def update(self) -> None:
        ...

    def draw(self, window: Surface) -> None:
        ...
