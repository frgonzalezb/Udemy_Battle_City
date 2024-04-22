import random
from typing import List

import pygame
from pygame.surface import Surface

import game_config as gc
from ammunition import Bullet


class Tank(pygame.sprite.Sprite):
    """
    Blueprint for all the tank objects.
    """

    def __init__(
            self,
            game,
            assets,
            groups,
            position: tuple[int, int],
            direction: str,
            color: str = 'Silver',
            tank_level: int = 0,
            is_enemy: bool = True
            ) -> None:

        super().__init__()

        # Game object and assets
        self.game = game
        self.assets = assets
        self.groups = groups

        # Sprite groups that may interact with tank
        self.tank_group = self.groups['all_tanks']
        self.player_group = self.groups['player_tanks']

        # Add tank object to the sprite group
        self.tank_group.add(self)

        # Enemy tank criteria
        levels: dict[int, str | None] = {
            0: None,
            4: 'level_0',
            5: 'level_1',
            6: 'level_2',
            7: 'level_3'
        }
        self.level: str | None = levels[tank_level]

        # Tank images
        self.tank_images: dict[str, dict[str, dict]] = self.assets.tank_images
        self.spawn_images: dict[str, Surface] = self.assets.spawn_star_images

        # Tank position and direction
        self.spawn_pos: tuple[int, int] = position
        self.pos_x, self.pos_y = self.spawn_pos
        self.direction: str = direction

        # Tank spawning / active
        self.is_spawning: bool = True
        self.is_active: bool = False

        # Common tank attributes
        self.tank_level: int = tank_level
        self.color: str = color
        self.tank_speed: int | float = (
            gc.TANK_SPEED if not self.level
            else gc.TANK_SPEED * gc.TANK_SPAWN_CRITERIA[self.level]['speed']
        )
        self.power: int = (
            1 if not self.level
            else gc.TANK_SPEED * gc.TANK_SPAWN_CRITERIA[self.level]['power']
        )
        self.bullet_speed_modifier: int = 1
        self.bullet_speed: int = (
            gc.TANK_SPEED * (3 * self.bullet_speed_modifier)
        )
        self.score: int = (
            100 if not self.level
            else gc.TANK_SPAWN_CRITERIA[self.level]['score']
        )
        self.is_enemy: bool = is_enemy
        self.tank_health: int = 1

        # Tank image, rectangle, and frame index
        self.frame_index: int = 0
        self.image: Surface = (
            self.tank_images[f'Tank_{self.tank_level}']
            [self.color]
            [self.direction]
            [self.frame_index]
        )
        self.rect = self.image.get_rect(topleft=self.spawn_pos)
        self.width, self.height = self.image.get_size()

        # Shoot cooldowns and bullet totals
        self.bullet_limit: int = 1
        self.bullet_sum: int = 0
        self.shot_cooldown_time: int = 500  # milliseconds
        self.shot_cooldown: int = pygame.time.get_ticks()

        # Tank paralysis
        self.is_paralyzed: bool = False
        self.paralysis: int = gc.TANK_PARALYSIS
        self.paralysis_timer: int = pygame.time.get_ticks()

        # Spawn images
        self.spawn_image = self.spawn_images[f'star_{self.frame_index}']
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_anim_timer = pygame.time.get_ticks()

        # Tank image masks
        self.mask_dict = self.get_tank_masks()
        self.mask = self.mask_dict[self.direction]
        # self.mask_image = self.mask.to_surface()
        self.mask_direction: str = self.direction

    def input(self) -> None:
        pass

    def update(self) -> None:
        if self.is_spawning:
            self.update_spawning_animation()
            self.stop_spawning_animation()
            return

        if (
            self.is_paralyzed and
            pygame.time.get_ticks() - self.paralysis_timer >= self.paralysis
        ):
            self.is_paralyzed = False

    def draw(self, window) -> None:
        """
        Draws the tank-related images on the screen.
        """
        self.draw_spawn_star(window)
        self.draw_tank(window)

    def move(self, direction: str) -> None:
        """
        Moves the tank in the given direction.
        """
        if not self.is_active:
            return

        self.direction = direction

        if self.is_paralyzed:
            self.image = (
                self.tank_images[f'Tank_{self.tank_level}']
                [self.color]
                [self.direction]
                [self.frame_index]
            )
            return

        match direction:
            case 'Up':
                self.pos_y -= self.tank_speed
                self.pos_x = self.align_tank_movement_to_grid(self.pos_x)
                if self.pos_y < gc.SCREEN_BORDER_TOP:
                    self.pos_y = gc.SCREEN_BORDER_TOP
            case 'Down':
                self.pos_y += self.tank_speed
                self.pos_x = self.align_tank_movement_to_grid(self.pos_x)
                if self.pos_y + self.height > gc.SCREEN_BORDER_BOTTOM:
                    self.pos_y = gc.SCREEN_BORDER_BOTTOM - self.height
            case 'Left':
                self.pos_x -= self.tank_speed
                self.pos_y = self.align_tank_movement_to_grid(self.pos_y)
                if self.pos_x < gc.SCREEN_BORDER_LEFT:
                    self.pos_x = gc.SCREEN_BORDER_LEFT
            case 'Right':
                self.pos_x += self.tank_speed
                self.pos_y = self.align_tank_movement_to_grid(self.pos_y)
                if self.pos_x + self.width > gc.SCREEN_BORDER_RIGHT:
                    self.pos_x = gc.SCREEN_BORDER_RIGHT - self.width
            case _:
                raise ValueError

        # Update the tank rectangle position
        self.rect.topleft = (self.pos_x, self.pos_y)

        # Update the tank animation
        self.update_tank_movement_animation()

        # Check for tank collisions with other tanks
        self.check_tank_on_tank_collision()

        # Check for tank collisions with obstacles
        self.check_tank_on_obstacle_collision()

    def align_tank_movement_to_grid(self, pos: int) -> int:
        """
        Resolves that awkward imposibility to movement when some tank
        rect pixel collides with the corner of an obstacle.
        """
        offset: int = pos % (gc.IMAGE_SIZE // 2)

        if offset != 0:
            if offset < gc.SPRITE_SIZE:
                pos -= pos % gc.SPRITE_SIZE
            elif offset > gc.SPRITE_SIZE:
                pos += (gc.SPRITE_SIZE) - (pos % gc.SPRITE_SIZE)

        return pos

    def draw_spawn_star(self, window) -> None:
        """
        Draws the spawn star on the screen.
        """
        if not self.is_spawning:
            return

        window.blit(self.spawn_image, self.rect)

    def draw_tank(self, window):
        """
        Draws the tank on the screen.
        """
        if not self.is_active:
            return

        window.blit(self.image, self.rect)
        # window.blit(self.mask_image, self.rect)
        pygame.draw.rect(window, gc.RGB_RED, self.rect, 1)  # dbg

    def update_spawning_animation(self) -> None:
        """
        Update the spawning star animation, if the required amount of
        time for each image has passed.
        """
        animation_time = pygame.time.get_ticks() - self.spawn_anim_timer
        if animation_time >= gc.SPAWN_ANIM_TIME:
            self.animate_spawn_star()

    def animate_spawn_star(self) -> None:
        """
        Cycles through the spawn star images to emulate a spawning icon.
        """
        self.frame_index += 1
        self.frame_index = self.frame_index % len(self.spawn_images)
        self.spawn_image = self.spawn_images[f'star_{self.frame_index}']
        self.spawn_anim_timer = pygame.time.get_ticks()

    def stop_spawning_animation(self) -> None:
        """
        If total spawn time has passed, defeats the spawning animation
        and the tank sprite enters the game.
        """
        spawn_time = pygame.time.get_ticks() - self.spawn_timer
        if spawn_time > gc.TOTAL_SPAWN_TIME:
            colliding_sprites: List = pygame.sprite.spritecollide(
                self,
                self.tank_group,
                False
            )
            is_our_current_tank: bool = len(colliding_sprites) == 1
            if is_our_current_tank:
                self.frame_index = 0
                self.is_spawning = False
                self.is_active = True
            else:
                self.check_tank_on_spawn_star_collision(colliding_sprites)

    def update_tank_movement_animation(self) -> None:
        """
        Simulates the tank moving.
        """
        self.frame_index += 1
        image_list_length = len(
            self.tank_images[f'Tank_{self.tank_level}']
            [self.color]
            [self.direction]
        )
        self.frame_index = self.frame_index % image_list_length
        self.image = (
            self.tank_images[f'Tank_{self.tank_level}']
            [self.color]
            [self.direction]
            [self.frame_index]
        )
        if self.mask_direction != self.direction:
            self.mask_direction = self.direction
            self.mask = self.mask_dict[self.mask_direction]
            # self.mask_image = self.mask.to_surface()

    def check_tank_on_tank_collision(self) -> None:
        """
        Checks if there is any overlapping between the current
        tank sprite and one or more tanks sprites.

        NOTE: The current tank object has also been included in the
        tank group. Indeed, there will always be a collision detected in
        the collision list and the current tank object will be colliding
        with itself.
        """
        tank_collision_list = pygame.sprite.spritecollide(
            self,
            self.tank_group,
            False
        )

        if len(tank_collision_list) == 1:
            return  # The current tank is just colliding with itself!

        for tank in tank_collision_list:
            if tank == self or tank.is_spawning:
                continue  # Skip if it's the current tank

            self._handle_tank_collisions(tank)

    def check_tank_on_obstacle_collision(self) -> None:
        obstacle_collision = pygame.sprite.spritecollide(
            self,
            self.groups['impassable_tiles'],
            False
        )
        for obstacle in obstacle_collision:
            self._handle_tank_collisions(obstacle)

    def _handle_tank_collisions(self, obj) -> None:
        """
        Utility method that abstracts both tank-on-tank and
        tank-on-obstacle collision logic (which are separated into
        their respective functions in the original code).

        In any case, figures out where's the collision and handles it.
        """
        if self.direction == 'Right' and self.rect.right >= obj.rect.left:
            self.rect.right = obj.rect.left
            self.pos_x = self.rect.x
        elif self.direction == 'Left' and self.rect.left <= obj.rect.right:
            self.rect.left = obj.rect.right
            self.pos_x = self.rect.x
        elif self.direction == 'Up' and self.rect.top <= obj.rect.bottom:
            self.rect.top = obj.rect.bottom
            self.pos_y = self.rect.y
        elif self.direction == 'Down' and self.rect.bottom >= obj.rect.top:
            self.rect.bottom = obj.rect.top
            self.pos_y = self.rect.y

    def check_tank_on_spawn_star_collision(
            self,
            colliding_sprites: List
            ) -> None:
        """
        Fixes infinite spawn bug if two spawn stars are colliding.
        """
        for tank in colliding_sprites:
            if tank.is_active:
                return
            if tank == self:
                continue
            if self.is_spawning and tank.is_spawning:
                self.frame_index = 0
                self.is_spawning = False
                self.is_active = True

    def shoot(self) -> None:
        if self.bullet_sum >= self.bullet_limit:
            return

        Bullet(
            self.assets,
            self.groups,
            self,
            self.rect.center,
            self.direction,
        )
        self.bullet_sum += 1

    def paralyze_tank(self, paralysis_time) -> None:
        """
        If player tank is hit by player tank, or if the freeze power up
        is used.
        """
        self.paralysis = paralysis_time
        self.is_paralyzed = True
        self.paralysis_timer = pygame.time.get_ticks()

    def destroy_tank(self) -> None:
        """
        Damages tank's health, and if health at zero, destroys the tank.
        """
        self.tank_health -= 1

        if self.tank_health <= 0:
            self.kill()
            self.game.enemies_killed -= 1

    def get_tank_masks(self) -> dict[str, pygame.Mask]:
        """
        Creates and returns a dictionary of tank masks for all
        directions.
        """
        images = {
            direction: pygame.mask.from_surface(
                self.tank_images[f'Tank_{self.tank_level}'][self.color]
                [direction][0]
            )
            for direction in ['Up', 'Down', 'Left', 'Right']
        }
        return images


class PlayerTank(Tank):
    """
    Blueprint specifically for Player 1 and Player 2 tanks.

    NOTE: We want the tank class to be the base object for all of the
    tanks in the game, with only slight differences between the player
    tank and the enemy tanks. So, we could go ahead and built the input
    method inside of the base Tank class, but... we'll run into issues
    because if we try to move the tank, all of the tanks on the screen
    will move! So, this class has come to provide a solution through the
    use of OOP's inheritance.
    """

    def __init__(
            self,
            game,
            assets,
            groups,
            position: tuple,
            direction: str,
            color: str = 'Silver',
            tank_level: int = 0,
            ) -> None:

        super().__init__(
            game,
            assets,
            groups,
            position,
            direction,
            color,
            tank_level,
            is_enemy=False
        )

        self.player_group.add(self)

        # Player lives
        self.lives = 3

        # Level score tracking
        self.score_list = []

    def input(
            self,
            key_pressed: pygame.key.ScancodeWrapper
            ) -> None:
        """
        Define the controls for a player tank object, depending on
        its color.

        NOTE: Player 1 is Gold, and Player 2 is Green.
        """
        if self.color == 'Gold':
            self.set_control_keys(
                key_pressed,
                up_key=pygame.K_w,
                down_key=pygame.K_s,
                left_key=pygame.K_a,
                right_key=pygame.K_d
            )

        if self.color == 'Green':
            self.set_control_keys(
                key_pressed,
                up_key=pygame.K_UP,
                down_key=pygame.K_DOWN,
                left_key=pygame.K_LEFT,
                right_key=pygame.K_RIGHT
            )

    def set_control_keys(
            self,
            key_pressed: pygame.key.ScancodeWrapper,
            up_key: int,
            down_key: int,
            left_key: int,
            right_key: int
            ) -> None:
        """
        Defines the keys for controlling a player.

        NOTE 1: Key params are referred to indexes from Pygame's key
        variables (e.g. `pygame.K_UP`). Although they can be passed in
        directly as pure integer values, it's recommended to use the
        `pygame.K_somekey` style for readability.

        NOTE 2: Controls can't be defined by the cleaner `X if Y else Z`
        style, because it allows diagonal movements, which are forbidden
        in the original game.
        """
        if key_pressed[up_key]:
            self.move('Up')
        elif key_pressed[down_key]:
            self.move('Down')
        elif key_pressed[left_key]:
            self.move('Left')
        elif key_pressed[right_key]:
            self.move('Right')

    def spawn_on_new_stage(self, position: tuple[int, int]):
        """
        Spawns the player tank on the new stage screen, according to the
        position values passed in. It also forces the tank to be in
        "Up" direction.

        NOTE: Although it seems weirdly at first glance, the "position"
        argument must need to be unpacked to reset the player tank at
        the start position and then repacked in the self.rect.topleft
        statement.
        """
        self.tank_group.add(self)
        self.is_spawning = True
        self.is_active = False
        self.direction = 'Up'
        self.pos_x, self.pos_y = position
        self.image = (
            self.tank_images[f'Tank_{self.tank_level}']
            [self.color][self.direction][self.frame_index]
        )
        self.rect.topleft = (self.pos_x, self.pos_y)
        self.score_list.clear()


class EnemyTank(Tank):

    def __init__(
            self,
            game,
            assets,
            groups,
            position: tuple[int, int],
            direction: str,
            color: str = 'Silver',
            tank_level: int = 0,
            is_enemy: bool = True
            ) -> None:

        super().__init__(
            game,
            assets,
            groups,
            position,
            direction,
            color,
            tank_level,
            is_enemy
        )

        self.time_between_shots: int = random.choice([300, 600, 900])
        self.shot_timer: int = pygame.time.get_ticks()

        def update(self) -> None:
            super().update()
            if self.is_spawning:
                return
            self.fire()

        def fire(self) -> None:
            if self.is_paralyzed:
                return
            current_time = pygame.time.get_ticks()
            if (
                self.bullet_sum < self.bullet_limit and
                current_time - self.shot_timer >= self.time_between_shots
            ):
                self.shoot()
                self.shot_timer = pygame.time.get_ticks()
