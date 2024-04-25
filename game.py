import random

import pygame
from pygame.surface import Surface

import game_config as gc
from game_hud import GameHUD
from characters import PlayerTank, EnemyTank, SpecialTank
from tile import BrickTile, SteelTile, ForestTile, IceTile, WaterTile
from fade_animation import Fade
from score_screen import ScoreScreen


class Game:
    """
    The main Game object when playing.

    NOTE: The assets are passed here through the Main object, then the
    Game object can use those assets as itself, and when it pleases,
    it can reach one of those assets and use them.
    """

    def __init__(
            self,
            main,
            assets,
            is_player_1_active: bool = True,
            is_player_2_active: bool = False
            ) -> None:

        # Important files
        self.main = main
        self.assets = assets

        # Object groups
        self.groups = {
            'ice_tiles': pygame.sprite.Group(),
            'water_tiles': pygame.sprite.Group(),
            'all_tanks': pygame.sprite.Group(),
            'player_tanks': pygame.sprite.Group(),
            'bullets': pygame.sprite.Group(),
            'destructable_tiles': pygame.sprite.Group(),
            'impassable_tiles': pygame.sprite.Group(),
            'explosion': pygame.sprite.Group(),
            'forest_tiles': pygame.sprite.Group(),
            'power_ups': pygame.sprite.Group()
        }

        # Player attributes
        self.is_player_1_active = is_player_1_active
        self.player_1_score: int = 0
        self.is_player_2_active = is_player_2_active
        self.player_2_score: int = 0
        self.top_score: int = 20_000

        # Game HUD
        self.hud = GameHUD(self, self.assets)

        # Level information
        self.level_num: int = 1
        self.is_level_complete = False
        self.level_transition_timer = None  # mehtod to be dev soon!
        self.data = self.main.levels

        # Level fade
        self.fade = Fade(self, self.assets, 10)

        # Stage score screen
        self.score_screen = ScoreScreen(self, self.assets)

        # Player objects
        if self.is_player_1_active:
            self.player_1 = PlayerTank(
                self,
                self.assets,
                self.groups,
                position=gc.PLAYER_1_POS,
                direction='Up',
                color='Gold',
            )

        if self.is_player_2_active:
            self.player_2 = PlayerTank(
                self,
                self.assets,
                self.groups,
                position=gc.PLAYER_2_POS,
                direction='Up',
                color='Green',
                tank_level=1
            )

        # Number of enemy tanks
        self.enemies: int = 20
        self.enemy_tank_spawn_timer: int = gc.TANK_SPAWNING_TIME
        self.enemy_spawn_positions: list[tuple[int, int]] = [
            gc.ENEMY_POS_1, gc.ENEMY_POS_2, gc.ENEMY_POS_3
        ]

        # Load the stage
        self.create_new_stage()

        # Fortify power up
        self.is_base_fortified: bool = False
        self.fortify_timer: int = pygame.time.get_ticks()

        # Game active or game over
        self.is_active: bool = True
        self.game_on: bool = False

    def input(self) -> None:
        """
        Handles input events for the game when it's running.
        """
        key_pressed = pygame.key.get_pressed()

        if self.is_player_1_active:
            self.player_1.input(key_pressed)

        if self.is_player_2_active:
            self.player_2.input(key_pressed)

        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            # Keyboard shortcut for quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False

                # dbg
                if event.key == pygame.K_SPACE:
                    if self.player_1.is_active:
                        self.player_1.shoot()

                # dbg
                if event.key == pygame.K_RCTRL:
                    if self.player_2.is_active:
                        self.player_2.shoot()

    def update(self) -> None:
        self.hud.update()

        if self.fade.is_fade_active:
            self.fade.update()
            if not self.fade.is_fade_active:
                for tank in self.groups['all_tanks']:
                    tank.spawn_timer = pygame.time.get_ticks()
            return

        if self.is_base_fortified:
            if pygame.time.get_ticks() - self.fortify_timer >= 10_000:
                self.apply_fortify(start=False, end=True)
                self.is_base_fortified = False

        for k in self.groups.keys():
            if k == 'player_tanks':
                continue
            for item in self.groups[k]:
                item.update()

        self.spawn_enemy_tanks()

        if self.enemies_killed <= 0 and not self.level_complete:
            self.level_complete = True
            self.level_transition_timer = pygame.time.get_ticks()

        if self.level_complete:
            """
            NOTE: time_buffer is the time between the last enemy tank
            being killed and the true end of the level. That's usually
            about 2 or 3 seconds in the original game. If the last tank
            had a power up and it was nearby, the buffer allows the
            player to catch that power up before the level truly ends!
            """
            time_buffer = pygame.time.get_ticks() - self.level_transition_timer
            if time_buffer >= gc.TRANSITION_TIMER:
                self.create_stage_transition()
                # self.level_num += 1
                # self.create_new_stage()

    def draw(self, window: Surface) -> None:
        """
        Draws the given window object on the screen.
        """
        self.hud.draw(window)

        if self.score_screen.is_active:
            self.score_screen.draw(window)
            return

        for k in self.groups.keys():
            if k == 'impassable_tiles':
                continue  # lets bullets be drawn above water!
            are_there_tanks: bool = k == 'all_tanks' or k == 'player_tanks'
            if self.fade.is_fade_active and are_there_tanks:
                continue
            for item in self.groups[k]:
                item.draw(window)

        if self.fade.is_fade_active:
            self.fade.draw(window)

    def create_stage_transition(self):
        if not self.score_screen.is_active:
            self.score_screen.timer = pygame.time.get_ticks()
            if self.is_player_1_active:
                self.score_screen.player_1_score = self.player_1_score
                self.score_screen.player_1_enemies_killed = sorted(
                    self.player_1.scores
                )
            if self.is_player_2_active:
                self.score_screen.player_2_score = self.player_2_score
                self.score_screen.player_2_enemies_killed = sorted(
                    self.player_2.scores
                )
            self.score_screen.update_basic_info(self.top_score, self.level_num)
        self.score_screen.is_active = True
        self.score_screen.update()

    def change_level(self, player_1_score, player_2_score):
        self.level_num += 1
        # We don't want our number of stages to surpass the actual list!
        self.level_num = self.level_num % len(self.data.level_data)
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        self.create_new_stage()

    def create_new_stage(self) -> None:
        self._reset_sprite_groups()

        self.current_level_data = self.data.level_data[self.level_num - 1]
        self.enemies = random.choice([16, 17, 18, 19, 20])
        self.enemies = 20  # remember if you edit: 20 is the standard
        self.enemies_killed = self.enemies

        self.load_level_data(self.current_level_data)
        self.level_complete = False

        self.fade.level = self.level_num
        self.fade.stage_image = self.fade.create_stage_image()
        self.fade.is_fade_active = True

        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0

        if self.is_player_1_active:
            self.player_1.spawn_on_new_stage(gc.PLAYER_1_POS)
        if self.is_player_2_active:
            self.player_2.spawn_on_new_stage(gc.PLAYER_2_POS)

    def load_level_data(self, level) -> None:
        """
        Decodes the level data found in its CSV file.
        """
        self.grid = []
        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                position = (
                    gc.SCREEN_BORDER_LEFT + (j * gc.IMAGE_SIZE // 2),
                    gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE // 2)
                )
                tile_id = int(tile)

                if tile_id < 0:
                    line.append(' ')
                elif tile_id == gc.ID_BRICK:
                    line.append(f'{tile}')
                    map_tile = BrickTile(
                        position,
                        self.groups['destructable_tiles'],
                        self.assets.brick_tiles
                    )
                    self.groups['impassable_tiles'].add(map_tile)
                elif tile_id == gc.ID_STEEL:
                    line.append(f'{tile}')
                    map_tile = SteelTile(
                        position,
                        self.groups['destructable_tiles'],
                        self.assets.steel_tiles
                    )
                    self.groups['impassable_tiles'].add(map_tile)
                elif tile_id == gc.ID_FOREST:
                    line.append(f'{tile}')
                    map_tile = ForestTile(
                        position,
                        self.groups['forest_tiles'],
                        self.assets.forest_tiles
                    )
                elif tile_id == gc.ID_ICE:
                    line.append(f'{tile}')
                    map_tile = IceTile(
                        position,
                        self.groups['ice_tiles'],
                        self.assets.ice_tiles
                    )
                elif tile_id == gc.ID_WATER:
                    line.append(f'{tile}')
                    map_tile = WaterTile(
                        position,
                        self.groups['water_tiles'],
                        self.assets.water_tiles
                    )
                    self.groups['impassable_tiles'].add(map_tile)
                elif tile_id == gc.ID_FLAG:
                    line.append(f'{tile}')

            self.grid.append(line)

    def generate_spawn_queue(self) -> None:
        """
        Generates a list of tanks that will be spawning during the game.
        """
        self.spawn_queue_ratios = gc.TANK_SPAWN_QUEUE[
            f'queue_{str((self.level_num - 1 % 36) // 3)}'
        ]
        self.spawn_queue = []

        for lvl, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f'level_{lvl}')
        random.shuffle(self.spawn_queue)

    def spawn_enemy_tanks(self) -> None:
        if self.enemies == 0:
            return

        spawn_time = pygame.time.get_ticks() - self.enemy_tank_spawn_timer
        if spawn_time >= gc.TANK_SPAWNING_TIME:
            position = self.enemy_spawn_positions[self.spawn_pos_index % 3]
            tank_level = gc.TANK_CRITERIA[
                self.spawn_queue[
                    self.spawn_queue_index % len(self.spawn_queue)
                ]
            ]['image']
            special_tank: int = random.randint(1, len(self.spawn_queue))
            if special_tank == self.spawn_queue_index:
                SpecialTank(
                    self,
                    self.assets,
                    self.groups,
                    position,
                    'Down',
                    'Silver',
                    tank_level
                )
            else:
                EnemyTank(
                    self,
                    self.assets,
                    self.groups,
                    position,
                    'Down',
                    'Silver',
                    tank_level
                )
            self._reset_enemy_tank_spawn_timer()

    def _reset_enemy_tank_spawn_timer(self) -> None:
        """
        Utility method for cleaning the spawn_enemy_tanks() original
        code. It just do what the function name says. :P
        """
        self.enemy_tank_spawn_timer = pygame.time.get_ticks()
        self.spawn_pos_index += 1
        self.spawn_queue_index += 1
        self.enemies -= 1

    def _reset_sprite_groups(self) -> None:
        """
        Utility method for cleaning the create_new_stage() original
        code. It just resets the various sprite groups back to zero.
        """
        for k, v in self.groups.items():
            if k == 'player_tanks':
                continue
            v.empty()

    def apply_fortify(self, *, start: bool = True, end: bool = False) -> None:
        """
        As soon as the fortify power up is catched, this applies it to
        the Phoenix base.
        """
        x_offset, y_offset = (gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP)
        half_img_size: int = gc.IMAGE_SIZE // 2
        positions: list[tuple[int, int]] = [
            (
                x_offset + half_img_size * 11,
                y_offset + half_img_size * 25
            ),
            (
                x_offset + half_img_size * 11,
                y_offset + half_img_size * 24
            ),
            (
                x_offset + half_img_size * 11,
                y_offset + half_img_size * 23
            ),
            (
                x_offset + half_img_size * 12,
                y_offset + half_img_size * 23
            ),
            (
                x_offset + half_img_size * 13,
                y_offset + half_img_size * 23
            ),
            (
                x_offset + half_img_size * 14,
                y_offset + half_img_size * 23
            ),
            (
                x_offset + half_img_size * 14,
                y_offset + half_img_size * 24
            ),
            (
                x_offset + half_img_size * 14,
                y_offset + half_img_size * 25
            ),
        ]
        if start:
            for position in positions:
                pos_rect = pygame.Rect(
                    position[0],
                    position[1],
                    half_img_size,
                    half_img_size
                )
                for rectangle in self.groups['impassable_tiles']:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()
                map_tile = SteelTile(
                    position,
                    self.groups['destructable_tiles'],
                    self.assets.steel_tiles
                )
                self.groups['impassable_tiles'].add(map_tile)
        elif end:
            for position in positions:
                pos_rect = pygame.Rect(
                    position[0],
                    position[1],
                    half_img_size,
                    half_img_size
                )
                for rectangle in self.groups['impassable_tiles']:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()
                map_tile = BrickTile(
                    position,
                    self.groups['destructable_tiles'],
                    self.assets.brick_tiles
                )
                self.groups['impassable_tiles'].add(map_tile)
