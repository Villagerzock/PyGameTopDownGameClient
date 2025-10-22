import json
import os.path

import pygame


def get_texture(texture, animation_tick, animation):
    if os.path.exists(f"textures/{texture}.json"):
        with open(f"textures/{texture}.json", "r") as f:
            data = json.load(f)
            animation_data = data["animations"][animation]
            animation_length = len(animation_data["textures"])
            animation_wait = animation_data["wait"]
            animation_tex = animation_data["textures"][(animation_tick // animation_wait) % animation_length]
            return pygame.image.load(f"textures/{animation_tex}.png").convert_alpha()
    else:
        return pygame.image.load(f"textures/{animation}.png").convert_alpha()
