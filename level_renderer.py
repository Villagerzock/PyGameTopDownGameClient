import json
import math
import os
import struct
from collections.abc import dict_items

import draw_context
import pygame
import scene_handler
from better_math import Vector2i
from elements.py_button import Button, TextureButton
from elements.text import TextEdit

from pygame.math import clamp
from pygame_scene import PyGameScene

import custom_renderer
import online_handler
import screens
import value_handler
from custom_elements import EditorTileOverlay
from tile_types import DoorType
from value_handler import TileChunk

tiles : list[dict[str,str | list[bool]]] = [{'texture': 'Overworld_Tileset_00_00'}, {'texture': 'Overworld_Tileset_00_01'}, {'texture': 'Overworld_Tileset_00_02'}, {'texture': 'Overworld_Tileset_00_03'}, {'texture': 'Overworld_Tileset_00_04'}, {'texture': 'Overworld_Tileset_00_05'}, {'texture': 'Overworld_Tileset_00_06'}, {'texture': 'Overworld_Tileset_00_07'}, {'texture': 'Overworld_Tileset_00_08'}, {'texture': 'Overworld_Tileset_00_09'}, {'texture': 'Overworld_Tileset_00_10'}, {'texture': 'Overworld_Tileset_00_11'}, {'texture': 'Overworld_Tileset_00_12'}, {'texture': 'Overworld_Tileset_00_13'}, {'texture': 'Overworld_Tileset_00_14'}, {'texture': 'Overworld_Tileset_00_15'}, {'texture': 'Overworld_Tileset_00_16'}, {'texture': 'Overworld_Tileset_00_17'}, {'texture': 'Overworld_Tileset_01_00'}, {'texture': 'Overworld_Tileset_01_01'}, {'texture': 'Overworld_Tileset_01_02'}, {'texture': 'Overworld_Tileset_01_03'}, {'texture': 'Overworld_Tileset_01_04'}, {'texture': 'Overworld_Tileset_01_05'}, {'texture': 'Overworld_Tileset_01_06'}, {'texture': 'Overworld_Tileset_01_07'}, {'texture': 'Overworld_Tileset_01_08'}, {'texture': 'Overworld_Tileset_01_09'}, {'texture': 'Overworld_Tileset_01_10'}, {'texture': 'Overworld_Tileset_01_11'}, {'texture': 'Overworld_Tileset_01_12'}, {'texture': 'Overworld_Tileset_01_13'}, {'texture': 'Overworld_Tileset_01_14'}, {'texture': 'Overworld_Tileset_01_15'}, {'texture': 'Overworld_Tileset_01_16'}, {'texture': 'Overworld_Tileset_01_17'}, {'texture': 'Overworld_Tileset_02_00'}, {'texture': 'Overworld_Tileset_02_01'}, {'texture': 'Overworld_Tileset_02_02'}, {'texture': 'Overworld_Tileset_02_03'}, {'texture': 'Overworld_Tileset_02_04'}, {'texture': 'Overworld_Tileset_02_05'}, {'texture': 'Overworld_Tileset_02_06'}, {'texture': 'Overworld_Tileset_02_07'}, {'texture': 'Overworld_Tileset_02_08'}, {'texture': 'Overworld_Tileset_02_09'}, {'texture': 'Overworld_Tileset_02_10'}, {'texture': 'Overworld_Tileset_02_11'}, {'texture': 'Overworld_Tileset_02_12'}, {'texture': 'Overworld_Tileset_02_13'}, {'texture': 'Overworld_Tileset_02_14'}, {'texture': 'Overworld_Tileset_02_15'}, {'texture': 'Overworld_Tileset_02_16'}, {'texture': 'Overworld_Tileset_02_17'}, {'texture': 'Overworld_Tileset_03_00'}, {'texture': 'Overworld_Tileset_03_01'}, {'texture': 'Overworld_Tileset_03_02'}, {'texture': 'Overworld_Tileset_03_03'}, {'texture': 'Overworld_Tileset_03_04'}, {'texture': 'Overworld_Tileset_03_05'}, {'texture': 'Overworld_Tileset_03_06'}, {'texture': 'Overworld_Tileset_03_07'}, {'texture': 'Overworld_Tileset_03_08'}, {'texture': 'Overworld_Tileset_03_09'}, {'texture': 'Overworld_Tileset_03_10'}, {'texture': 'Overworld_Tileset_03_11'}, {'texture': 'Overworld_Tileset_03_12'}, {'texture': 'Overworld_Tileset_03_13'}, {'texture': 'Overworld_Tileset_03_14'}, {'texture': 'Overworld_Tileset_03_15'}, {'texture': 'Overworld_Tileset_03_16'}, {'texture': 'Overworld_Tileset_03_17'}, {'texture': 'Overworld_Tileset_04_00'}, {'texture': 'Overworld_Tileset_04_01'}, {'texture': 'Overworld_Tileset_04_02'}, {'texture': 'Overworld_Tileset_04_03'}, {'texture': 'Overworld_Tileset_04_04'}, {'texture': 'Overworld_Tileset_04_05'}, {'texture': 'Overworld_Tileset_04_06'}, {'texture': 'Overworld_Tileset_04_07'}, {'texture': 'Overworld_Tileset_04_08'}, {'texture': 'Overworld_Tileset_04_09'}, {'texture': 'Overworld_Tileset_04_10'}, {'texture': 'Overworld_Tileset_04_11'}, {'texture': 'Overworld_Tileset_04_12'}, {'texture': 'Overworld_Tileset_04_13'}, {'texture': 'Overworld_Tileset_04_14'}, {'texture': 'Overworld_Tileset_04_15'}, {'texture': 'Overworld_Tileset_04_16'}, {'texture': 'Overworld_Tileset_04_17'}, {'texture': 'Overworld_Tileset_05_00'}, {'texture': 'Overworld_Tileset_05_01'}, {'texture': 'Overworld_Tileset_05_02'}, {'texture': 'Overworld_Tileset_05_03'}, {'texture': 'Overworld_Tileset_05_04'}, {'texture': 'Overworld_Tileset_05_05'}, {'texture': 'Overworld_Tileset_05_06'}, {'texture': 'Overworld_Tileset_05_07'}, {'texture': 'Overworld_Tileset_05_08'}, {'texture': 'Overworld_Tileset_05_09'}, {'texture': 'Overworld_Tileset_05_10'}, {'texture': 'Overworld_Tileset_05_11'}, {'texture': 'Overworld_Tileset_05_12'}, {'texture': 'Overworld_Tileset_05_13'}, {'texture': 'Overworld_Tileset_05_14'}, {'texture': 'Overworld_Tileset_05_15'}, {'texture': 'Overworld_Tileset_05_16'}, {'texture': 'Overworld_Tileset_05_17'}, {'texture': 'Overworld_Tileset_06_00'}, {'texture': 'Overworld_Tileset_06_01'}, {'texture': 'Overworld_Tileset_06_02'}, {'texture': 'Overworld_Tileset_06_03'}, {'texture': 'Overworld_Tileset_06_04'}, {'texture': 'Overworld_Tileset_06_05'}, {'texture': 'Overworld_Tileset_06_06'}, {'texture': 'Overworld_Tileset_06_07'}, {'texture': 'Overworld_Tileset_06_08'}, {'texture': 'Overworld_Tileset_06_09'}, {'texture': 'Overworld_Tileset_06_10'}, {'texture': 'Overworld_Tileset_06_11'}, {'texture': 'Overworld_Tileset_06_12'}, {'texture': 'Overworld_Tileset_06_13'}, {'texture': 'Overworld_Tileset_06_14'}, {'texture': 'Overworld_Tileset_06_15'}, {'texture': 'Overworld_Tileset_06_16'}, {'texture': 'Overworld_Tileset_06_17'}, {'texture': 'Overworld_Tileset_07_00'}, {'texture': 'Overworld_Tileset_07_01'}, {'texture': 'Overworld_Tileset_07_02'}, {'texture': 'Overworld_Tileset_07_03'}, {'texture': 'Overworld_Tileset_07_04'}, {'texture': 'Overworld_Tileset_07_05'}, {'texture': 'Overworld_Tileset_07_06'}, {'texture': 'Overworld_Tileset_07_07'}, {'texture': 'Overworld_Tileset_07_08'}, {'texture': 'Overworld_Tileset_07_09'}, {'texture': 'Overworld_Tileset_07_10'}, {'texture': 'Overworld_Tileset_07_11'}, {'texture': 'Overworld_Tileset_07_12'}, {'texture': 'Overworld_Tileset_07_13'}, {'texture': 'Overworld_Tileset_07_14'}, {'texture': 'Overworld_Tileset_07_15'}, {'texture': 'Overworld_Tileset_07_16'}, {'texture': 'Overworld_Tileset_07_17'}, {'texture': 'Overworld_Tileset_08_00'}, {'texture': 'Overworld_Tileset_08_01'}, {'texture': 'Overworld_Tileset_08_02'}, {'texture': 'Overworld_Tileset_08_03'}, {'texture': 'Overworld_Tileset_08_04'}, {'texture': 'Overworld_Tileset_08_05'}, {'texture': 'Overworld_Tileset_08_06'}, {'texture': 'Overworld_Tileset_08_07'}, {'texture': 'Overworld_Tileset_08_08'}, {'texture': 'Overworld_Tileset_08_09'}, {'texture': 'Overworld_Tileset_08_10'}, {'texture': 'Overworld_Tileset_08_11'}, {'texture': 'Overworld_Tileset_08_12'}, {'texture': 'Overworld_Tileset_08_13'}, {'texture': 'Overworld_Tileset_08_14'}, {'texture': 'Overworld_Tileset_08_15'}, {'texture': 'Overworld_Tileset_08_16'}, {'texture': 'Overworld_Tileset_08_17'}, {'texture': 'Overworld_Tileset_09_00'}, {'texture': 'Overworld_Tileset_09_01'}, {'texture': 'Overworld_Tileset_09_02'}, {'texture': 'Overworld_Tileset_09_03'}, {'texture': 'Overworld_Tileset_09_04'}, {'texture': 'Overworld_Tileset_09_05'}, {'texture': 'Overworld_Tileset_09_06'}, {'texture': 'Overworld_Tileset_09_07'}, {'texture': 'Overworld_Tileset_09_08'}, {'texture': 'Overworld_Tileset_09_09'}, {'texture': 'Overworld_Tileset_09_10'}, {'texture': 'Overworld_Tileset_09_11'}, {'texture': 'Overworld_Tileset_09_12'}, {'texture': 'Overworld_Tileset_09_13'}, {'texture': 'Overworld_Tileset_09_14'}, {'texture': 'Overworld_Tileset_09_15'}, {'texture': 'Overworld_Tileset_09_16'}, {'texture': 'Overworld_Tileset_09_17'}, {'texture': 'Overworld_Tileset_10_00'}, {'texture': 'Overworld_Tileset_10_01'}, {'texture': 'Overworld_Tileset_10_02'}, {'texture': 'Overworld_Tileset_10_03'}, {'texture': 'Overworld_Tileset_10_04'}, {'texture': 'Overworld_Tileset_10_05'}, {'texture': 'Overworld_Tileset_10_06'}, {'texture': 'Overworld_Tileset_10_07'}, {'texture': 'Overworld_Tileset_10_08'}, {'texture': 'Overworld_Tileset_10_09'}, {'texture': 'Overworld_Tileset_10_10'}, {'texture': 'Overworld_Tileset_10_11'}, {'texture': 'Overworld_Tileset_10_12'}, {'texture': 'Overworld_Tileset_10_13'}, {'texture': 'Overworld_Tileset_10_14'}, {'texture': 'Overworld_Tileset_10_15'}, {'texture': 'Overworld_Tileset_10_16'}, {'texture': 'Overworld_Tileset_10_17'}, {'texture': 'Overworld_Tileset_11_00'}, {'texture': 'Overworld_Tileset_11_01'}, {'texture': 'Overworld_Tileset_11_02'}, {'texture': 'Overworld_Tileset_11_03'}, {'texture': 'Overworld_Tileset_11_04'}, {'texture': 'Overworld_Tileset_11_05'}, {'texture': 'Overworld_Tileset_11_06'}, {'texture': 'Overworld_Tileset_11_07'}, {'texture': 'Overworld_Tileset_11_08'}, {'texture': 'Overworld_Tileset_11_09'}, {'texture': 'Overworld_Tileset_11_10'}, {'texture': 'Overworld_Tileset_11_11'}, {'texture': 'Overworld_Tileset_11_12'}, {'texture': 'Overworld_Tileset_11_13'}, {'texture': 'Overworld_Tileset_11_14'}, {'texture': 'Overworld_Tileset_11_15'}, {'texture': 'Overworld_Tileset_11_16'}, {'texture': 'Overworld_Tileset_11_17'}, {'texture': 'Overworld_Tileset_12_00'}, {'texture': 'Overworld_Tileset_12_01'}, {'texture': 'Overworld_Tileset_12_02'}, {'texture': 'Overworld_Tileset_12_03'}, {'texture': 'Overworld_Tileset_12_04'}, {'texture': 'Overworld_Tileset_12_05'}, {'texture': 'Overworld_Tileset_12_06'}, {'texture': 'Overworld_Tileset_12_07'}, {'texture': 'Overworld_Tileset_12_08'}, {'texture': 'Overworld_Tileset_12_09'}, {'texture': 'Overworld_Tileset_12_10'}, {'texture': 'Overworld_Tileset_12_11'}, {'texture': 'Overworld_Tileset_12_12'}, {'texture': 'Overworld_Tileset_12_13'}, {'texture': 'Overworld_Tileset_12_14'}, {'texture': 'Overworld_Tileset_12_15'}, {'texture': 'Overworld_Tileset_12_16'}, {'texture': 'Overworld_Tileset_12_17'}, {'texture': 'Dungeon_Tileset_00_00'}, {'texture': 'Dungeon_Tileset_00_01'}, {'texture': 'Dungeon_Tileset_00_02'}, {'texture': 'Dungeon_Tileset_00_03'}, {'texture': 'Dungeon_Tileset_00_04'}, {'texture': 'Dungeon_Tileset_00_05'}, {'texture': 'Dungeon_Tileset_00_06'}, {'texture': 'Dungeon_Tileset_00_07'}, {'texture': 'Dungeon_Tileset_00_08'}, {'texture': 'Dungeon_Tileset_00_09'}, {'texture': 'Dungeon_Tileset_00_10'}, {'texture': 'Dungeon_Tileset_00_11'}, {'texture': 'Dungeon_Tileset_01_00'}, {'texture': 'Dungeon_Tileset_01_01'}, {'texture': 'Dungeon_Tileset_01_02'}, {'texture': 'Dungeon_Tileset_01_03'}, {'texture': 'Dungeon_Tileset_01_04'}, {'texture': 'Dungeon_Tileset_01_05'}, {'texture': 'Dungeon_Tileset_01_06'}, {'texture': 'Dungeon_Tileset_01_07'}, {'texture': 'Dungeon_Tileset_01_08'}, {'texture': 'Dungeon_Tileset_01_09'}, {'texture': 'Dungeon_Tileset_01_10'}, {'texture': 'Dungeon_Tileset_01_11'}, {'texture': 'Dungeon_Tileset_02_00'}, {'texture': 'Dungeon_Tileset_02_01'}, {'texture': 'Dungeon_Tileset_02_02'}, {'texture': 'Dungeon_Tileset_02_03'}, {'texture': 'Dungeon_Tileset_02_04'}, {'texture': 'Dungeon_Tileset_02_05'}, {'texture': 'Dungeon_Tileset_02_06'}, {'texture': 'Dungeon_Tileset_02_07'}, {'texture': 'Dungeon_Tileset_02_08'}, {'texture': 'Dungeon_Tileset_02_09'}, {'texture': 'Dungeon_Tileset_02_10'}, {'texture': 'Dungeon_Tileset_02_11'}, {'texture': 'Dungeon_Tileset_03_00'}, {'texture': 'Dungeon_Tileset_03_01'}, {'texture': 'Dungeon_Tileset_03_02'}, {'texture': 'Dungeon_Tileset_03_03'}, {'texture': 'Dungeon_Tileset_03_04'}, {'texture': 'Dungeon_Tileset_03_05'}, {'texture': 'Dungeon_Tileset_03_06'}, {'texture': 'Dungeon_Tileset_03_07'}, {'texture': 'Dungeon_Tileset_03_08'}, {'texture': 'Dungeon_Tileset_03_09'}, {'texture': 'Dungeon_Tileset_03_10'}, {'texture': 'Dungeon_Tileset_03_11'}, {'texture': 'Dungeon_Tileset_04_00'}, {'texture': 'Dungeon_Tileset_04_01'}, {'texture': 'Dungeon_Tileset_04_02'}, {'texture': 'Dungeon_Tileset_04_03'}, {'texture': 'Dungeon_Tileset_04_04'}, {'texture': 'Dungeon_Tileset_04_05'}, {'texture': 'Dungeon_Tileset_04_06'}, {'texture': 'Dungeon_Tileset_04_07'}, {'texture': 'Dungeon_Tileset_04_08'}, {'texture': 'Dungeon_Tileset_04_09'}, {'texture': 'Dungeon_Tileset_04_10'}, {'texture': 'Dungeon_Tileset_04_11'}, {'texture': 'Dungeon_Tileset_05_00'}, {'texture': 'Dungeon_Tileset_05_01'}, {'texture': 'Dungeon_Tileset_05_02'}, {'texture': 'Dungeon_Tileset_05_03'}, {'texture': 'Dungeon_Tileset_05_04'}, {'texture': 'Dungeon_Tileset_05_05'}, {'texture': 'Dungeon_Tileset_05_06'}, {'texture': 'Dungeon_Tileset_05_07'}, {'texture': 'Dungeon_Tileset_05_08'}, {'texture': 'Dungeon_Tileset_05_09'}, {'texture': 'Dungeon_Tileset_05_10'}, {'texture': 'Dungeon_Tileset_05_11'}, {'texture': 'Dungeon_Tileset_06_00'}, {'texture': 'Dungeon_Tileset_06_01'}, {'texture': 'Dungeon_Tileset_06_02'}, {'texture': 'Dungeon_Tileset_06_03'}, {'texture': 'Dungeon_Tileset_06_04'}, {'texture': 'Dungeon_Tileset_06_05'}, {'texture': 'Dungeon_Tileset_06_06'}, {'texture': 'Dungeon_Tileset_06_07'}, {'texture': 'Dungeon_Tileset_06_08'}, {'texture': 'Dungeon_Tileset_06_09'}, {'texture': 'Dungeon_Tileset_06_10'}, {'texture': 'Dungeon_Tileset_06_11'}, {'texture': 'Dungeon_Tileset_07_00'}, {'texture': 'Dungeon_Tileset_07_01'}, {'texture': 'Dungeon_Tileset_07_02'}, {'texture': 'Dungeon_Tileset_07_03'}, {'texture': 'Dungeon_Tileset_07_04'}, {'texture': 'Dungeon_Tileset_07_05'}, {'texture': 'Dungeon_Tileset_07_06'}, {'texture': 'Dungeon_Tileset_07_07'}, {'texture': 'Dungeon_Tileset_07_08'}, {'texture': 'Dungeon_Tileset_07_09'}, {'texture': 'Dungeon_Tileset_07_10'}, {'texture': 'Dungeon_Tileset_07_11'}, {'texture': 'Dungeon_Tileset_08_00'}, {'texture': 'Dungeon_Tileset_08_01'}, {'texture': 'Dungeon_Tileset_08_02'}, {'texture': 'Dungeon_Tileset_08_03'}, {'texture': 'Dungeon_Tileset_08_04'}, {'texture': 'Dungeon_Tileset_08_05'}, {'texture': 'Dungeon_Tileset_08_06'}, {'texture': 'Dungeon_Tileset_08_07'}, {'texture': 'Dungeon_Tileset_08_08'}, {'texture': 'Dungeon_Tileset_08_09'}, {'texture': 'Dungeon_Tileset_08_10'}, {'texture': 'Dungeon_Tileset_08_11'}, {'texture': 'Dungeon_Tileset_09_00'}, {'texture': 'Dungeon_Tileset_09_01'}, {'texture': 'Dungeon_Tileset_09_02'}, {'texture': 'Dungeon_Tileset_09_03'}, {'texture': 'Dungeon_Tileset_09_04'}, {'texture': 'Dungeon_Tileset_09_05'}, {'texture': 'Dungeon_Tileset_09_06'}, {'texture': 'Dungeon_Tileset_09_07'}, {'texture': 'Dungeon_Tileset_09_08'}, {'texture': 'Dungeon_Tileset_09_09'}, {'texture': 'Dungeon_Tileset_09_10'}, {'texture': 'Dungeon_Tileset_09_11'}, {'texture': 'Dungeon_Tileset_10_00'}, {'texture': 'Dungeon_Tileset_10_01'}, {'texture': 'Dungeon_Tileset_10_02'}, {'texture': 'Dungeon_Tileset_10_03'}, {'texture': 'Dungeon_Tileset_10_04'}, {'texture': 'Dungeon_Tileset_10_05'}, {'texture': 'Dungeon_Tileset_10_06'}, {'texture': 'Dungeon_Tileset_10_07'}, {'texture': 'Dungeon_Tileset_10_08'}, {'texture': 'Dungeon_Tileset_10_09'}, {'texture': 'Dungeon_Tileset_10_10'}, {'texture': 'Dungeon_Tileset_10_11'}, {'texture': 'Dungeon_Tileset_11_00'}, {'texture': 'Dungeon_Tileset_11_01'}, {'texture': 'Dungeon_Tileset_11_02'}, {'texture': 'Dungeon_Tileset_11_03'}, {'texture': 'Dungeon_Tileset_11_04'}, {'texture': 'Dungeon_Tileset_11_05'}, {'texture': 'Dungeon_Tileset_11_06'}, {'texture': 'Dungeon_Tileset_11_07'}, {'texture': 'Dungeon_Tileset_11_08'}, {'texture': 'Dungeon_Tileset_11_09'}, {'texture': 'Dungeon_Tileset_11_10'}, {'texture': 'Dungeon_Tileset_11_11'}, {'texture': 'Dungeon_Tileset_12_00'}, {'texture': 'Dungeon_Tileset_12_01'}, {'texture': 'Dungeon_Tileset_12_02'}, {'texture': 'Dungeon_Tileset_12_03'}, {'texture': 'Dungeon_Tileset_12_04'}, {'texture': 'Dungeon_Tileset_12_05'}, {'texture': 'Dungeon_Tileset_12_06'}, {'texture': 'Dungeon_Tileset_12_07'}, {'texture': 'Dungeon_Tileset_12_08'}, {'texture': 'Dungeon_Tileset_12_09'}, {'texture': 'Dungeon_Tileset_12_10'}, {'texture': 'Dungeon_Tileset_12_11'}]

