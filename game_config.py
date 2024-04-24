"""
Main game settings file.
"""


from utilities import get_object_position_and_size


# Game screen settings
SPRITE_SIZE = 16  # px
SPRITE_SCALE = 4

IMAGE_SIZE = SPRITE_SIZE * SPRITE_SCALE  # 64 px

'''
NOTE: The IMAGE_SIZE constant is quite important, because it's used as
base for all the graphical objects in the game and for generating a very
useful grid layout of 64x64-pixels squares to manage them.

According to Harry, the idea of using a grid of 64x64 squares is because
of the ability to resize the entire game screen and then thsese images
will then be resized accordingly or placed in the correct place
according to the screen dimensions, whether the screen width and height
does change, then these items would change along with it.
'''

SCREEN_WIDTH = 16 * IMAGE_SIZE   # px
SCREEN_HEIGHT = 14 * IMAGE_SIZE  # px

GAME_SCREEN = get_object_position_and_size(
    pos_x=IMAGE_SIZE,
    pos_y=IMAGE_SIZE // 2,
    width=IMAGE_SIZE * 13,
    height=IMAGE_SIZE * 13
)
INFO_PANEL_X, INFO_PANEL_Y = SCREEN_WIDTH - (IMAGE_SIZE * 2), IMAGE_SIZE // 2
STD_ENEMIES = 20

SCREEN_BORDER_LEFT = GAME_SCREEN['pos_x']
SCREEN_BORDER_TOP = GAME_SCREEN['pos_y']
SCREEN_BORDER_RIGHT = GAME_SCREEN['width'] + SCREEN_BORDER_LEFT
SCREEN_BORDER_BOTTOM = GAME_SCREEN['height'] + SCREEN_BORDER_TOP

SCREEN_SCROLL_SPEED = 5

TRANSITION_TIMER = 3000  # milliseconds

FPS = 60

RGB_BLACK = (0, 0, 0)
RGB_RED = (255, 0, 0)
RGB_GREY = (99, 99, 99)
RGB_GREEN = (0, 255, 0)

# Tank variables
TANK_SPEED = IMAGE_SIZE // SPRITE_SIZE

TANK_PARALYSIS = 2000    # milliseconds

SPAWN_ANIM_TIME = 50     # milliseconds
TOTAL_SPAWN_TIME = 2000  # milliseconds

ENEMY_TANK_SPAWNS = [
    (0, 0), (0, 1), (1, 0), (1, 1),      # enemy spawn 1
    (12, 0), (12, 1), (13, 0), (13, 1),  # enemy spawn 2
    (24, 0), (24, 1), (25, 0), (25, 1)   # enemy spawn 3
]

PLAYER_TANK_SPAWNS = [
    (8, 24), (8, 25), (9, 24), (9, 25),     # player 1 spawn
    (16, 24), (16, 25), (17, 24), (17, 25)  # player 2 spawn
]

TANK_SPAWNING_TIME = 3000  # milliseconds

# Player 1 and 2 initial positions
PLAYER_1_POS = (
    SCREEN_BORDER_LEFT + IMAGE_SIZE // 2 * 8,
    SCREEN_BORDER_TOP + IMAGE_SIZE // 2 * 24
)

PLAYER_2_POS = (
    SCREEN_BORDER_LEFT + IMAGE_SIZE // 2 * 16,
    SCREEN_BORDER_TOP + IMAGE_SIZE // 2 * 24
)

# Enemy tank spawning positions
ENEMY_POS_1 = (
    SCREEN_BORDER_LEFT + IMAGE_SIZE // 2 * 12,
    SCREEN_BORDER_TOP + IMAGE_SIZE // 2 * 0
)
ENEMY_POS_2 = (
    SCREEN_BORDER_LEFT + IMAGE_SIZE // 2 * 24,
    SCREEN_BORDER_TOP + IMAGE_SIZE // 2 * 0
)
ENEMY_POS_3 = (
    SCREEN_BORDER_LEFT + IMAGE_SIZE // 2 * 0,
    SCREEN_BORDER_TOP + IMAGE_SIZE // 2 * 0
)

