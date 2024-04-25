"""
Phoenix, a.k.a. the eagle icon inside the base!
"""


import pygame
from pygame.surface import Surface

import game_config as gc
from explosions import Explosion


class Phoenix(pygame.sprite.Sprite):

    def __init__(self, game, assets, groups) -> None:
        super().__init__()

        self.game = game
        self.assets = assets
        self.group = groups
        self.group['phoenix'].add(self)

    def update(self) -> None:
        return super().update()

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)