with open("tiles.json", "r", encoding="utf-8") as f:
    tiles = json.load(f)





class TileWorld(PyGameScene):
    def __init__(self, dim : str = "overworld"):
        self.skin = value_handler.skin
        self.dimension = dim
        self.floor_tile = "Overworld_Tileset_01_06"
        self.camera_rule = "move_free"
        value_handler.tile_types["door"] = DoorType
        if online_handler.id != "":
            self.initialize_packet()
        value_handler.tile_world_type = TileWorld
        self.chat_input = None
        self.editor_overlay = None
        self.save_button = None
        self.chunk_size = 32
        self.render_distance = 1
        self.load_world(f"{self.dimension}.json")
        value_handler.TileChunk.SIZE = self.chunk_size
        self.chat_input_text = ""
        super().__init__()

    texture_cache : dict[str,pygame.Surface] = {}
    def get_texture(self, name: str,prefix = "tiles/") -> pygame.Surface:
        texture = self.texture_cache.get(name)
        if texture is None:
            self.texture_cache[name] = pygame.transform.scale(pygame.image.load(prefix + name + ".png").convert_alpha(),(self.tile_size,self.tile_size))
            return self.texture_cache[name]
        return texture
    def initialize_packet(self):
        print(online_handler.id)
        online_handler.client.send_opcode(4,struct.pack("!I",len(online_handler.id.encode('utf-8'))) + online_handler.id.encode('utf-8') + struct.pack("!I",len(self.dimension.encode('utf-8'))) + self.dimension.encode('utf-8'))
    def save_world(self, name: str = "overworld.json") -> None:
        """
        Speichert alle Chunks nach ./dim/<name> im Format:
        {
          "chunks": [
            { "pos": [x, y], "tiles": [ ... 1024 ints ... ] },
            ...
          ]
        }
        """
        os.makedirs("./dim", exist_ok=True)
        path = os.path.join("dim", name)
        items : dict_items[tuple[tuple[int,int], TileChunk]] = self.chunks.items()
        chunk_items : list[tuple[tuple[int,int],TileChunk]] = []
        for item in items:
            print(item[1].tiles.count(-1))
            if item[1].tiles.count(-1) != (self.chunk_size * self.chunk_size):
                print(item[1].tiles.count(-1))
                chunk_items.append(item)
        data = {
            "meta":{
                "floor":self.floor_tile,
                "camera_rule":self.camera_rule,
                "chunk_size":self.chunk_size,
                "render_distance":self.render_distance,
            },
            "chunks": [
                {
                    "pos": [int(pos[0]), int(pos[1])],
                    "tiles": list(chunk.tiles)  # flache Liste mit 1024 Einträgen
                }
                for pos, chunk in chunk_items
            ]
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_world(self, name: str = "overworld.json") -> None:
        """
        Lädt Chunks aus ./dim/<name> und baut self.chunks neu auf.
        Nicht vorhandene Datei wird einfach ignoriert (kein Fehler).
        """
        path = os.path.join("dim", name)
        if not os.path.isfile(path):
            # Nichts zu laden – leise zurück
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Chunks zurück in Dict[(x, y)] -> TileChunk
        self.chunks = {}
        self.floor_tile = data.get("meta").get("floor") if data.get("meta") is not None else "Overworld_Tileset_01_06"
        self.camera_rule = data.get("meta").get("camera_rule") if data.get("meta") is not None else "move_free"
        self.chunk_size = data.get("meta").get("chunk_size") if data.get("meta") is not None else 32
        self.render_distance = data.get("meta").get("render_distance") if data.get("meta") is not None else 1
        for entry in data.get("chunks", []):
            pos = entry.get("pos", [0, 0])
            tiles = entry.get("tiles", [])
            # TileChunk kümmert sich ums Auffüllen, falls Liste kürzer ist
            chunk = TileChunk(tiles)
            self.chunks[(int(pos[0]), int(pos[1]))] = chunk
    is_select_mode = False
    selected : tuple[TileChunk,int] | None = None

    def get_position(self, position_offset : Vector2i = Vector2i(0,0), is_override : bool = False) -> Vector2i:
        print(self.position.x * (self.tile_size / 64.0))
        if is_override:
            return Vector2i(int((position_offset.x) * (self.tile_size / 64.0)),
                            int((position_offset.y) * (self.tile_size / 64.0)))
        return Vector2i(int((self.position.x + position_offset.x) * (self.tile_size / 64.0)),int((self.position.y + position_offset.y) * (self.tile_size / 64.0)))
    def update(self):
        global tiles
        super().update()
        if value_handler.open_screen is not None:
            value_handler.open_screen.update()
        png = pygame.image.load("textures/gui/cursor_normal.png").convert_alpha()
        hotspot = (12, 4)
        cursor = pygame.cursors.Cursor(hotspot, png)
        pygame.mouse.set_cursor(cursor)
        self.tile_size = min(scene_handler.camera_size.y,scene_handler.camera_size.x) // 16
        self.texture_cache.clear()
        self.camera_rect = pygame.Rect(self.get_position().x - (scene_handler.camera_size.x // 2), self.get_position().y - (scene_handler.camera_size.y // 2), scene_handler.camera_size.x,scene_handler.camera_size.y)
        self.camera_rect.center = (self.get_position().x, self.get_position().y)
        self.editor_overlay = EditorTileOverlay(pygame.Rect(scene_handler.camera_size.x - (self.tile_size * 6),0,(self.tile_size * 10),scene_handler.camera_size.y),tile_size=self.tile_size,tiles=tiles,scene=self)
        self.editor_overlay.visible = False
        self.drawables.append(
            self.editor_overlay
        )
        def toggle_edit_mode():
            print("Toggled Is Select Mode")
            self.is_select_mode = not self.is_select_mode
        def click_on_edit():
            print("Editing Data!")
            if self.selected is not None and tiles[self.selected[0].get_type(self.selected[1])].get("type") is not None:
                value_handler.open_screen = screens.ModifyTileScreen(value_handler.tile_types[tiles[self.selected[0].get_type(self.selected[1])]["type"]](self.selected[0].get_data(self.selected[1])),*self.selected)
        self.edit_button = TextureButton("textures/gui/pencil.png", (16,56),(32,32),toggle_edit_mode)
        self.edit_button.visible = False
        self.modify_button = TextureButton("textures/gui/edit.png", (48,56),(32,32),click_on_edit)
        self.modify_button.visible = False
        self.drawables.append(self.edit_button)
        self.drawables.append(self.modify_button)
        
        chat_input_rect = pygame.Rect(0,scene_handler.camera_size.y - 40,250,40)
        def chat_input_changed(new_text):
            self.chat_input_text = new_text
            return True
        self.chat_input = TextEdit(self.chat_input_text, "Enter Message...","arial",chat_input_rect,chat_input_changed)
        self.drawables.append(self.chat_input)
        self.save_button = Button("Save",(125,20),(250,40),pygame.font.SysFont("./font/Boxy-Bold.ttf",16),self.save_world, on_click_values=(f"{self.dimension}.json",))
        self.save_button.visible = False
        self.drawables.append(
            self.save_button
        )



    chunks : dict[tuple[int,int],TileChunk] = {
        (0,0):TileChunk(),
        (0,1):TileChunk(),
        (-1,0):TileChunk(),
        (1,1):TileChunk(),
    }

    def close(self):
        print("Closing...")
        payload = struct.pack("!I", len(online_handler.id)) + online_handler.id.encode("utf-8")
        online_handler.client.send_opcode(0x02, payload)


    camera_rect : pygame.Rect
    position : Vector2i = Vector2i(0, 0)
    tile_size = 64
    direction = 0
    animation = 0
    animation_tick = 0
    def toggle_editor(self):
        self.editor_overlay.visible = not self.editor_overlay.visible
        self.save_button.visible = not self.save_button.visible
        self.edit_button.visible = not self.edit_button.visible

    def get_animation_state(self, direction, animation, animationTick,skin_id : str = "female"):
        skin = "male" if skin_id == 0 else "female"
        match animation:
            case 0:
                return self.get_texture(f"Char{("" if skin_id == 0 else "2")}_idle_{self.get_dir_string(direction)}_00_{((animationTick // 5) % 6):02d}",prefix=f"textures/player/{skin}/")
            case 1:
                return self.get_texture(f"Char{("" if skin_id == 0 else "2")}_walk_{self.get_dir_string(direction)}_00_{((animationTick // 10) % 6):02d}",prefix=f"textures/player/{skin}/")
            case _:
                return self.get_texture(f"Char{("" if skin_id == 0 else "2")}_4_sides_00_{(direction % 4):02d}",prefix=f"textures/player/{skin}/")
    def get_dir_string(self,direction) -> str:
        match direction:
            case 0:
                return "down"
            case 1:
                return "right"
            case 2:
                return "up"
            case 3:
                return "left"
        return "down"

    def get_value(self, start_time):
        # aktuelle Zeit in Sekunden seit start_time
        t = (pygame.time.get_ticks() - start_time) / 1000.0

        if t <= 5.0:
            return 1.0
        elif t >= 7.0:
            return 0.0
        else:
            # Linearer Übergang von 1.0 -> 0.0 in 2 Sekunden
            return 1.0 - (t - 5.0) / 2.0
    inside_tiles_last_frame = []





    def render(self, surface: pygame.Surface, events):
        global tiles
        if self.selected is not None:
            print(tiles[self.selected[0].get_type(self.selected[1])].get("type"))
        if self.selected is not None and (tiles[self.selected[0].get_type(self.selected[1])].get("type") is not None):
            self.modify_button.visible = True
        else:
            self.modify_button.visible = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.toggle_editor()

                if event.key == 13:
                    if self.chat_input.is_focused():
                        print("Sending Chat Message...")
                        message = f"<{value_handler.username}> {self.chat_input_text}"
                        online_handler.client.send_opcode(0x03, struct.pack("!I", len(message)) + message.encode("utf-8"))
                        self.chat_input_text = ""
                        self.chat_input.text = ""
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()

        if scene_handler.delta > 1.0 / 30.0:
            pass
            #print("BAD PERFORMANCE")
        pygame.draw.rect(surface, (0,0,0), (0,0,scene_handler.camera_size.x,scene_handler.camera_size.y))
        speed_px_per_frame = 8.0
        if value_handler.open_screen is None:
            keys = pygame.key.get_pressed()
            dx = (1 if keys[pygame.K_d] else 0) - (1 if keys[pygame.K_a] else 0)
            dy = (1 if keys[pygame.K_s] else 0) - (1 if keys[pygame.K_w] else 0)

            length = math.hypot(dx, dy)
            if dx != 0:
                self.direction = (-dx + 1) + 1
            if dy != 0:
                self.direction = (-dy  + 1)
            if length > 0:
                self.animation = 1
                dx /= length
                dy /= length
                can_move_x = True
                can_move_y = True
                local_rect_x = pygame.Rect(0,0,self.tile_size // 2 + 2,self.tile_size)
                local_rect_x.center = (self.get_position(Vector2i((dx * speed_px_per_frame),0)).x, self.get_position().y)
                local_rect_y = pygame.Rect(0,0,self.tile_size // 2 + 2,self.tile_size)
                local_rect_y.center = (self.get_position().x, self.get_position(Vector2i(0, (dy * speed_px_per_frame))).y)
                local_rect_current = pygame.Rect(0,0,self.tile_size // 2 + 2,self.tile_size)
                local_rect_current.center = (self.get_position(Vector2i((dx * speed_px_per_frame), 0)).x, self.get_position(Vector2i(0, (dy * speed_px_per_frame))).y)
                for key in online_handler.online_players:
                    p = online_handler.online_players[key]
                    print(f"Player: {p.dimension} Self: {self.dimension}")
                    if p.dimension != self.dimension:
                        continue
                    online_player_pos = (((self.get_position(p.position,True) + -self.get_position(p.old_pos,True)) / 7.0) * p.tick) + self.get_position(p.old_pos,True)

                    pos = Vector2i(
                        clamp(online_player_pos.x, min(self.get_position(p.position,True).x, self.get_position(p.old_pos,True).x), max(self.get_position(p.position,True).x, self.get_position(p.old_pos,True).x)),
                        clamp(online_player_pos.y, min(self.get_position(p.position,True).y, self.get_position(p.old_pos,True).y), max(self.get_position(p.position,True).y, self.get_position(p.old_pos,True).y)))
                    online_rect = pygame.Rect(pos.x - (self.tile_size // 2),
                                                     pos.y - (self.tile_size // 2),
                                                     self.tile_size,
                                                     self.tile_size)
                    if local_rect_x.colliderect(online_rect):
                        can_move_x = False
                    if local_rect_y.colliderect(online_rect):
                        can_move_y = False
                    if local_rect_current.colliderect(online_rect):

                        x1, y1 = local_rect_current.center
                        x2, y2 = local_rect_current.center

                        dx = x1 - x2
                        dy = y1 - y2

                        dist = math.hypot(dx, dy)

                        if dist == 0:
                            dx, dy = 1, 0
                            dist = 1

                        dx /= dist
                        dy /= dist

                        push_strength = 10

                        self.get_position().x += int(dx * push_strength)
                        self.get_position().y += int(dy * push_strength)

                for x in range(-1,2):
                    for y in range(-1, 2):
                        wx = (self.get_position().x + x * self.tile_size)
                        wy = (self.get_position().y + y * self.tile_size)

                        # --- Welt-Tile-Koordinaten (in Tiles, nicht Pixel!) ---
                        world_tile_x = wx // self.tile_size
                        world_tile_y = wy // self.tile_size

                        # --- Chunk-Koordinaten (welcher 32x32-Block) ---
                        chunk_x = world_tile_x // self.chunk_size
                        chunk_y = world_tile_y // self.chunk_size

                        # --- Lokaler Index im Chunk (0..1023) ---
                        local_x = world_tile_x % self.chunk_size
                        local_y = world_tile_y % self.chunk_size
                        local_index = local_y * self.chunk_size + local_x

                        chunk = self.chunks.get((chunk_x,chunk_y))
                        if chunk is None:
                            continue
                        tile_rect = pygame.Rect(world_tile_x * self.tile_size, world_tile_y * self.tile_size,
                                                self.tile_size, self.tile_size)
                        if ((world_tile_x, world_tile_y) in self.inside_tiles_last_frame):
                            if not local_rect_current.colliderect(tile_rect):
                                self.inside_tiles_last_frame.remove((world_tile_x, world_tile_y))
                                if tiles[chunk.get_type(local_index)].get("type"):
                                    value_handler.tile_types[tiles[chunk.get_type(local_index)]["type"]](chunk.get_data(local_index)).on_player_leave()
                        else:
                            if local_rect_current.colliderect(tile_rect):
                                self.inside_tiles_last_frame.append((world_tile_x, world_tile_y))
                                if tiles[chunk.get_type(local_index)].get("type"):
                                    value_handler.tile_types[tiles[chunk.get_type(local_index)]["type"]](chunk.get_data(local_index)).on_player_enter()
                        collision : list[bool] = tiles[chunk.get_type(int(local_index))]["collision"]
                        for i in range(len(collision)):
                            collision_point = collision[i]
                            if collision_point:
                                point_pos = ((i % 3) / 2.0, (i // 3) / 2.0)
                                world_point_pos = ((world_tile_x + point_pos[0]) * self.tile_size, (world_tile_y + point_pos[1]) * self.tile_size)
                                if local_rect_x.collidepoint(*world_point_pos):
                                    can_move_x = False
                                if local_rect_y.collidepoint(*world_point_pos):
                                    can_move_y = False


                if (can_move_x or self.editor_overlay.visible) and not self.chat_input.is_focused():
                    self.position.x += dx * speed_px_per_frame
                if (can_move_y or self.editor_overlay.visible) and not self.chat_input.is_focused():
                    self.position.y += dy * speed_px_per_frame
            else:
                self.animation = 0
        self.animation_tick += 1
        online_handler.throttled_sender.tick(scene_handler.delta,int(self.position.x),int(self.position.y),int(self.direction),int(self.animation),int(self.animation_tick))
        if self.camera_rule == "move_free":
            self.camera_rect.center = (self.get_position().x, self.get_position().y)
        if self.camera_rule == "rooms":
            # Größe eines Chunks in Pixeln
            room_w = self.chunk_size * self.tile_size
            room_h = self.chunk_size * self.tile_size

            # Bestimme in welchem Chunk der Spieler ist
            chunk_x = int(self.get_position().x // room_w)
            chunk_y = int(self.get_position().y // room_h)

            # Ziel: Mittelpunkt dieses Chunks
            target_center = (
                chunk_x * room_w + room_w // 2,
                chunk_y * room_h + room_h // 2
            )

            # Erste Initialisierung → Kamera direkt setzen
            if not hasattr(self, "camera_target"):
                self.camera_target = target_center
                self.camera_rect.center = target_center
                self.transition_frame = 0
                self.start_center = target_center
            else:
                # Hat sich das Ziel geändert? → Übergang starten
                if target_center != self.camera_target:
                    self.camera_target = target_center
                    self.start_center = self.camera_rect.center
                    self.transition_frame = 0

                # Wenn wir noch nicht am Ziel sind → interpolieren
                if self.camera_rect.center != self.camera_target:
                    self.transition_frame += 1
                    t = min(self.transition_frame / 20.0, 1.0)  # 20 Frames animieren

                    # Linear Interpolation Start → Ziel
                    new_cx = self.start_center[0] + (self.camera_target[0] - self.start_center[0]) * t
                    new_cy = self.start_center[1] + (self.camera_target[1] - self.start_center[1]) * t
                    self.camera_rect.center = (new_cx, new_cy)
                else:
                    # Ziel erreicht → sicherstellen, dass es exakt sitzt
                    self.camera_rect.center = self.camera_target

        chunk_size_px = self.tile_size * self.chunk_size
        player_chunk_pos = Vector2i(
            int(math.floor(self.get_position().x / chunk_size_px)),
            int(math.floor(self.get_position().y / chunk_size_px)),
        )
        selected_surface = pygame.Surface((self.tile_size, self.tile_size))
        pygame.draw.rect(selected_surface, (120, 120, 255), (0, 0, self.tile_size, self.tile_size))
        selected_surface.set_alpha(127)
        for rx in range(-self.render_distance, self.render_distance + 1):
            for ry in range(-self.render_distance, self.render_distance + 1):
                chunk_pos = Vector2i(player_chunk_pos.x + rx, player_chunk_pos.y + ry)
                chunk = self.chunks.get((chunk_pos.x, chunk_pos.y))
                if chunk is None:
                    chunk = TileChunk()
                    self.chunks[(chunk_pos.x, chunk_pos.y)] = chunk

                # Pixel-Ursprung dieses Chunks relativ zur Kamera
                chunk_origin_x = chunk_pos.x * chunk_size_px - self.camera_rect.x
                chunk_origin_y = chunk_pos.y * chunk_size_px - self.camera_rect.y

                for i, id in enumerate(chunk.tiles):
                    tid = chunk.get_type(i)
                    local_x = i % self.chunk_size
                    local_y = i // self.chunk_size
                    dst_x = chunk_origin_x + local_x * self.tile_size
                    dst_y = chunk_origin_y + local_y * self.tile_size

                    # Hintergrund
                    grass = self.get_texture(self.floor_tile)
                    surface.blit(grass, (dst_x, dst_y))

                    # Tile
                    if tid != -1:
                        tex = self.get_texture(tiles[tid]["texture"])
                        surface.blit(tex, (dst_x, dst_y))
                    if self.editor_overlay.visible and self.selected is not None and (self.selected[0] == chunk and self.selected[1] == i) and self.is_select_mode:
                        surface.blit(selected_surface, (dst_x, dst_y))
                    #pygame.draw.rect(surface, (0, 255, 0),(dst_x, dst_y,self.tile_size, self.tile_size),1)
                #pygame.draw.rect(surface, (255,0,0), (chunk_origin_x, chunk_origin_y, chunk_size_px, chunk_size_px),1)


        player_rect = pygame.Rect(self.get_position().x - self.camera_rect.x - (self.tile_size // 2),self.get_position().y - self.camera_rect.y - (self.tile_size // 2),self.tile_size,self.tile_size)
        player_texture = self.get_animation_state(self.direction,self.animation,self.animation_tick, skin_id=self.skin)
        context = draw_context.DrawContext(surface)

        context.text(value_handler.username,"Boxy-Bold",Vector2i(player_rect.centerx - (pygame.font.SysFont("Boxy-Bold",24).size(value_handler.username)[0] // 2), player_rect.y - self.chunk_size),24)
        surface.blit(player_texture,(player_rect.x,player_rect.y))

        for key in online_handler.online_players:
            p = online_handler.online_players[key]
            if p.dimension != self.dimension:
                continue
            online_player_pos = (((self.get_position(p.position,True) + -self.get_position(p.old_pos,True)) / 3.0) * p.tick) + self.get_position(p.old_pos,True)
            online_player_texture = self.get_animation_state(p.direction,p.animation,p.animation_tick, skin_id=p.skin)

            pos = Vector2i(clamp(online_player_pos.x,min(self.get_position(p.position,True).x,self.get_position(p.old_pos,True).x),max(self.get_position(p.position,True).x,self.get_position(p.old_pos,True).x)),clamp(online_player_pos.y,min(self.get_position(p.position,True).y,self.get_position(p.old_pos,True).y),max(self.get_position(p.position,True).y,self.get_position(p.old_pos,True).y)))
            p.tick += 1
            online_player_rect = pygame.Rect(pos.x - self.camera_rect.x - (self.tile_size // 2), pos.y - self.camera_rect.y - (self.tile_size // 2), self.tile_size, self.tile_size)
            context.text(p.name, "Boxy-Bold", Vector2i(online_player_rect.centerx - (pygame.font.SysFont("Boxy-Bold",24).size(p.name)[0] // 2), online_player_rect.y - self.chunk_size), 24)
            surface.blit(online_player_texture, (online_player_rect.x,online_player_rect.y))
        if value_handler.open_screen is not None:
            value_handler.open_screen.render(surface,events)
            return True

        mx, my = pygame.mouse.get_pos()
        # --- Welt-Tile-Koordinaten (in Tiles, nicht Pixel!) ---
        world_tile_x = (mx + self.camera_rect.x) // self.tile_size
        world_tile_y = (my + self.camera_rect.y) // self.tile_size

        # --- Chunk-Koordinaten (welcher 32x32-Block) ---
        chunk_x = world_tile_x // self.chunk_size
        chunk_y = world_tile_y // self.chunk_size

        # --- Lokaler Index im Chunk (0..1023) ---
        local_x = world_tile_x % self.chunk_size
        local_y = world_tile_y % self.chunk_size
        local_index = local_y * self.chunk_size + local_x

        if self.editor_overlay.visible and not self.editor_overlay.get_rect().collidepoint(mx, my) and not self.modify_button.get_rect().collidepoint(mx, my) and not self.edit_button.get_rect().collidepoint(mx, my) and not self.save_button.get_rect().collidepoint(mx, my):

            if pygame.mouse.get_pressed()[0]:
                chunk = self.chunks.get((chunk_x, chunk_y))
                if chunk is None:
                    chunk = TileChunk()
                    self.chunks[(chunk_x, chunk_y)] = chunk

                # Editor-Tile setzen
                # Editor-Tile setzen
                if self.is_select_mode:
                    self.selected = (chunk, local_index)

                else:
                    for tilex in range(self.editor_overlay.selected[0].x,self.editor_overlay.selected[1].x + 1):
                        for tiley in range(self.editor_overlay.selected[0].y, self.editor_overlay.selected[1].y + 1):
                            chunk.tiles[local_index + (self.chunk_size * (tiley - self.editor_overlay.selected[0].y )) + (tilex - self.editor_overlay.selected[0].x )] = int((18 * tiley) + tilex)
            elif pygame.mouse.get_pressed()[1]:
                chunk = self.chunks.get((chunk_x, chunk_y))
                if chunk is None:
                    chunk = TileChunk()
                    self.chunks[(chunk_x, chunk_y)] = chunk

                # Editor-Tile setzen
                chunk.tiles[local_index] = -1


            # Vorschau-Rahmen exakt an der Tile unter dem Cursor
            highlight_px_x = world_tile_x * self.tile_size - self.camera_rect.x
            highlight_px_y = world_tile_y * self.tile_size - self.camera_rect.y
            if not self.is_select_mode:
                for tilex in range(self.editor_overlay.selected[0].x, self.editor_overlay.selected[1].x + 1):
                    for tiley in range(self.editor_overlay.selected[0].y, self.editor_overlay.selected[1].y + 1):
                        tex = self.get_texture(tiles[int((18 * tiley) + tilex)]["texture"])
                        surf = tex.copy()
                        surf.set_alpha(127)
                        surface.blit(surf, (highlight_px_x + (tilex - self.editor_overlay.selected[0].x) * self.tile_size, highlight_px_y + (tiley - self.editor_overlay.selected[0].y)  * self.tile_size))

            pygame.draw.rect(
                surface, (255, 255, 255),
                (highlight_px_x, highlight_px_y, self.tile_size, self.tile_size), 2
            )
        super().render(surface,events)
        chat_y = scene_handler.camera_size.y - 64
        for message in value_handler.chat.__reversed__():

            alpha = self.get_value(message[0])
            if alpha == 0.0:
                continue
            custom_renderer.Renderer(surface).text(message[1],"arial",Vector2i(0,chat_y),16,alpha=alpha, color=(255,255,255))
            chat_y -= pygame.font.SysFont("Arial",16).get_height() * len(message[1].split("\n"))
        return True

    is_fullscreen = False
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            pygame.quit()
            pygame.init()
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
            desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
            new_screen = pygame.display.set_mode((desktop_w,desktop_h), pygame.NOFRAME)
            global screen
            screen = new_screen
        else:
            pygame.display.set_mode((800,600),pygame.RESIZABLE)