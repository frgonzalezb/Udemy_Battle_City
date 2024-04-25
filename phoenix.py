"""
Phoenix, a.k.a. the eagle icon inside the base!
"""


import pygame
from pygame.surface import Surface
from pygame.rect import Rect

import game_config as gc
from explosions import Explosion


class Phoenix(pygame.sprite.Sprite):

    def __init__(self, game, assets, groups) -> None:
        super().__init__()

        self.game = game
        self.assets = assets
        self.group = groups
        self.group['phoenix'].add(self)

        self.is_active: bool = True
        self.timer: int = pygame.time.get_ticks()

        self.images: dict[str, Surface] = self.assets.flag_images
        self.image: Surface = self.images['Phoenix_Alive']
        self.rect: Rect = self.image.get_rect(topleft=gc.PHOENIX_POSITION)

    def update(self) -> None:
        if not self.is_active and pygame.time.get_ticks() - self.timer >= 750:
            self._declare_game_over()

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)

    def _declare_game_over(self):
        """
        Utility method for cleaning the update() one, to give a easily-
        readable idea.
        """
        if self.game.is_player_1_active:
            self.game.player_1.is_game_over = True
        if self.game.is_player_2_active:
            self.game.player_2.is_game_over = True

    def destroy_phoenix(self):
        """
        Destroys the player base.
        """
        self.is_active = False
        Explosion(self.assets, self.group, self.rect.center, 5, 0)
        self.image: Surface = self.images['Phoenix_Destroyed']
        self.timer: int = pygame.time.get_ticks()
