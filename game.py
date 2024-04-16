import random

import pygame

import game_config as gc
from game_hud import GameHUD
from characters import Tank, PlayerTank
from tile import BrickTile


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
            'All_Tanks': pygame.sprite.Group(),
            'Player_Tanks': pygame.sprite.Group(),
            'Bullets': pygame.sprite.Group(),
            'Destructable_Tiles': pygame.sprite.Group()
        }

        # Player attributes
        self.is_player_1_active = is_player_1_active
        self.is_player_2_active = is_player_2_active

        # Game HUD
        self.hud = GameHUD(self, self.assets)

        # Level information
        self.level_num: int = 1
        self.data = self.main.levels

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

        # Game active or game over
        self.is_active: bool = True

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
                    if self.player_1.active:
                        self.player_1.shoot()

                # dbg
                if event.key == pygame.K_RCTRL:
                    if self.player_2.active:
                        self.player_2.shoot()

                # dbg
                if event.key == pygame.K_RETURN:
                    Tank(
                        self,
                        self.assets,
                        self.groups,
                        (400, 400),
                        'Down',
                    )
                    # self.enemies -= 1

    def update(self) -> None:
        self.hud.update()

        # if self.is_player_1_active:
        #     self.player_1.update()

        # if self.is_player_2_active:
        #     self.player_2.update()

        for k in self.groups.keys():
            if k == 'Player_Tanks':
                continue
            for item in self.groups[k]:
                item.update()

        self.spawn_enemy_tanks()

    def draw(self, window: pygame.Surface) -> None:
        """
        Draws the given window object on the screen.
        """
        self.hud.draw(window)

        # if self.is_player_1_active:
        #     self.player_1.draw(window)

        # if self.is_player_2_active:
        #     self.player_2.draw(window)

        for k in self.groups.keys():
            for item in self.groups[k]:
                item.draw(window)

    def create_new_stage(self) -> None:
        self._reset_sprite_groups()

        self.current_level_data = self.data.level_data[self.level_num - 1]
        # self.enemies = random.choice([16, 17, 18, 19, 20])
        self.enemies = 5
        self.enemies_killed = self.enemies
        self.load_level_data(self.current_level_data)
        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0
        print(self.spawn_queue)  # dbg

        if self.is_player_1_active:
            self.player_1.spawn_on_new_stage(gc.PLAYER_1_POS)
        if self.is_player_2_active:
            self.player_2.spawn_on_new_stage(gc.PLAYER_2_POS)

    def load_level_data(self, level) -> None:
        """
        Decodes the level data found in its CSV file.
        """
        tile_mapping = [
            gc.ID_BRICK,
            gc.ID_STEEL,
            gc.ID_FOREST,
            gc.ID_ICE,
            gc.ID_WATER,
            gc.ID_FLAG
        ]
        self.grid = []
        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                pos = (
                    gc.SCREEN_BORDER_LEFT + (j * gc.IMAGE_SIZE // 2),
                    gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE // 2)
                )
                tile_id = int(tile)

                if tile_id < 0:
                    line.append(' ')
                # elif tile_id in tile_mapping:
                #     line.append(tile_id)

                elif tile_id == gc.ID_BRICK:
                    line.append(f'{tile}')
                    map_tile = BrickTile(
                        pos,
                        self.groups['Destructable_Tiles'],
                        self.assets.brick_tiles
                    )
                elif tile_id == gc.ID_STEEL:
                    line.append(f'{tile}')
                elif tile_id == gc.ID_FOREST:
                    line.append(f'{tile}')
                elif tile_id == gc.ID_ICE:
                    line.append(f'{tile}')
                elif tile_id == gc.ID_WATER:
                    line.append(f'{tile}')
                elif tile_id == gc.ID_FLAG:
                    line.append(f'{tile}')

            self.grid.append(line)

        # for row in self.grid:
        #     print(row)  # dbg

    def generate_spawn_queue(self) -> None:
        """
        Generates a list of tanks that will be spawning during the game.
        """
        self.spawn_queue_ratios = gc.TANK_SPAWN_QUEUE[
            f'queue_{str((self.level_num % 36) // 3)}'
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
            tank_level = gc.TANK_SPAWN_CRITERIA[
                self.spawn_queue[
                    self.spawn_queue_index % len(self.spawn_queue)
                ]
            ]['image']
            Tank(
                self,
                self.assets,
                self.groups,
                position,
                'Down',
                'Silver',
                tank_level,
                True
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
            if k == 'Player_Tanks':
                continue
            v.empty()
