"""
Custom module for better type hints in the code, based on the project
classes, in order to improve readability.

As with my utilities.py module, this is made by me and it's not part of
the course!
"""


from typing import Type

import main
import game_assets
import game_hud
import characters


Main = Type[main.Main]
Assets = Type[game_assets.GameAssets]
GameHUD = Type[game_hud.GameHUD]
Tank = Type[characters.Tank]
PlayerTank = Type[characters.PlayerTank]
