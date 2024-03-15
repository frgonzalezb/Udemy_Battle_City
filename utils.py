'''
Random utilities for the code.

NOTE: This is my own stuff, not part of the course!
'''


def get_map_tile_by_type(type: str, sprite_size: int):
    '''
    Delivers the coordinates and size for each map tile, according to 
    its type (bricks, water, etc.).
    '''
    if type == 'bricks':
        return {
            'small': [(sprite_size * 16), (sprite_size * 4), 8, 8],
            'small_right': [(sprite_size * 16), (sprite_size * 4), 8, 8],
            'small_bottom': [(sprite_size * 17), (sprite_size * 4) + 4, 8, 8],
            'small_left': [(sprite_size * 17), (sprite_size * 4), 8, 8],
            'small_top': [(sprite_size * 16), (sprite_size * 4), 8, 8]
        }
    elif type == 'steel':
        return {
            'small': [(sprite_size * 16), (sprite_size * 4) + 8, 8, 8]
        }
    elif type == 'forest':
        return {
            'small': [(sprite_size * 16) + 8, (sprite_size * 4) + 8, 8, 8]
        }
    elif type == 'ice':
        return {
            'small': [(sprite_size * 17), (sprite_size * 4) + 8, 8, 8]
        }
    elif type == 'water':
        return {
            'small_1': [(sprite_size * 16) + 8, (sprite_size * 5), 8, 8],
            'small_2': [(sprite_size * 17), (sprite_size * 5), 8, 8],
        }
    