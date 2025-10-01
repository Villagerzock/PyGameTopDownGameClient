from typing import Callable

import scene_handler
from better_math import Vector2i
from pygame_scene import PyGameScene


class TileType:
    def on_player_enter(self):
        pass
    def on_player_leave(self):
        pass
    def get_values(self) -> dict[str, tuple[type[str | int | bool]]]:
        return {}

class Screen(PyGameScene):
    def close(self):
        global open_screen
        open_screen = None
        scene_handler.current_scene.update()

class TileChunk:
    SIZE = 32
    def __init__(self, chunks=None):
        if chunks is None:
            chunks = [-1] * (self.SIZE * self.SIZE)
        self.tiles: list[int | tuple[int, dict]] = chunks
        if len(self.tiles) < self.SIZE * self.SIZE:
            self.tiles += [-1] * (self.SIZE * self.SIZE - len(self.tiles))
    def get_type(self, index):
        if isinstance(self.tiles[index], int):
            return self.tiles[index]
        else:
            return self.tiles[index][0]



auth_token : str = ""
username : str = ""
chat : list[tuple[int, str]] = []
server_data : list[tuple[str, int | None, int | None, str | None]] = []
tile_world_type = None
open_screen: Screen = None
def change_dimension(new_dimension, spawn_point : Vector2i | None = None):
    if tile_world_type is None:
        return
    if isinstance(scene_handler.current_scene, tile_world_type):
        pos = spawn_point if spawn_point is not None else scene_handler.current_scene.position
        scene_handler.current_scene = tile_world_type()

tile_types : dict[str, type[TileType]] = {}
