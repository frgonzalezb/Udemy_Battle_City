import pygame
from pygame.surface import Surface
from pygame.rect import Rect


class ScoreBanner(pygame.sprite.Sprite):

    def __init__(
            self,
            assets,
            group,
            position: tuple[int, int],
            score: int
            ) -> None:
        super().__init__()

        self.assets = assets
        self.group = group
        self.groups['scores'].add(self)

        self.position: tuple[int, int] = position
        self.images: dict[str, Surface] = self.assets.score_images
        self.image: Surface = self.images[self.direction]
        self.rect: Rect = self.image.get_rect(center=self.position)

        self.timer: int = pygame.time.get_ticks()

    def update(self) -> None:
        if pygame.time.get_ticks() - self.timer >= 0:
            return
        return super().update()

    def draw(self, window: Surface) -> None:
        window.blit()