BASE = [(12, 24), (12, 25), (13, 24), (13, 25)]
FORT = [
    (11, 25),
    (11, 24),
    (11, 23),
    (12, 23),
    (13, 23),
    (14, 23),
    (14, 24),
    (14, 25)
]

TANK_CRITERIA: dict[str, dict[str, int | float]] = {
    'level_0': {
        'image': 4,
        'health': 1,
        'speed': 0.5,
        'cooldown': 1,
        'power': 1,
        'score': 100
    },
    'level_1': {
        'image': 5,
        'health': 1,
        'speed': 1,
        'cooldown': 1,
        'power': 1,
        'score': 200
    },
    'level_2': {
        'image': 6,
        'health': 1,
        'speed': 0.5,
        'cooldown': 1,
        'power': 2,
        'score': 300
    },
    'level_3': {
        'image': 7,
        'health': 4,
        'speed': 0.5,
        'cooldown': 1,
        'power': 2,
        'score': 400
    }
}

# Tank spawn queue ratios (calculated by Harry)
TANK_SPAWN_QUEUE = {
    'queue_0': [90, 10, 0, 0],
    'queue_1': [80, 20, 0, 0],
    'queue_2': [70, 30, 0, 0],
    'queue_3': [60, 30, 10, 0],
    'queue_4': [50, 30, 20, 0],
    'queue_5': [40, 30, 30, 0],
    'queue_6': [30, 30, 30, 10],
    'queue_7': [20, 30, 30, 20],
    'queue_8': [10, 30, 30, 30],
    'queue_9': [10, 20, 40, 30],
    'queue_10': [10, 10, 50, 30],
    'queue_11': [0, 10, 50, 40],
}

# Sprites
SPAWN_STAR = {
    f'star_{i}': get_object_position_and_size(
        pos_x=SPRITE_SIZE * (16 + i),
        pos_y=SPRITE_SIZE * 6,
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i in range(4)
}

SHIELD = {
    f'shield_{i}': get_object_position_and_size(
        pos_x=SPRITE_SIZE * (15 + i),
        pos_y=SPRITE_SIZE * 9,
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i in range(1, 3)
}

POWER_UPS = {
    power_up: get_object_position_and_size(
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
    score: get_object_position_and_size(
        pos_x=(SPRITE_SIZE * (17 + i)),
        pos_y=(SPRITE_SIZE * 10),
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i, score in enumerate(['100', '200', '300', '400', '500'], 1)
}

FLAGS = {
    flag: get_object_position_and_size(
        pos_x=(SPRITE_SIZE * (18 + i)),
        pos_y=(SPRITE_SIZE * 2),
        width=SPRITE_SIZE,
        height=SPRITE_SIZE
    )
    for i, flag in enumerate(['Phoenix_Alive', 'Phoenix_Destroyed'], 1)
}

EXPLOSIONS = {
    f'explode_{i}': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * ((15 + i) if i < 5 else 21)),
        pos_y=SPRITE_SIZE * 8,
        width=SPRITE_SIZE if i < 4 else (SPRITE_SIZE * 2),
        height=SPRITE_SIZE if i < 4 else (SPRITE_SIZE * 2)
    )
    for i in range(1, 6)
}

BULLETS = {
    direction: get_object_position_and_size(
        pos_x=(
            (
                (SPRITE_SIZE * 20)
                if direction == 'Up'
                else (SPRITE_SIZE * 21)
            )
            if direction in ['Up', 'Down']
            else (
                (SPRITE_SIZE * 20) + 8
                if direction == 'Left'
                else (SPRITE_SIZE * 21) + 8
            )
        ),
        pos_y=(SPRITE_SIZE * 6) + 4,
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    )
    for direction in ['Up', 'Left', 'Down', 'Right']
}

MAP_TILES = {
    'bricks': {
        'small': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 16),
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        ),
        'small_right': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 16) + 12,
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 4),
            height=round(SPRITE_SIZE / 2)
        ),
        'small_bottom': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 17),
            pos_y=(SPRITE_SIZE * 4) + 4,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 4)
        ),
        'small_left': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 17) + 8,
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 4),
            height=round(SPRITE_SIZE / 2)
        ),
        'small_top': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 18),
            pos_y=(SPRITE_SIZE * 4),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 4)
        )
    },
    'steel': {
        'small': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 16),
            pos_y=(SPRITE_SIZE * 4) + 8,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        )
    },
    'forest': {
        'small': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 16) + 8,
            pos_y=(SPRITE_SIZE * 4) + 8,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        )
    },
    'ice': {
        'small': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 17),
            pos_y=(SPRITE_SIZE * 4) + 8,
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        )
    },
    'water': {
        'small_1': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 16) + 8,
            pos_y=(SPRITE_SIZE * 5),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        ),
        'small_2': get_object_position_and_size(
            pos_x=(SPRITE_SIZE * 17),
            pos_y=(SPRITE_SIZE * 5),
            width=round(SPRITE_SIZE / 2),
            height=round(SPRITE_SIZE / 2)
        ),
    }
}

