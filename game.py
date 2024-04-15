import random

import pygame

import game_config as gc
from game_hud import GameHUD
from characters import Tank, PlayerTank


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
            'Bullets': pygame.sprite.Group()
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

        for dict_key in self.groups.keys():
            for item in self.groups[dict_key]:
                item.update()

    def draw(self, window: pygame.Surface) -> None:
        """
        Draws the given window object on the screen.
        """
        self.hud.draw(window)

        # if self.is_player_1_active:
        #     self.player_1.draw(window)

        # if self.is_player_2_active:
        #     self.player_2.draw(window)

        # No DRY!! update and draw method share this same snippet
        for dict_key in self.groups.keys():
            for item in self.groups[dict_key]:
                item.draw(window)

    def create_new_stage(self):
        """
        Retrieves the specific level data.
        """
        self.current_level_data = self.data.level_data[self.level_num - 1]
        # self.enemies = random.choice([16, 17, 18, 19, 20])
        self.enemies = 5
        self.enemies_killed = self.enemies
        self.load_level_data(self.current_level_data)
        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0

        if self.is_player_1_active:
            self.player_1.spawn_on_new_stage(gc.PLAYER_1_POS)

    def load_level_data(self, level):
        """
        Decodes the level data found in its CSV file.
        """
        self.grid = []
        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                pos = (
                    gc.SCREEN_BORDER_LEFT + (j * gc.IMAGE_SIZE // 2),
                    gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE // 2)
                )
                if int(tile) < 0:
                    line.append(' ')
                elif int(tile) == gc.ID_BRICK:
                    line.append(f'{tile}')
                elif int(tile) == gc.ID_STEEL:
                    line.append(f'{tile}')
                elif int(tile) == gc.ID_FOREST:
                    line.append(f'{tile}')
                elif int(tile) == gc.ID_ICE:
                    line.append(f'{tile}')
                elif int(tile) == gc.ID_WATER:
                    line.append(f'{tile}')
                elif int(tile) == gc.ID_FLAG:
                    line.append(f'{tile}')

            self.grid.append(line)

        for row in self.grid:
            print(row)  # dbg

    def generate_spawn_queue(self):
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
