"""
Random utilities for the source code.

This module is made by me, mostly for cleaning up the code,
because of the code smells I've found in some parts of
the original code provided from the course.

It's not part of the course!
"""


def get_sprite_object(
        pos_x: int,
        pos_y: int,
        width: int,
        height: int
        ) -> dict[str, int]:
    """
    Returns a dictionary object which represents the position and size
    of the sprite within the spritesheet.
    """
    return {'pos_x': pos_x, 'pos_y': pos_y, 'width': width, 'height': height}
