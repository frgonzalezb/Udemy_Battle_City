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

        # self.power_up: str = self.select_power_up_randomly()
        self.power_up: str = 'extra_life'
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
            elif self.power_up == 'freeze':
                self.freeze_tanks()
            elif self.power_up == 'explosion':
                self.destroy_tanks(player_tank)
            elif self.power_up == 'extra_life':
                self.get_extra_life(player_tank)
            elif self.power_up == 'power':
                self.get_power(player_tank)
            print(self.power_up)  # dbg
            self.collect_power_up()

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)

    def select_power_up_randomly(self) -> str:
        power_ups: list[str] = list(gc.POWER_UPS.keys())
        return random.choice(power_ups)

    def collect_power_up(self) -> None:
        self.kill()

    def create_shield(self, player) -> None:
        """
        Creates a shield around the player tank.

        In the original game, the shield is a wavy animation drawn
        around the player tank. This shield is used both as a power up
        and as a automatic short-term protection after spawning into the
        game screen (either at the stage start or after being killed by
        an enemy tank). The protection time is longer on the power up,
        of course.
        """
        player.has_shield_at_start = True

    def freeze_tanks(self) -> None:
        """
        Freezes all of the currently spawned enemy tanks for a short
        amount of time.
        """
        for tank in self.groups['all_tanks']:
            if tank.is_enemy:
                tank.paralyze_tank(5_000)

    def destroy_tanks(self, player) -> None:
        """
        Destroys all of the currently spawned enemy tanks.

        NOTE: Player argument is needed here because, when the enemy
        tanks are destroyed by the power up, there's a score attached
        to it, which must be assigned correctly to either player 1 or
        player 2.
        """
        for tank in self.groups['all_tanks']:
            if tank.is_enemy:
                score = tank.score
                player.scores.append(score)
                tank.destroy_tank()

    def get_extra_life(self, player) -> None:
        """
        Gives the player an extra life.
        """
        player.lives += 1

    def get_power(self, player):
        """
        Increases the bullet speed, and when speed reaches 1.5,
        increases the bullet limit by 1.
        """
        player.bullet_speed_modifier += 0.1
        if player.bullet_speed_modifier > 1.5:
            player.bullet_speed_modifier = 1
            player.bullet_limit += 1
        player.bullet_speed = (
            gc.TANK_SPEED * (3 * player.bullet_speed_modifier)
        )
