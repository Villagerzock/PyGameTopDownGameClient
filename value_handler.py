from typing import Callable

import scene_handler
from better_math import Vector2i
from pygame_scene import PyGameScene


class TileType:
    def __init__(self, data : dict = {}):
        self.data = data
    def get_data(self,key : str):
        return self.data.get(key) if self.data.get(key) is not None else ""
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
        if isinstance(self.tiles[int(index)], int):
            return self.tiles[int(index)]
        else:
            return self.tiles[int(index)][0]
    def get_data(self,index):
        if isinstance(self.tiles[int(index)], int):
            return {}
        else:
            return self.tiles[int(index)][1]



auth_token : str = ""
username : str = ""
chat : list[tuple[int, str]] = []
server_data : list[tuple[str, int | None, int | None, str | None]] = []
tile_world_type = None
open_screen: Screen = None


tile_types : dict[str, type[TileType]] = {}
