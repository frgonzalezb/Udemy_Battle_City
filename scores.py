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
        self.group['scores'].add(self)

        self.position: tuple[int, int] = position
        self.score: str = str(score)

        self.images: dict[str, Surface] = self.assets.score_images
        self.image: Surface = self.images[self.score]
        self.rect: Rect = self.image.get_rect(center=self.position)

        self.timer: int = pygame.time.get_ticks()

    def update(self) -> None:
        self.rect.y -= 1
        if pygame.time.get_ticks() - self.timer >= 1_000:
            self.kill()
        return super().update()

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)