HUD_INFO = {
    'stage': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 20) + 8,
        pos_y=(SPRITE_SIZE * 11),
        width=(SPRITE_SIZE // 2) * 5,
        height=(SPRITE_SIZE // 2)
    ),
    'num_0': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 20) + 8,
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_1': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 21),
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_2': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 21) + 8,
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_3': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 22),
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_4': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 22) + 8,
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_5': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 20) + 8,
        pos_y=(SPRITE_SIZE * 12),
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_6': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 21),
        pos_y=(SPRITE_SIZE * 12),
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_7': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 21) + 8,
        pos_y=(SPRITE_SIZE * 12),
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_8': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 22),
        pos_y=(SPRITE_SIZE * 12),
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'num_9': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 22) + 8,
        pos_y=(SPRITE_SIZE * 12),
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'life': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 20),
        pos_y=(SPRITE_SIZE * 12),
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    ),
    'info_panel': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 23),
        pos_y=(SPRITE_SIZE * 0),
        width=(SPRITE_SIZE * 2),
        height=(SPRITE_SIZE * 15)
    ),
    'grey_square': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 23),
        pos_y=(SPRITE_SIZE * 0),
        width=(SPRITE_SIZE // 2),
        height=(SPRITE_SIZE // 2)
    )
}

NUMBERS = {
    0: get_object_position_and_size(
        pos_x=0,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    1: get_object_position_and_size(
        pos_x=8,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    2: get_object_position_and_size(
        pos_x=16,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    3: get_object_position_and_size(
        pos_x=24,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    4: get_object_position_and_size(
        pos_x=32,
        pos_y=0,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    5: get_object_position_and_size(
        pos_x=0,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    6: get_object_position_and_size(
        pos_x=8,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    7: get_object_position_and_size(
        pos_x=16,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    8: get_object_position_and_size(
        pos_x=24,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    ),
    9: get_object_position_and_size(
        pos_x=32,
        pos_y=8,
        width=SPRITE_SIZE // 2,
        height=SPRITE_SIZE // 2
    )
}

CONTEXT = {
    'pause': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 18),
        pos_y=(SPRITE_SIZE * 11),
        width=round((SPRITE_SIZE / 2) * 5),
        height=round(SPRITE_SIZE / 2)
    ),
    'game_over': get_object_position_and_size(
        pos_x=(SPRITE_SIZE * 18),
        pos_y=(SPRITE_SIZE * 11) + 8,
        width=(SPRITE_SIZE * 2),
        height=SPRITE_SIZE
    )
}

# Tile numeric identificators (defined by Harry, not me!) for encoding
# and decoding CSV files for levels
ID_BRICK = 432
ID_STEEL = 482
ID_FOREST = 483
ID_ICE = 484
ID_WATER = 533
ID_FLAG = 999
