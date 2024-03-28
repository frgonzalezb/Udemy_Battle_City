import pygame
import game_config as gc


class Tank(pygame.sprite.Sprite):
    """
    Represents Tank objects.
    """

    def __init__(
            self,
            game,
            assets,
            groups: dict[str, pygame.sprite.Group],
            position: tuple,
            direction: str,
            color: str = 'Silver',
            tank_level: int = 0
            ) -> None:
        super().__init__()
        """
        NOTE: In order to avoid circular imports, some params have not
        been defined to an explicit type (but they should, IMO).

        Non-defined keyword arguments:
            game -- the Game class object.
            assets -- the GameAssets class object.
        """

        # Game object and assets
        self.game = game
        self.assets = assets
        self.groups = groups

        # Sprite groups that may interact with tank
        self.tank_group = self.groups['All_Tanks']

        # Add tank object to the sprite group
        self.tank_group.add(self)

        # Tank images
        self.tank_images = self.assets.tank_images

        # Tank position and direction
        self.spawn_pos = position
        self.pos_x, self.pos_y = self.spawn_pos
        self.direction = direction

        # Common tank attributes
        self.active = True
        self.tank_level = tank_level
        self.color = color
        self.tank_speed = gc.TANK_SPEED

        # Tank image, rectangle, and frame index
        self.frame_index = 0
        self.image = (
            self.tank_images[f'Tank_{self.tank_level}']
            [self.color]
            [self.direction]
            [self.frame_index]
        )
        self.rect = self.image.get_rect(topleft=self.spawn_pos)

    def input(self) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, window) -> None:
        if self.active:
            window.blit(self.image, self.rect)
            pygame.draw.rect(window, gc.RGB_RED, self.rect, 1)  # dbg

    def move(self, direction: str) -> None:
        """
        Move the tank in the passed direction.
        """
        self.direction = direction

        match direction:
            case 'Up':
                self.pos_y -= self.tank_speed
            case 'Down':
                self.pos_y += self.tank_speed
            case 'Left':
                self.pos_x -= self.tank_speed
            case 'Right':
                self.pos_x += self.tank_speed

        # Update the tank rectangle position
        self.rect.topleft = (self.pos_x, self.pos_y)

        # Update the tank animation
        self.update_tank_movement_animation()

        # Check for tank collisions with other tanks
        self.check_tank_on_tank_collisions()

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

    def check_tank_on_tank_collisions(self) -> None:
        """
        Checks if there is any overlapping between the current
        tank sprite and one or more tanks sprites.

        NOTE: The current tank object has also been included in the
        tank group. Indeed, there will always be a collision detected in
        the collision list and the current tank object will be colliding
        with itself.

        FIXME: This function seems to feature some long and nested
        code, so a refactor will be nice.
        """
        tank_collision_list = pygame.sprite.spritecollide(
            self,
            self.tank_group,
            False
        )

        if len(tank_collision_list) == 1:
            # The current tank is just colliding with itself!
            return

        for tank in tank_collision_list:
            # Skip the tank if it's the current one
            if tank == self:
                continue

            # Figure out where is the collision
            if self.direction == 'Right':
                if (self.rect.right >= tank.rect.left
                        and self.rect.bottom > tank.rect.top
                        and self.rect.top < tank.rect.bottom):
                    self.rect.right = tank.rect.left
                    self.pos_x = self.rect.x
            elif self.direction == 'Left':
                if (self.rect.left <= tank.rect.right
                        and self.rect.bottom > tank.rect.top
                        and self.rect.top < tank.rect.bottom):
                    self.rect.left = tank.rect.right
                    self.pos_x = self.rect.x
            elif self.direction == 'Up':
                if (self.rect.top <= tank.rect.bottom
                        and self.rect.left < tank.rect.right
                        and self.rect.right > tank.rect.left):
                    self.rect.top = tank.rect.bottom
                    self.pos_y = self.rect.y
            elif self.direction == 'Down':
                if (self.rect.bottom >= tank.rect.top
                        and self.rect.left < tank.rect.right
                        and self.rect.right > tank.rect.left):
                    self.rect.bottom = tank.rect.top
                    self.pos_y = self.rect.y


class PlayerTank(Tank):
    """
    Represents the Player Tank object.

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
            groups: dict[str, pygame.sprite.Group],
            position: tuple,
            direction: str,
            color: str = 'Silver',
            tank_level: int = 0
            ) -> None:
        super().__init__(
            game,
            assets,
            groups,
            position,
            direction,
            color,
            tank_level
        )

    def input(
            self,
            key_pressed: pygame.key.ScancodeWrapper
            ) -> None:
        """
        Move the player tank according to the key pressed.

        NOTE: Player 1 is Gold, Player 2 is Green.
        """
        if self.color == 'Gold':
            if key_pressed[pygame.K_w]:
                self.move('Up')
            elif key_pressed[pygame.K_s]:
                self.move('Down')
            elif key_pressed[pygame.K_a]:
                self.move('Left')
            elif key_pressed[pygame.K_d]:
                self.move('Right')

        if self.color == 'Green':
            if key_pressed[pygame.K_UP]:
                self.move('Up')
            elif key_pressed[pygame.K_DOWN]:
                self.move('Down')
            elif key_pressed[pygame.K_LEFT]:
                self.move('Left')
            elif key_pressed[pygame.K_RIGHT]:
                self.move('Right')
