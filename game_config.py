"""
Main game settings file.
"""


from utilities import get_sprite_object


SPRITE_SIZE = 16
SPRITE_SCALE = 4

IMAGE_SIZE = SPRITE_SIZE * SPRITE_SCALE

# Screen settings
# SCREEN_WIDTH = 1024 # Original
# SCREEN_HEIGHT = 896 # Original
# SCREEN_WIDTH = 16 * IMAGE_SIZE # Original edited
# SCREEN_HEIGHT = 14 * IMAGE_SIZE # Original edited
SCREEN_WIDTH = 800      # Momentary
SCREEN_HEIGHT = 600     # Momentary

FPS = 60

RGB_BLACK = (0, 0, 0)

# Sprites
SPAWN_STAR = {
    f'star_{i}': get_sprite_object(
        pos_x=SPRITE_SIZE * (15 + i),
        pos_y=SPRITE_SIZE * 6,
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i in range(1, 5)
}

SHIELD = {
    f'shield_{i}': get_sprite_object(
        pos_x=SPRITE_SIZE * (15 + i),
        pos_y=SPRITE_SIZE * 9,
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i in range(1, 3)
}

POWER_UP_LIST = [
    'shield',
    'freeze',
    'fortify',
    'power',
    'explosion',
    'extra_life',
    'special'
]
POWER_UPS = {
    power_up: get_sprite_object(
        pos_x=(SPRITE_SIZE * (15 + i)),
        pos_y=(SPRITE_SIZE * 7),
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i, power_up in enumerate(POWER_UP_LIST, 1)
}

SCORES = {
    score: get_sprite_object(
        pos_x=(SPRITE_SIZE * (17 + i)),
        pos_y=(SPRITE_SIZE * 10),
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i, score in enumerate(['100', '200', '300', '400', '500'], 1)
}

FLAGS = {
    flag: get_sprite_object(
        pos_x=(SPRITE_SIZE * (18 + i)),
        pos_y=(SPRITE_SIZE * 2),
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i, flag in enumerate(['Phoenix_Alive', 'Phoenix_Destroyed'], 1)
}

EXPLOSIONS = {
    f'explode_{i}': get_sprite_object(
        pos_x=(SPRITE_SIZE * ((15 + i) if i < 5 else 21)),
        pos_y=SPRITE_SIZE * 8,
        width=SPRITE_SIZE if i < 4 else (SPRITE_SIZE * 2),
        height=SPRITE_SIZE if i < 4 else (SPRITE_SIZE * 2)
    )
    for i in range(1, 6)
}

BULLETS = {
    direction: get_sprite_object(
        pos_x=(SPRITE_SIZE * (20 if direction in ["Up", "Left"] else 21)),
        pos_y=(SPRITE_SIZE * 2),
        width=round(SPRITE_SIZE / 2),
        height=round(SPRITE_SIZE / 2)
    )
    for direction in ['Up', 'Left', 'Down', 'Right']
}

MAP_TILES = {
    'bricks': {
        'small': get_sprite_object(
            pos_x=(SPRITE_SIZE * 16),
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        ),
        'small_right': get_sprite_object(
            pos_x=(SPRITE_SIZE * 16) + 12,
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 4),
            height=round(SPRITE_SIZE / 2)
        )
    },
    'steel': {
        'small': get_sprite_object(
            pos_x=(SPRITE_SIZE * 16),
            pos_y=(SPRITE_SIZE * 4) + 8,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        )
    }
}

HUD_INFO = {}

zero = get_sprite_object(
    pos_x=0,
    pos_y=0,
    width=round(SPRITE_SIZE / 2),
    height=round(SPRITE_SIZE / 2)
)
NUMBERS = {
    0: zero
}

CONTEXT = {}
