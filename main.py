import json
import math
import os
import struct
import sys
from collections.abc import dict_items
from unittest import case

import pygameui
import pygame
import scene_handler
from better_math import Vector2i
from elements.py_button import Button
from pygame._sdl2 import Window
from pygame.math import clamp
from pygame_scene import PyGameScene, PyOverlay
from typing import Literal

import online_handler
from custom_elements import EditorTileOverlay

tiles : list[dict[str,str | list[bool]]] = [{'texture': 'Overworld_Tileset_00_00'}, {'texture': 'Overworld_Tileset_00_01'}, {'texture': 'Overworld_Tileset_00_02'}, {'texture': 'Overworld_Tileset_00_03'}, {'texture': 'Overworld_Tileset_00_04'}, {'texture': 'Overworld_Tileset_00_05'}, {'texture': 'Overworld_Tileset_00_06'}, {'texture': 'Overworld_Tileset_00_07'}, {'texture': 'Overworld_Tileset_00_08'}, {'texture': 'Overworld_Tileset_00_09'}, {'texture': 'Overworld_Tileset_00_10'}, {'texture': 'Overworld_Tileset_00_11'}, {'texture': 'Overworld_Tileset_00_12'}, {'texture': 'Overworld_Tileset_00_13'}, {'texture': 'Overworld_Tileset_00_14'}, {'texture': 'Overworld_Tileset_00_15'}, {'texture': 'Overworld_Tileset_00_16'}, {'texture': 'Overworld_Tileset_00_17'}, {'texture': 'Overworld_Tileset_01_00'}, {'texture': 'Overworld_Tileset_01_01'}, {'texture': 'Overworld_Tileset_01_02'}, {'texture': 'Overworld_Tileset_01_03'}, {'texture': 'Overworld_Tileset_01_04'}, {'texture': 'Overworld_Tileset_01_05'}, {'texture': 'Overworld_Tileset_01_06'}, {'texture': 'Overworld_Tileset_01_07'}, {'texture': 'Overworld_Tileset_01_08'}, {'texture': 'Overworld_Tileset_01_09'}, {'texture': 'Overworld_Tileset_01_10'}, {'texture': 'Overworld_Tileset_01_11'}, {'texture': 'Overworld_Tileset_01_12'}, {'texture': 'Overworld_Tileset_01_13'}, {'texture': 'Overworld_Tileset_01_14'}, {'texture': 'Overworld_Tileset_01_15'}, {'texture': 'Overworld_Tileset_01_16'}, {'texture': 'Overworld_Tileset_01_17'}, {'texture': 'Overworld_Tileset_02_00'}, {'texture': 'Overworld_Tileset_02_01'}, {'texture': 'Overworld_Tileset_02_02'}, {'texture': 'Overworld_Tileset_02_03'}, {'texture': 'Overworld_Tileset_02_04'}, {'texture': 'Overworld_Tileset_02_05'}, {'texture': 'Overworld_Tileset_02_06'}, {'texture': 'Overworld_Tileset_02_07'}, {'texture': 'Overworld_Tileset_02_08'}, {'texture': 'Overworld_Tileset_02_09'}, {'texture': 'Overworld_Tileset_02_10'}, {'texture': 'Overworld_Tileset_02_11'}, {'texture': 'Overworld_Tileset_02_12'}, {'texture': 'Overworld_Tileset_02_13'}, {'texture': 'Overworld_Tileset_02_14'}, {'texture': 'Overworld_Tileset_02_15'}, {'texture': 'Overworld_Tileset_02_16'}, {'texture': 'Overworld_Tileset_02_17'}, {'texture': 'Overworld_Tileset_03_00'}, {'texture': 'Overworld_Tileset_03_01'}, {'texture': 'Overworld_Tileset_03_02'}, {'texture': 'Overworld_Tileset_03_03'}, {'texture': 'Overworld_Tileset_03_04'}, {'texture': 'Overworld_Tileset_03_05'}, {'texture': 'Overworld_Tileset_03_06'}, {'texture': 'Overworld_Tileset_03_07'}, {'texture': 'Overworld_Tileset_03_08'}, {'texture': 'Overworld_Tileset_03_09'}, {'texture': 'Overworld_Tileset_03_10'}, {'texture': 'Overworld_Tileset_03_11'}, {'texture': 'Overworld_Tileset_03_12'}, {'texture': 'Overworld_Tileset_03_13'}, {'texture': 'Overworld_Tileset_03_14'}, {'texture': 'Overworld_Tileset_03_15'}, {'texture': 'Overworld_Tileset_03_16'}, {'texture': 'Overworld_Tileset_03_17'}, {'texture': 'Overworld_Tileset_04_00'}, {'texture': 'Overworld_Tileset_04_01'}, {'texture': 'Overworld_Tileset_04_02'}, {'texture': 'Overworld_Tileset_04_03'}, {'texture': 'Overworld_Tileset_04_04'}, {'texture': 'Overworld_Tileset_04_05'}, {'texture': 'Overworld_Tileset_04_06'}, {'texture': 'Overworld_Tileset_04_07'}, {'texture': 'Overworld_Tileset_04_08'}, {'texture': 'Overworld_Tileset_04_09'}, {'texture': 'Overworld_Tileset_04_10'}, {'texture': 'Overworld_Tileset_04_11'}, {'texture': 'Overworld_Tileset_04_12'}, {'texture': 'Overworld_Tileset_04_13'}, {'texture': 'Overworld_Tileset_04_14'}, {'texture': 'Overworld_Tileset_04_15'}, {'texture': 'Overworld_Tileset_04_16'}, {'texture': 'Overworld_Tileset_04_17'}, {'texture': 'Overworld_Tileset_05_00'}, {'texture': 'Overworld_Tileset_05_01'}, {'texture': 'Overworld_Tileset_05_02'}, {'texture': 'Overworld_Tileset_05_03'}, {'texture': 'Overworld_Tileset_05_04'}, {'texture': 'Overworld_Tileset_05_05'}, {'texture': 'Overworld_Tileset_05_06'}, {'texture': 'Overworld_Tileset_05_07'}, {'texture': 'Overworld_Tileset_05_08'}, {'texture': 'Overworld_Tileset_05_09'}, {'texture': 'Overworld_Tileset_05_10'}, {'texture': 'Overworld_Tileset_05_11'}, {'texture': 'Overworld_Tileset_05_12'}, {'texture': 'Overworld_Tileset_05_13'}, {'texture': 'Overworld_Tileset_05_14'}, {'texture': 'Overworld_Tileset_05_15'}, {'texture': 'Overworld_Tileset_05_16'}, {'texture': 'Overworld_Tileset_05_17'}, {'texture': 'Overworld_Tileset_06_00'}, {'texture': 'Overworld_Tileset_06_01'}, {'texture': 'Overworld_Tileset_06_02'}, {'texture': 'Overworld_Tileset_06_03'}, {'texture': 'Overworld_Tileset_06_04'}, {'texture': 'Overworld_Tileset_06_05'}, {'texture': 'Overworld_Tileset_06_06'}, {'texture': 'Overworld_Tileset_06_07'}, {'texture': 'Overworld_Tileset_06_08'}, {'texture': 'Overworld_Tileset_06_09'}, {'texture': 'Overworld_Tileset_06_10'}, {'texture': 'Overworld_Tileset_06_11'}, {'texture': 'Overworld_Tileset_06_12'}, {'texture': 'Overworld_Tileset_06_13'}, {'texture': 'Overworld_Tileset_06_14'}, {'texture': 'Overworld_Tileset_06_15'}, {'texture': 'Overworld_Tileset_06_16'}, {'texture': 'Overworld_Tileset_06_17'}, {'texture': 'Overworld_Tileset_07_00'}, {'texture': 'Overworld_Tileset_07_01'}, {'texture': 'Overworld_Tileset_07_02'}, {'texture': 'Overworld_Tileset_07_03'}, {'texture': 'Overworld_Tileset_07_04'}, {'texture': 'Overworld_Tileset_07_05'}, {'texture': 'Overworld_Tileset_07_06'}, {'texture': 'Overworld_Tileset_07_07'}, {'texture': 'Overworld_Tileset_07_08'}, {'texture': 'Overworld_Tileset_07_09'}, {'texture': 'Overworld_Tileset_07_10'}, {'texture': 'Overworld_Tileset_07_11'}, {'texture': 'Overworld_Tileset_07_12'}, {'texture': 'Overworld_Tileset_07_13'}, {'texture': 'Overworld_Tileset_07_14'}, {'texture': 'Overworld_Tileset_07_15'}, {'texture': 'Overworld_Tileset_07_16'}, {'texture': 'Overworld_Tileset_07_17'}, {'texture': 'Overworld_Tileset_08_00'}, {'texture': 'Overworld_Tileset_08_01'}, {'texture': 'Overworld_Tileset_08_02'}, {'texture': 'Overworld_Tileset_08_03'}, {'texture': 'Overworld_Tileset_08_04'}, {'texture': 'Overworld_Tileset_08_05'}, {'texture': 'Overworld_Tileset_08_06'}, {'texture': 'Overworld_Tileset_08_07'}, {'texture': 'Overworld_Tileset_08_08'}, {'texture': 'Overworld_Tileset_08_09'}, {'texture': 'Overworld_Tileset_08_10'}, {'texture': 'Overworld_Tileset_08_11'}, {'texture': 'Overworld_Tileset_08_12'}, {'texture': 'Overworld_Tileset_08_13'}, {'texture': 'Overworld_Tileset_08_14'}, {'texture': 'Overworld_Tileset_08_15'}, {'texture': 'Overworld_Tileset_08_16'}, {'texture': 'Overworld_Tileset_08_17'}, {'texture': 'Overworld_Tileset_09_00'}, {'texture': 'Overworld_Tileset_09_01'}, {'texture': 'Overworld_Tileset_09_02'}, {'texture': 'Overworld_Tileset_09_03'}, {'texture': 'Overworld_Tileset_09_04'}, {'texture': 'Overworld_Tileset_09_05'}, {'texture': 'Overworld_Tileset_09_06'}, {'texture': 'Overworld_Tileset_09_07'}, {'texture': 'Overworld_Tileset_09_08'}, {'texture': 'Overworld_Tileset_09_09'}, {'texture': 'Overworld_Tileset_09_10'}, {'texture': 'Overworld_Tileset_09_11'}, {'texture': 'Overworld_Tileset_09_12'}, {'texture': 'Overworld_Tileset_09_13'}, {'texture': 'Overworld_Tileset_09_14'}, {'texture': 'Overworld_Tileset_09_15'}, {'texture': 'Overworld_Tileset_09_16'}, {'texture': 'Overworld_Tileset_09_17'}, {'texture': 'Overworld_Tileset_10_00'}, {'texture': 'Overworld_Tileset_10_01'}, {'texture': 'Overworld_Tileset_10_02'}, {'texture': 'Overworld_Tileset_10_03'}, {'texture': 'Overworld_Tileset_10_04'}, {'texture': 'Overworld_Tileset_10_05'}, {'texture': 'Overworld_Tileset_10_06'}, {'texture': 'Overworld_Tileset_10_07'}, {'texture': 'Overworld_Tileset_10_08'}, {'texture': 'Overworld_Tileset_10_09'}, {'texture': 'Overworld_Tileset_10_10'}, {'texture': 'Overworld_Tileset_10_11'}, {'texture': 'Overworld_Tileset_10_12'}, {'texture': 'Overworld_Tileset_10_13'}, {'texture': 'Overworld_Tileset_10_14'}, {'texture': 'Overworld_Tileset_10_15'}, {'texture': 'Overworld_Tileset_10_16'}, {'texture': 'Overworld_Tileset_10_17'}, {'texture': 'Overworld_Tileset_11_00'}, {'texture': 'Overworld_Tileset_11_01'}, {'texture': 'Overworld_Tileset_11_02'}, {'texture': 'Overworld_Tileset_11_03'}, {'texture': 'Overworld_Tileset_11_04'}, {'texture': 'Overworld_Tileset_11_05'}, {'texture': 'Overworld_Tileset_11_06'}, {'texture': 'Overworld_Tileset_11_07'}, {'texture': 'Overworld_Tileset_11_08'}, {'texture': 'Overworld_Tileset_11_09'}, {'texture': 'Overworld_Tileset_11_10'}, {'texture': 'Overworld_Tileset_11_11'}, {'texture': 'Overworld_Tileset_11_12'}, {'texture': 'Overworld_Tileset_11_13'}, {'texture': 'Overworld_Tileset_11_14'}, {'texture': 'Overworld_Tileset_11_15'}, {'texture': 'Overworld_Tileset_11_16'}, {'texture': 'Overworld_Tileset_11_17'}, {'texture': 'Overworld_Tileset_12_00'}, {'texture': 'Overworld_Tileset_12_01'}, {'texture': 'Overworld_Tileset_12_02'}, {'texture': 'Overworld_Tileset_12_03'}, {'texture': 'Overworld_Tileset_12_04'}, {'texture': 'Overworld_Tileset_12_05'}, {'texture': 'Overworld_Tileset_12_06'}, {'texture': 'Overworld_Tileset_12_07'}, {'texture': 'Overworld_Tileset_12_08'}, {'texture': 'Overworld_Tileset_12_09'}, {'texture': 'Overworld_Tileset_12_10'}, {'texture': 'Overworld_Tileset_12_11'}, {'texture': 'Overworld_Tileset_12_12'}, {'texture': 'Overworld_Tileset_12_13'}, {'texture': 'Overworld_Tileset_12_14'}, {'texture': 'Overworld_Tileset_12_15'}, {'texture': 'Overworld_Tileset_12_16'}, {'texture': 'Overworld_Tileset_12_17'}, {'texture': 'Dungeon_Tileset_00_00'}, {'texture': 'Dungeon_Tileset_00_01'}, {'texture': 'Dungeon_Tileset_00_02'}, {'texture': 'Dungeon_Tileset_00_03'}, {'texture': 'Dungeon_Tileset_00_04'}, {'texture': 'Dungeon_Tileset_00_05'}, {'texture': 'Dungeon_Tileset_00_06'}, {'texture': 'Dungeon_Tileset_00_07'}, {'texture': 'Dungeon_Tileset_00_08'}, {'texture': 'Dungeon_Tileset_00_09'}, {'texture': 'Dungeon_Tileset_00_10'}, {'texture': 'Dungeon_Tileset_00_11'}, {'texture': 'Dungeon_Tileset_01_00'}, {'texture': 'Dungeon_Tileset_01_01'}, {'texture': 'Dungeon_Tileset_01_02'}, {'texture': 'Dungeon_Tileset_01_03'}, {'texture': 'Dungeon_Tileset_01_04'}, {'texture': 'Dungeon_Tileset_01_05'}, {'texture': 'Dungeon_Tileset_01_06'}, {'texture': 'Dungeon_Tileset_01_07'}, {'texture': 'Dungeon_Tileset_01_08'}, {'texture': 'Dungeon_Tileset_01_09'}, {'texture': 'Dungeon_Tileset_01_10'}, {'texture': 'Dungeon_Tileset_01_11'}, {'texture': 'Dungeon_Tileset_02_00'}, {'texture': 'Dungeon_Tileset_02_01'}, {'texture': 'Dungeon_Tileset_02_02'}, {'texture': 'Dungeon_Tileset_02_03'}, {'texture': 'Dungeon_Tileset_02_04'}, {'texture': 'Dungeon_Tileset_02_05'}, {'texture': 'Dungeon_Tileset_02_06'}, {'texture': 'Dungeon_Tileset_02_07'}, {'texture': 'Dungeon_Tileset_02_08'}, {'texture': 'Dungeon_Tileset_02_09'}, {'texture': 'Dungeon_Tileset_02_10'}, {'texture': 'Dungeon_Tileset_02_11'}, {'texture': 'Dungeon_Tileset_03_00'}, {'texture': 'Dungeon_Tileset_03_01'}, {'texture': 'Dungeon_Tileset_03_02'}, {'texture': 'Dungeon_Tileset_03_03'}, {'texture': 'Dungeon_Tileset_03_04'}, {'texture': 'Dungeon_Tileset_03_05'}, {'texture': 'Dungeon_Tileset_03_06'}, {'texture': 'Dungeon_Tileset_03_07'}, {'texture': 'Dungeon_Tileset_03_08'}, {'texture': 'Dungeon_Tileset_03_09'}, {'texture': 'Dungeon_Tileset_03_10'}, {'texture': 'Dungeon_Tileset_03_11'}, {'texture': 'Dungeon_Tileset_04_00'}, {'texture': 'Dungeon_Tileset_04_01'}, {'texture': 'Dungeon_Tileset_04_02'}, {'texture': 'Dungeon_Tileset_04_03'}, {'texture': 'Dungeon_Tileset_04_04'}, {'texture': 'Dungeon_Tileset_04_05'}, {'texture': 'Dungeon_Tileset_04_06'}, {'texture': 'Dungeon_Tileset_04_07'}, {'texture': 'Dungeon_Tileset_04_08'}, {'texture': 'Dungeon_Tileset_04_09'}, {'texture': 'Dungeon_Tileset_04_10'}, {'texture': 'Dungeon_Tileset_04_11'}, {'texture': 'Dungeon_Tileset_05_00'}, {'texture': 'Dungeon_Tileset_05_01'}, {'texture': 'Dungeon_Tileset_05_02'}, {'texture': 'Dungeon_Tileset_05_03'}, {'texture': 'Dungeon_Tileset_05_04'}, {'texture': 'Dungeon_Tileset_05_05'}, {'texture': 'Dungeon_Tileset_05_06'}, {'texture': 'Dungeon_Tileset_05_07'}, {'texture': 'Dungeon_Tileset_05_08'}, {'texture': 'Dungeon_Tileset_05_09'}, {'texture': 'Dungeon_Tileset_05_10'}, {'texture': 'Dungeon_Tileset_05_11'}, {'texture': 'Dungeon_Tileset_06_00'}, {'texture': 'Dungeon_Tileset_06_01'}, {'texture': 'Dungeon_Tileset_06_02'}, {'texture': 'Dungeon_Tileset_06_03'}, {'texture': 'Dungeon_Tileset_06_04'}, {'texture': 'Dungeon_Tileset_06_05'}, {'texture': 'Dungeon_Tileset_06_06'}, {'texture': 'Dungeon_Tileset_06_07'}, {'texture': 'Dungeon_Tileset_06_08'}, {'texture': 'Dungeon_Tileset_06_09'}, {'texture': 'Dungeon_Tileset_06_10'}, {'texture': 'Dungeon_Tileset_06_11'}, {'texture': 'Dungeon_Tileset_07_00'}, {'texture': 'Dungeon_Tileset_07_01'}, {'texture': 'Dungeon_Tileset_07_02'}, {'texture': 'Dungeon_Tileset_07_03'}, {'texture': 'Dungeon_Tileset_07_04'}, {'texture': 'Dungeon_Tileset_07_05'}, {'texture': 'Dungeon_Tileset_07_06'}, {'texture': 'Dungeon_Tileset_07_07'}, {'texture': 'Dungeon_Tileset_07_08'}, {'texture': 'Dungeon_Tileset_07_09'}, {'texture': 'Dungeon_Tileset_07_10'}, {'texture': 'Dungeon_Tileset_07_11'}, {'texture': 'Dungeon_Tileset_08_00'}, {'texture': 'Dungeon_Tileset_08_01'}, {'texture': 'Dungeon_Tileset_08_02'}, {'texture': 'Dungeon_Tileset_08_03'}, {'texture': 'Dungeon_Tileset_08_04'}, {'texture': 'Dungeon_Tileset_08_05'}, {'texture': 'Dungeon_Tileset_08_06'}, {'texture': 'Dungeon_Tileset_08_07'}, {'texture': 'Dungeon_Tileset_08_08'}, {'texture': 'Dungeon_Tileset_08_09'}, {'texture': 'Dungeon_Tileset_08_10'}, {'texture': 'Dungeon_Tileset_08_11'}, {'texture': 'Dungeon_Tileset_09_00'}, {'texture': 'Dungeon_Tileset_09_01'}, {'texture': 'Dungeon_Tileset_09_02'}, {'texture': 'Dungeon_Tileset_09_03'}, {'texture': 'Dungeon_Tileset_09_04'}, {'texture': 'Dungeon_Tileset_09_05'}, {'texture': 'Dungeon_Tileset_09_06'}, {'texture': 'Dungeon_Tileset_09_07'}, {'texture': 'Dungeon_Tileset_09_08'}, {'texture': 'Dungeon_Tileset_09_09'}, {'texture': 'Dungeon_Tileset_09_10'}, {'texture': 'Dungeon_Tileset_09_11'}, {'texture': 'Dungeon_Tileset_10_00'}, {'texture': 'Dungeon_Tileset_10_01'}, {'texture': 'Dungeon_Tileset_10_02'}, {'texture': 'Dungeon_Tileset_10_03'}, {'texture': 'Dungeon_Tileset_10_04'}, {'texture': 'Dungeon_Tileset_10_05'}, {'texture': 'Dungeon_Tileset_10_06'}, {'texture': 'Dungeon_Tileset_10_07'}, {'texture': 'Dungeon_Tileset_10_08'}, {'texture': 'Dungeon_Tileset_10_09'}, {'texture': 'Dungeon_Tileset_10_10'}, {'texture': 'Dungeon_Tileset_10_11'}, {'texture': 'Dungeon_Tileset_11_00'}, {'texture': 'Dungeon_Tileset_11_01'}, {'texture': 'Dungeon_Tileset_11_02'}, {'texture': 'Dungeon_Tileset_11_03'}, {'texture': 'Dungeon_Tileset_11_04'}, {'texture': 'Dungeon_Tileset_11_05'}, {'texture': 'Dungeon_Tileset_11_06'}, {'texture': 'Dungeon_Tileset_11_07'}, {'texture': 'Dungeon_Tileset_11_08'}, {'texture': 'Dungeon_Tileset_11_09'}, {'texture': 'Dungeon_Tileset_11_10'}, {'texture': 'Dungeon_Tileset_11_11'}, {'texture': 'Dungeon_Tileset_12_00'}, {'texture': 'Dungeon_Tileset_12_01'}, {'texture': 'Dungeon_Tileset_12_02'}, {'texture': 'Dungeon_Tileset_12_03'}, {'texture': 'Dungeon_Tileset_12_04'}, {'texture': 'Dungeon_Tileset_12_05'}, {'texture': 'Dungeon_Tileset_12_06'}, {'texture': 'Dungeon_Tileset_12_07'}, {'texture': 'Dungeon_Tileset_12_08'}, {'texture': 'Dungeon_Tileset_12_09'}, {'texture': 'Dungeon_Tileset_12_10'}, {'texture': 'Dungeon_Tileset_12_11'}]

