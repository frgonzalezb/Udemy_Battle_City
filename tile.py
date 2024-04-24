import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite, Group

# import game_config as gc


class TileType(Sprite):

    def __init__(
            self,
            pos: tuple[int, int],
            group: Group,
            map_tiles: dict[str, Surface]
            ) -> None:
        super().__init__(group)

        self.group: Group = group

        self.images: dict[str, Surface] = map_tiles
        self.image: Surface

        self.pos_x: int = pos[0]
        self.pos_y: int = pos[1]

    def update(self) -> None:
        pass

    def draw(self, window: Surface) -> None:
        window.blit(self.image, self.rect)

    def _get_rect_and_size(self, position: tuple[int, int]) -> None:
        self.rect = self.image.get_rect(topleft=position)
        self.width, self.height = self.image.get_size()

    def handle_bullet_hit(self, bullet):
        pass


class BrickTile(TileType):

    def __init__(self, pos, group, map_tiles) -> None:
        super().__init__(pos, group, map_tiles)

        self.name: str = 'Brick'
        self.health: int = 2

        self.image: Surface = self.images['small']
        self._get_rect_and_size(position=(self.pos_x, self.pos_y))

    def handle_bullet_hit(self, bullet):
        bullet.update_owner()
        bullet.kill()

        self.health -= 1
        if self.health <= 0:
            self.kill()
        self._reshape_brick_tile(bullet)

    def _reshape_brick_tile(self, bullet):
        """
        Utility method for the handle_bullet_hit() one, in order to
        make the code a little more readable.
        """
        if bullet.direction == 'Left':
            self.image = self.images['small_left']
            self._get_rect_and_size(
                (self.pos_x, self.pos_y)
            )
        elif bullet.direction == 'Right':
            self.image = self.images['small_right']
            self._get_rect_and_size(
                (self.pos_x + self.width // 2, self.pos_y)
            )
        elif bullet.direction == 'Up':
            self.image = self.images['small_top']
            self._get_rect_and_size(
                (self.pos_x, self.pos_y)
            )
        elif bullet.direction == 'Down':
            self.image = self.images['small_bottom']
            self._get_rect_and_size(
                (self.pos_x, self.pos_y + self.height // 2)
            )


class SteelTile(TileType):

    def __init__(self, pos, group, map_tiles) -> None:
        super().__init__(pos, group, map_tiles)

        self.name: str = 'Steel'

        self.image: Surface = self.images['small']
        self._get_rect_and_size(position=(self.pos_x, self.pos_y))

    def handle_bullet_hit(self, bullet):
        bullet.update_owner()
        bullet.kill()
        if bullet.power > 2:
            self.kill()


class ForestTile(TileType):

    def __init__(self, pos, group, map_tiles) -> None:
        super().__init__(pos, group, map_tiles)

        self.name: str = 'Forest'

        self.image: Surface = self.images['small']
        self._get_rect_and_size(position=(self.pos_x, self.pos_y))


class IceTile(ForestTile):

    def __init__(self, pos, group, map_tiles) -> None:
        super().__init__(pos, group, map_tiles)

        self.name: str = 'Ice'

        self.image: Surface = self.images['small']
        self._get_rect_and_size(position=(self.pos_x, self.pos_y))


class WaterTile(TileType):

    def __init__(self, pos, group, map_tiles) -> None:
        super().__init__(pos, group, map_tiles)

        self.name: str = 'Water'

        self.image: Surface = self.images['small_1']
        self._get_rect_and_size(position=(self.pos_x, self.pos_y))

        # For water animation
        self.frame_index: int = 0
        self.timer: int = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.timer >= 500:
            self.frame_index = 1 if self.frame_index == 0 else 0
            self.timer: int = pygame.time.get_ticks()  # reset timer
            self.image = self.images[f'small_{self.frame_index + 1}']
