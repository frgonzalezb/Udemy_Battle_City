import random

import pygame
from pygame.surface import Surface

import game_assets as gc


class PowerUp(pygame.sprite.Sprite):

    def __init__(self, game, assets, groups) -> None:
        super().__init__()

        self.game = game
        self.assets = assets
        self.groups = groups
        self.groups['power_ups'].add(self)

        self.power_up_images: dict[str, Surface] = self.assets.power_up_images
