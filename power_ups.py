import random

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

import game_config as gc


class PowerUp(pygame.sprite.Sprite):

    def __init__(self, game, assets, groups) -> None:
        super().__init__()

        self.game = game
        self.assets = assets
        self.groups = groups
        self.groups['power_ups'].add(self)

        self.power_up_images: dict[str, Surface] = self.assets.power_up_images

        self.power_up: str = self.select_power_up_randomly()
        self.power_up_timer: int = pygame.time.get_ticks()

        self.x_coord: int = random.randint(
            gc.SCREEN_BORDER_LEFT,
            gc.SCREEN_BORDER_RIGHT - gc.IMAGE_SIZE
        )
        self.y_coord: int = random.randint(
            gc.SCREEN_BORDER_TOP,
            gc.SCREEN_BORDER_BOTTOM - gc.IMAGE_SIZE
        )

        self.image: Surface = self.power_up_images[self.power_up]
        self.rect: Rect = self.image.get_rect(
            topleft=(self.x_coord, self.y_coord)
        )

    def update(self) -> None:
        if pygame.time.get_ticks() - self.power_up_timer >= 5_000:
            self.kill()
            # return

        player_tank = pygame.sprite.spritecollideany(
            self,
            self.groups['player_tanks']
        )
        if player_tank:
            if self.power_up == 'shield':
                self.create_shield(player_tank)
            print(self.power_up)  # dbg
            self.collect_power_up()

    def draw(self, window: Surface):
        window.blit(self.image, self.rect)

    def select_power_up_randomly(self) -> str:
        power_ups: list[str] = list(gc.POWER_UPS.keys())
        return random.choice(power_ups)

    def collect_power_up(self):
        self.kill()

    def create_shield(self, player):
        """
        In the original game, the shield is a wavy animation drawn
        around the player tank. This shield is used both as a power up
        and as a automatic short-term protection after spawning into the
        game screen (either at the stage start or after being killed by
        an enemy tank). The protection time is longer on the power up,
        of course.
        """
        player.has_shield_at_start = True
