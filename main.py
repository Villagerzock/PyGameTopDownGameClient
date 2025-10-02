import sys
from collections.abc import dict_items

import pygame
import scene_handler
from better_math import Vector2i

from pygame_scene import PyGameScene, PyOverlay


import online_handler
import value_handler
from menus import Login


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
        else:
            if isinstance(scene_handler.current_scene,value_handler.tile_world_type):
                scene_handler.current_scene.close()
        pygame.display.update()
        scene_handler.delta = clock.tick(scene_handler.FPS)

if __name__ == "__main__":
    #scene_handler.FPS = 10
    setup(Login(),sys.argv[1])

