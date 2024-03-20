"""
Random utilities for the source code.

This module is made by me, mostly for cleaning up the code,
because of the code smells I've found in some parts of
the original code provided from the course.

It's not part of the course!
"""


class Sprite:
    """
    Represents a sprite object.
    """

    def __init__(self) -> None:
        pass


def get_sprite_from_spritesheet(
        coord_x: int,
        coord_y: int,
        spr_width: int,
        spr_height: int
        ) -> list[int]:
    """
    Returns a list object which represents a unique sprite image
    from the spritesheet, for given coordinates and size values.
    """
    return [coord_x, coord_y, spr_width, spr_height]
