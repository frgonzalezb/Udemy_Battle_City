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
        game -- the Game class object
        assets -- the GameAssets class object
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

    def move(self, direction: str) -> None:
        """
        Move the tank in the passed direction.
        """
        self.direction = direction

        if direction == 'Up':
            self.pos_y -= self.tank_speed
        elif direction == 'Down':
            self.pos_y += self.tank_speed
        elif direction == 'Left':
            self.pos_x -= self.tank_speed
        elif direction == 'Right':
            self.pos_x += self.tank_speed

        # Update the tank rectangle position
        self.rect.topleft = (self.pos_x, self.pos_y)

        # Update the tank animation
        self.update_tank_movement_animation()

    def update_tank_movement_animation(self) -> None:
        """
        Update the animation images to simulate the tank moving.
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

    def input(self, key_pressed) -> None:
        """
        Move the player tank according to the key pressed.
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
