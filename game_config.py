'''Main game settings file.'''


from utils import get_map_tile_by_type


# Sprite settings
SPRITE_SIZE = 16
SPRITE_SCALE = 4
IMG_SIZE = SPRITE_SIZE * SPRITE_SCALE

# Screen settings
# SCREEN_WIDTH = 1024 # Original
# SCREEN_HEIGHT = 896 # Original
# SCREEN_WIDTH = 16 * IMG_SIZE # Original edited
# SCREEN_HEIGHT = 14 * IMG_SIZE # Original edited
SCREEN_WIDTH = 800  # Momentary
SCREEN_HEIGHT = 600 # Momentary

# FPS settings
FPS = 60

# RGB Color definitions
BLACK = (0, 0, 0)


# ----------------------------------------
# Spritesheet images: coordinates and size
# ----------------------------------------

SPAWN_STAR = {
    f'star_{i}': [
        (SPRITE_SIZE * (16 + i)),
        (SPRITE_SIZE * 6),
        SPRITE_SIZE,
        SPRITE_SIZE,  
    ] for i in range(4)
}

SHIELD = {
    f'shield_{i}': [
        (SPRITE_SIZE * 16),
        (SPRITE_SIZE * 9),
        SPRITE_SIZE,
        SPRITE_SIZE,  
    ] for i in range(4)
}

powerup_names = [
    'shield', 
    'freeze', 
    'fortify', 
    'power', 
    'explosion', 
    'extra_life', 
    'special'
]
POWERUPS = {
    name: [
        (SPRITE_SIZE * (16 + i)),
        (SPRITE_SIZE * 7),
        SPRITE_SIZE,
        SPRITE_SIZE,  
    ] for i, name in enumerate(powerup_names)
}

SCORE = {
    value: [
        (SPRITE_SIZE * (18 + i)),
        (SPRITE_SIZE * 10),
        SPRITE_SIZE,
        SPRITE_SIZE,  
    ] for i, value in enumerate(['100', '200', '300', '400', '500'])
}

FLAG = {
    value: [
        (SPRITE_SIZE * (19 + i)),
        (SPRITE_SIZE * 2),
        SPRITE_SIZE,
        SPRITE_SIZE,  
    ] for i, value in enumerate(['Phoenix_Alive', 'Phoenix_Destroyed'])
}

EXPLOSIONS = {
    f'explode_{i + 1}': [
        (SPRITE_SIZE * (16 + i + 1)) if i == 4 else (SPRITE_SIZE * (16 + i)),
        (SPRITE_SIZE * 8),
        SPRITE_SIZE * 2 if i >= 3 else SPRITE_SIZE,
        SPRITE_SIZE * 2 if i >= 3 else SPRITE_SIZE,  
    ] for i in range(5)
}

BULLETS = {
    direction: [
        (SPRITE_SIZE * 20) + (8 if i == 1 or i == 3 else 0),
        (SPRITE_SIZE * 6) + 4,
        (SPRITE_SIZE / 2),
        (SPRITE_SIZE / 2),
    ] if i <= 2 else [
        (SPRITE_SIZE * 21) + (8 if i == 1 or i == 3 else 0),
        (SPRITE_SIZE * 6) + 4,
        (SPRITE_SIZE / 2),
        (SPRITE_SIZE / 2),
    ] for i, direction in enumerate(['Up', 'Left', 'Down', 'Right'])
}

MAP_TILES = {
    'bricks': get_map_tile_by_type('bricks', SPRITE_SIZE),
    'steel': get_map_tile_by_type('steel', SPRITE_SIZE),
    'forest': get_map_tile_by_type('forest', SPRITE_SIZE),
    'ice': get_map_tile_by_type('ice', SPRITE_SIZE),
    'water': get_map_tile_by_type('water', SPRITE_SIZE)
}

# ----------------------------------------
