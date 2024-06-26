import random

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

import game_config as gc
from scores import ScoreBanner


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
            self._assign_score_to_player_tank(player_tank)

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
            elif self.power_up == 'special':
                self.get_special_power_up(player_tank)
            elif self.power_up == 'fortify':
                self.fortify_base()
            self.collect_power_up()

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)

    def _assign_score_to_player_tank(self, player_tank) -> None:
        """
        Utility method for cleaning the scoring functionality to player
        tanks when a power up is catched.
        """
        if player_tank.color == 'Gold':
            self.game.player_1_score += 500
        elif player_tank.color == 'Green':
            self.game.player_2_score += 500

    def select_power_up_randomly(self) -> str:
        power_ups: list[str] = list(gc.POWER_UPS.keys())
        return random.choice(power_ups)

    def collect_power_up(self) -> None:
        ScoreBanner(self.assets, self.groups, self.rect.center, '500')
        self.assets.bonus_sound_channel.play(
            self.assets.bonus_sound
        )
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

    def get_special_power_up(self, player):
        """
        Upgrades player tank level. Level 0 is the standard for the
        player tank without special power up. The following levels:

        Level 1: Shot power increased to 2, player tank can destroy a
        block of brick in one shot!
        Level 2: Shot power increased to 3, player tank can destroy a
        block of steel in one shot!
        Level 3: Player tank health increased by 1.
        Level 4: Player tank becomes amphibious.
        """
        if player.power >= 4:
            player.is_amphibious = True
            return

        player.power += 1
        player.tank_level += 1
        if player.tank_level >= 3:
            player.tank_level = 3
            player.tank_health += 1
        player.image = (
            player.tank_images[f'Tank_{player.tank_level}']
            [player.color]
            [player.direction]
            [player.frame_index]
        )
        player.mask_dict = player.get_tank_masks()
        player.mask = player.mask_dict[player.direction]

    def fortify_base(self):
        """
        Fortify the Phoenix base against enemy tanks' attacks!
        """
        self.game.is_base_fortified = True
        self.game.fortify_timer = pygame.time.get_ticks()
        self.game.apply_fortify()
