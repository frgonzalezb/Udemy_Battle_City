import pygame

# import game_config as gc


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
        game -- the Game class (or a Game class object)
        assets -- the GameAssets class (or a GameAssets class object)
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

        # Tank image, rectangle, and frame index
        self.frame_index = 0
        self.image = (
            self.tank_images[f'Tank_{self.tank_level}']
            [self.color]
            [self.direction]
            [self.frame_index]
        )
        self.rect = self.image.get_rect(topleft=self.spawn_pos)

    def input(self):
        pass

    def update(self):
        pass

    def draw(self, window):
        if self.active:
            window.blit(self.image, self.rect)
