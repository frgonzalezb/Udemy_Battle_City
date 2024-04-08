import pygame
import game_config as gc


class Bullet(pygame.sprite.Sprite):

    def __init__(
            self,
            assets,
            groups,
            owner,
            position,
            direction
            ) -> None:

        super().__init__()

        self.assets = assets
        self.group = groups

        # Groups for collision detection
        self.tanks = self.group['All_Tanks']
        self.bullet_group = self.group['Bullets']

        # Bullet position and direction
        self.pos_x, self.pos_y = position
        self.direction = direction

        # Bullet attributes
        self.owner = owner

        # Bullet images
        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        # Add bullet to bullets group
        self.bullet_group.add(self)

    def update(self) -> None:
        pass

    def draw(self, window) -> None:
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.RGB_GREEN, self.rect, 1)
