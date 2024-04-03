"""
Main game settings file.
"""


from utilities import get_sprite_object


# Game screen settings
SPRITE_SIZE = 16
SPRITE_SCALE = 4

IMAGE_SIZE = SPRITE_SIZE * SPRITE_SCALE

SCREEN_WIDTH = 16 * IMAGE_SIZE
SCREEN_HEIGHT = 14 * IMAGE_SIZE

GAME_SCREEN = (IMAGE_SIZE, IMAGE_SIZE // 2, IMAGE_SIZE * 13, IMAGE_SIZE * 13)
INFO_PANEL_X, INFO_PANEL_Y = SCREEN_WIDTH - (IMAGE_SIZE * 2), IMAGE_SIZE // 2

FPS = 60

RGB_BLACK = (0, 0, 0)
RGB_RED = (255, 0, 0)
RGB_GREY = (99, 99, 99)

# Tank variables
TANK_SPEED = IMAGE_SIZE // SPRITE_SIZE

SPAWN_ANIM_TIME = 50     # milliseconds
TOTAL_SPAWN_TIME = 2000  # milliseconds

# Sprites
SPAWN_STAR = {
    f'star_{i}': get_sprite_object(
        pos_x=SPRITE_SIZE * (16 + i),
        pos_y=SPRITE_SIZE * 6,
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i in range(4)
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

POWER_UPS = {
    power_up: get_sprite_object(
        pos_x=(SPRITE_SIZE * (15 + i)),
        pos_y=(SPRITE_SIZE * 7),
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i, power_up in enumerate([
        'shield',
        'freeze',
        'fortify',
        'power',
        'explosion',
        'extra_life',
        'special'
    ], 1)
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
        ),
        'small_bottom': get_sprite_object(
            pos_x=(SPRITE_SIZE * 17),
            pos_y=(SPRITE_SIZE * 4) + 4,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 4)
        ),
        'small_left': get_sprite_object(
            pos_x=(SPRITE_SIZE * 17) + 8,
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 4),
            height=round(SPRITE_SIZE / 2)
        ),
        'small_top': get_sprite_object(
            pos_x=(SPRITE_SIZE * 18),
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 4)
        )
    },
    'steel': {
        'small': get_sprite_object(
            pos_x=(SPRITE_SIZE * 16),
            pos_y=(SPRITE_SIZE * 4) + 8,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        )
    },
    'forest': {
        'small': get_sprite_object(
            pos_x=(SPRITE_SIZE * 16) + 8,
            pos_y=(SPRITE_SIZE * 4) + 8,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        )
    },
    'ice': {
        'small': get_sprite_object(
            pos_x=(SPRITE_SIZE * 17),
            pos_y=(SPRITE_SIZE * 4) + 8,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        )
    },
    'water': {
        'small_1': get_sprite_object(
            pos_x=(SPRITE_SIZE * 16) + 8,
            pos_y=(SPRITE_SIZE * 5),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        ),
        'small_2': get_sprite_object(
            pos_x=(SPRITE_SIZE * 17),
            pos_y=(SPRITE_SIZE * 5),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        ),
    }
}

HUD_INFO = {
    'stage': get_sprite_object(
        pos_x=(SPRITE_SIZE * 20) + 8,
        pos_y=(SPRITE_SIZE * 11),
        width=(SPRITE_SIZE // 2) * 5,
        height=SPRITE_SIZE // 2
    ),
    'num_0': get_sprite_object(
        pos_x=(SPRITE_SIZE * 20) + 8,
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_1': get_sprite_object(
        pos_x=(SPRITE_SIZE * 21),
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_2': get_sprite_object(
        pos_x=(SPRITE_SIZE * 21) + 8,
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_3': get_sprite_object(
        pos_x=(SPRITE_SIZE * 22),
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_4': get_sprite_object(
        pos_x=(SPRITE_SIZE * 22) + 8,
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_5': get_sprite_object(
        pos_x=(SPRITE_SIZE * 20) + 8,
        pos_y=(SPRITE_SIZE * 12),
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_6': get_sprite_object(
        pos_x=(SPRITE_SIZE * 21),
        pos_y=(SPRITE_SIZE * 12),
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_7': get_sprite_object(
        pos_x=(SPRITE_SIZE * 21) + 8,
        pos_y=(SPRITE_SIZE * 12),
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_8': get_sprite_object(
        pos_x=(SPRITE_SIZE * 22),
        pos_y=(SPRITE_SIZE * 12),
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'num_9': get_sprite_object(
        pos_x=(SPRITE_SIZE * 22) + 8,
        pos_y=(SPRITE_SIZE * 12),
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'life': get_sprite_object(
        pos_x=(SPRITE_SIZE * 20),
        pos_y=(SPRITE_SIZE * 12),
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    'info_panel': get_sprite_object(
        pos_x=(SPRITE_SIZE * 23),
        pos_y=(SPRITE_SIZE * 0),
        width=(SPRITE_SIZE * 2),
        height=(SPRITE_SIZE * 15)
    ),
    'grey_square': get_sprite_object(
        pos_x=(SPRITE_SIZE * 23),
        pos_y=(SPRITE_SIZE * 0),
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    )
}

NUMBERS = {
    0: get_sprite_object(
        pos_x=0,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    1: get_sprite_object(
        pos_x=8,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    2: get_sprite_object(
        pos_x=16,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    3: get_sprite_object(
        pos_x=24,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    4: get_sprite_object(
        pos_x=32,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    5: get_sprite_object(
        pos_x=0,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    6: get_sprite_object(
        pos_x=8,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    7: get_sprite_object(
        pos_x=16,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    8: get_sprite_object(
        pos_x=24,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    9: get_sprite_object(
        pos_x=32,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    )
}

CONTEXT = {
    'pause': get_sprite_object(
        pos_x=(SPRITE_SIZE * 18),
        pos_y=(SPRITE_SIZE * 11),
        width=round((SPRITE_SIZE / 2) * 5),
        height=round(SPRITE_SIZE / 2)
    ),
    'game_over': get_sprite_object(
        pos_x=(SPRITE_SIZE * 18),
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=(SPRITE_SIZE * 2),
        height=SPRITE_SIZE
    )
}
