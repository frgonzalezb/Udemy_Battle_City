# import pygame
from pygame import Surface
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


class BrickTile(TileType):

    def __init__(self, pos, group, map_tiles) -> None:
        super().__init__(pos, group, map_tiles)

        self.name: str = 'Brick'
        self.health: int = 2

        self.image: Surface = self.images['small']
        self._get_rect_and_size(position=(self.pos_x, self.pos_y))