with open("tiles.json", "r", encoding="utf-8") as f:
    tiles = json.load(f)


class TileChunk:
    SIZE = 32
    def __init__(self, chunks=None):
        if chunks is None:
            chunks = [-1] * (self.SIZE * self.SIZE)
        self.tiles: list[int] = chunks
        if len(self.tiles) < self.SIZE * self.SIZE:
            self.tiles += [-1] * (self.SIZE * self.SIZE - len(self.tiles))



class TileWorld(PyGameScene):
    def __init__(self):
        self.editor_overlay = None
        self.save_button = None
        self.load_world()
        super().__init__()

    texture_cache : dict[str,pygame.Surface] = {}
    def get_texture(self, name: str,prefix = "tiles/") -> pygame.Surface:
        texture = self.texture_cache.get(name)
        if texture is None:
            self.texture_cache[name] = pygame.transform.scale(pygame.image.load(prefix + name + ".png").convert_alpha(),(self.tile_size,self.tile_size))
            return self.texture_cache[name]
        return texture

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
        items : dict_items[tuple[tuple[int,int],TileChunk]] = self.chunks.items()
        chunk_items : list[tuple[tuple[int,int],TileChunk]] = []
        for item in items:
            print(item[1].tiles.count(-1))
            if item[1].tiles.count(-1) != (32 * 32):
                chunk_items.append(item)
        data = {

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
        for entry in data.get("chunks", []):
            pos = entry.get("pos", [0, 0])
            tiles = entry.get("tiles", [])
            # TileChunk kümmert sich ums Auffüllen, falls Liste kürzer ist
            chunk = TileChunk(tiles)
            self.chunks[(int(pos[0]), int(pos[1]))] = chunk
    def update(self):
        global tiles
        super().update()
        png = pygame.image.load("textures/gui/cursor_normal.png").convert_alpha()
        hotspot = (12, 4)
        cursor = pygame.cursors.Cursor(hotspot, png)
        pygame.mouse.set_cursor(cursor)
        #self.tile_size = min(scene_handler.camera_size.y,scene_handler.camera_size.x) // 20
        self.texture_cache.clear()
        self.camera_rect = pygame.Rect(self.position.x - (scene_handler.camera_size.x // 2), self.position.y - (scene_handler.camera_size.y // 2), scene_handler.camera_size.x,scene_handler.camera_size.y)
        self.editor_overlay = EditorTileOverlay(pygame.Rect(scene_handler.camera_size.x - (self.tile_size * 10),0,(self.tile_size * 10),scene_handler.camera_size.y),tile_size=self.tile_size,tiles=tiles,scene=self)
        self.editor_overlay.visible = False
        self.drawables.append(
            self.editor_overlay
        )


        self.save_button = Button("Save",(125,20),(250,40),pygame.font.SysFont("arial",16),self.save_world)
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

    def get_animation_state(self, direction, animation, animationTick):
        match animation:
            case 0:
                return self.get_texture(f"Char_idle_{self.get_dir_string(direction)}_00_{((animationTick // 5) % 6):02d}",prefix="textures/player/")
            case 1:
                return self.get_texture(f"Char_walk_{self.get_dir_string(direction)}_00_{((animationTick // 10) % 6):02d}",prefix="textures/player/")
            case _:
                return self.get_texture(f"Char_4_sides_00_{(direction % 4):02d}",prefix="textures/player/")
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
    def render(self, surface: pygame.Surface, events):
        global tiles

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.toggle_editor()
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()

        if scene_handler.delta > 1.0 / 30.0:
            pass
            #print("BAD PERFORMANCE")
        pygame.draw.rect(surface, (0,0,0), (0,0,scene_handler.camera_size.x,scene_handler.camera_size.y))
        speed_px_per_frame = 8.0

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
            local_rect_x = pygame.Rect(0,0,self.tile_size // 2,self.tile_size)
            local_rect_x.center = (self.position.x + (dx * speed_px_per_frame), self.position.y)
            local_rect_y = pygame.Rect(0,0,self.tile_size // 2,self.tile_size)
            local_rect_y.center = (self.position.x, self.position.y + (dy * speed_px_per_frame))
            for key in online_handler.online_players:
                p = online_handler.online_players[key]
                online_player_pos = (((p.position + -p.old_pos) / 7.0) * p.tick) + p.old_pos

                pos = Vector2i(
                    clamp(online_player_pos.x, min(p.position.x, p.old_pos.x), max(p.position.x, p.old_pos.x)),
                    clamp(online_player_pos.y, min(p.position.y, p.old_pos.y), max(p.position.y, p.old_pos.y)))
                online_rect = pygame.Rect(pos.x - (self.tile_size // 2),
                                                 pos.y - (self.tile_size // 2),
                                                 self.tile_size,
                                                 self.tile_size)
                if local_rect_x.colliderect(online_rect):
                    can_move_x = False
                if local_rect_y.colliderect(online_rect):
                    can_move_y = False
            for x in range(-1,2):
                for y in range(-1,2):
                    wx = (self.position.x + x * self.tile_size)
                    wy = (self.position.y + y * self.tile_size)
                    # --- Welt-Tile-Koordinaten (in Tiles, nicht Pixel!) ---
                    world_tile_x = wx // self.tile_size
                    world_tile_y = wy // self.tile_size

                    # --- Chunk-Koordinaten (welcher 32x32-Block) ---
                    chunk_x = world_tile_x // 32
                    chunk_y = world_tile_y // 32

                    # --- Lokaler Index im Chunk (0..1023) ---
                    local_x = world_tile_x % 32
                    local_y = world_tile_y % 32
                    local_index = local_y * 32 + local_x

                    chunk = self.chunks.get((chunk_x,chunk_y))
                    if chunk is None:
                        continue
                    collision : list[bool] = tiles[chunk.tiles[int(local_index)]]["collision"]
                    print(f"Local X: {local_x} Local Y: {local_y} Type: {chunk.tiles[int(local_index)]}")
                    for i in range(len(collision)):
                        collision_point = collision[i]
                        if collision_point:
                            print("Checking for Point")
                            point_pos = ((i % 3) / 2.0, (i // 3) / 2.0)
                            world_point_pos = ((world_tile_x + point_pos[0]) * self.tile_size - self.tile_size // 2, (world_tile_y + point_pos[1]) * self.tile_size - self.tile_size // 2)
                            if local_rect_x.collidepoint(*world_point_pos):
                                can_move_x = False
                            if local_rect_y.collidepoint(*world_point_pos):
                                can_move_y = False


            if can_move_x:
                self.position.x += dx * speed_px_per_frame
            if can_move_y:
                self.position.y += dy * speed_px_per_frame
        else:
            self.animation = 0
        self.animation_tick += 1
        online_handler.throttled_sender.tick(scene_handler.delta,int(self.position.x),int(self.position.y),int(self.direction),int(self.animation),int(self.animation_tick))
        self.camera_rect.center = (self.position.x, self.position.y)
        chunk_size_px = self.tile_size * 32
        player_chunk_pos = Vector2i(
            int(math.floor(self.position.x / chunk_size_px)),
            int(math.floor(self.position.y / chunk_size_px)),
        )

        for rx in range(-1, 2):
            for ry in range(-1, 2):
                chunk_pos = Vector2i(player_chunk_pos.x + rx, player_chunk_pos.y + ry)
                chunk = self.chunks.get((chunk_pos.x, chunk_pos.y))
                if chunk is None:
                    chunk = TileChunk()
                    self.chunks[(chunk_pos.x, chunk_pos.y)] = chunk

                # Pixel-Ursprung dieses Chunks relativ zur Kamera
                chunk_origin_x = chunk_pos.x * chunk_size_px - self.camera_rect.x
                chunk_origin_y = chunk_pos.y * chunk_size_px - self.camera_rect.y

                for i, tid in enumerate(chunk.tiles):
                    local_x = i % 32
                    local_y = i // 32
                    dst_x = chunk_origin_x + local_x * self.tile_size
                    dst_y = chunk_origin_y + local_y * self.tile_size

                    # Hintergrund
                    grass = self.get_texture("Overworld_Tileset_01_06")
                    surface.blit(grass, (dst_x, dst_y))

                    # Tile
                    if tid != -1:
                        tex = self.get_texture(tiles[tid]["texture"])
                        surface.blit(tex, (dst_x, dst_y))
                    #pygame.draw.rect(surface, (0, 255, 0),(dst_x, dst_y,self.tile_size, self.tile_size),1)
                #pygame.draw.rect(surface, (255,0,0), (chunk_origin_x, chunk_origin_y, chunk_size_px, chunk_size_px),1)


        player_rect = pygame.Rect(0,0,self.tile_size,self.tile_size)
        player_rect.center = (scene_handler.camera_size.x // 2,scene_handler.camera_size.y // 2)
        player_texture = self.get_animation_state(self.direction,self.animation,self.animation_tick)
        surface.blit(player_texture,player_rect.center)

        for key in online_handler.online_players:
            p = online_handler.online_players[key]
            online_player_pos = (((p.position + -p.old_pos) / 7.0) * p.tick) + p.old_pos
            online_player_texture = self.get_animation_state(p.direction,p.animation,p.animation_tick)

            pos = Vector2i(clamp(online_player_pos.x,min(p.position.x,p.old_pos.x),max(p.position.x,p.old_pos.x)),clamp(online_player_pos.y,min(p.position.y,p.old_pos.y),max(p.position.y,p.old_pos.y)))
            p.tick += 1
            online_player_rect = pygame.Rect(pos.x - self.camera_rect.x - (self.tile_size // 2), pos.y - self.camera_rect.y - (self.tile_size // 2), self.tile_size, self.tile_size)
            surface.blit(online_player_texture, online_player_rect.center)


        mx, my = pygame.mouse.get_pos()
        # --- Welt-Tile-Koordinaten (in Tiles, nicht Pixel!) ---
        world_tile_x = (mx + self.camera_rect.x) // self.tile_size
        world_tile_y = (my + self.camera_rect.y) // self.tile_size

        # --- Chunk-Koordinaten (welcher 32x32-Block) ---
        chunk_x = world_tile_x // 32
        chunk_y = world_tile_y // 32

        # --- Lokaler Index im Chunk (0..1023) ---
        local_x = world_tile_x % 32
        local_y = world_tile_y % 32
        local_index = local_y * 32 + local_x

        if self.editor_overlay.visible and not self.editor_overlay.get_rect().collidepoint(mx, my) and not self.save_button.get_rect().collidepoint(mx, my):

            if pygame.mouse.get_pressed()[0]:
                chunk = self.chunks.get((chunk_x, chunk_y))
                if chunk is None:
                    chunk = TileChunk()
                    self.chunks[(chunk_x, chunk_y)] = chunk

                # Editor-Tile setzen
                chunk.tiles[local_index] = int(self.editor_overlay.selected)
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
            pygame.draw.rect(
                surface, (255, 255, 255),
                (highlight_px_x, highlight_px_y, self.tile_size, self.tile_size), 2
            )
        super().render(surface,events)
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
screen = None

clock = pygame.time.Clock()
def setup(default_scene : PyGameScene,window_name="PyGameUI Window"):
    global screen
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(window_name)
    screen = pygame.display.set_mode((scene_handler.camera_size.x,scene_handler.camera_size.y),pygame.RESIZABLE)
    running = True
    scene_handler.current_scene = default_scene
    default_scene.update()
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                scene_handler.camera_size = Vector2i(event.w,event.h)
                scene_handler.current_scene.update()
        if running:
            running = scene_handler.current_scene.render(screen,events)

        if not running:
            scene_handler.current_scene.close()
        pygame.display.update()
        scene_handler.delta = clock.tick(scene_handler.FPS)

if __name__ == "__main__":
    online_handler.client.join_server(sys.argv[1])
    setup(TileWorld(),sys.argv[1])

