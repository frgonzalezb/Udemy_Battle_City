import pygame
from pygame.surface import Surface
from pygame.rect import Rect


class Explosion(pygame.sprite.Sprite):

    def __init__(
            self,
            assets,
            groups,
            position: tuple[int, int],
            explode_type: int = 1
            ) -> None:
        super().__init__()

        self.assets = assets
        self.groups = groups
        self.explosion_group = self.groups['explosion']
        self.explosion_group.add(self)

        self.explode_type: int = explode_type

        self.position: tuple[int, int] = position
        self.frame_index: int = 1
        self.images: dict[str, Surface] = self.assets.explosions_images
        self.image: Surface = self.images['explode_1']
        self.rect: Rect = self.image.get_rect(center=self.position)

        self.animation_timer: int = pygame.time.get_ticks()

    def update(self) -> None:
        if pygame.time.get_ticks() - self.animation_timer >= 100:
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            # Differentiating between a small and a large explosion
            if self.explode_type == 1 and self.frame_index > 3:
                self.kill()
            self.animation_timer = pygame.time.get_ticks()
            self.image: Surface = self.images[f'explode_{self.frame_index}']
            self.rect: Rect = self.image.get_rect(center=self.position)

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)
