import pygame
import os
import csv

from pathlib import Path


class LevelData:
    """
    Represents the object which manages the actual level data for the
    game or the level editor.
    """

    def __init__(self) -> None:
        self.level_data = self.load()

    def load(self) -> list:
        game_stages = []
        for stage in os.listdir('levels'):
            level_data = [[] for i in range(27)]
            with open(f'levels/{stage}', newline='') as f:
                reader = csv.reader(f, delimiter=',')
                for i, row in enumerate(reader):
                    for j, tile in enumerate(row):
                        level_data[i].append(int(tile))
            game_stages.append(level_data)

        return game_stages

    def save(self, level_data: list) -> None:
        """
        Stores the level created in the level editor as a CSV file.
        """
        self._check_level_directory()

        data_length: int = len(level_data)
        for i in range(data_length):
            # Create two digit number in str format
            num = str(i + 1) if len(str(i + 1)) > 1 else '0' + str(i + 1)
            path = Path(
                os.getcwd(),
                'levels',
                f'BattleCityLevel{num}.csv'
            )
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                for row in level_data[i]:
                    writer.writerow(row)

    def _check_level_directory(self) -> None:
        """
        Utility method which creates a "levels" folder if such folder is
        not found.
        """
        levels_dir = Path(__file__).parent / 'levels'
        if not levels_dir.exists():
            levels_dir.mkdir()
