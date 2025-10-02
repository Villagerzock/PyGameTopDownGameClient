from typing import Callable

import pygame
import scene_handler
from better_math import Vector2i
from elements.py_button import Button
from elements.text import Text, TextEdit
from pygame.math import clamp
from pygame_scene import PyGameScene, PyGameUIHandler

from value_handler import TileChunk, Screen, TileType

class LoadingScreen(Screen):
    def update(self):
        super().update()
        self.drawables.append(Text("Connecting To Server...","arial",pygame.Rect(scene_handler.camera_size.x // 2,scene_handler.camera_size.y // 2, 0, 16)))
    def render(self, screen, events):
        pygame.draw.rect(screen,(40,120,40),(0,0,scene_handler.camera_size.x,scene_handler.camera_size.y))
        super().render(screen,events)
class ModifyTileScreen(Screen):
    def __init__(self, tile_instance : TileType,chunk : TileChunk,tile_idx):
        self.save_button = None
        self.tile_instance = tile_instance
        self.chunk = chunk
        self.tile_idx = tile_idx
        for value in self.tile_instance.get_values():
            self.objects[value] = TextEdit(tile_instance.data.get(value) if tile_instance.data.get(value) is not None else "","","arial",pygame.Rect(0,0,0,0))
        super().__init__()
    objects : dict[str, PyGameUIHandler] = {}
    def update(self):
        y = 10
        def save():
            values = {}
            for value in self.tile_instance.get_values():
                values[value] = self.objects[value].text
            self.chunk.tiles[self.tile_idx] = (self.chunk.get_type(self.tile_idx), values)

        self.save_button = Button("Save",(scene_handler.camera_size.x // 2,scene_handler.camera_size.y // 2 + 270),(250,40),pygame.font.SysFont("arial",16),save)
        self.drawables.append(self.save_button)
        for value in self.tile_instance.get_values():
            text_rect = pygame.Rect(scene_handler.camera_size.x // 2 - 330, scene_handler.camera_size.y // 2 - 296 + y,pygame.font.SysFont("arial",16).size(value)[0],16)
            edit_rect = pygame.Rect(scene_handler.camera_size.x // 2 , scene_handler.camera_size.y // 2 - 300 + y, 320, 24)
            text = Text(value, "arial", text_rect)
            self.objects[value] = TextEdit(self.objects[value].text,"Enter Text...","arial",edit_rect)
            self.drawables.append(text)
            self.drawables.append(self.objects[value])
            y += 28
    def render(self,surface,events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.close()
        rect = pygame.Rect(0,0,700,600)
        rect.center = (scene_handler.camera_size.x // 2,scene_handler.camera_size.y // 2)
        pygame.draw.rect(surface,(255,255,255),rect,border_radius=10)
        super().render(surface,events)
        small_bottom_rect = rect.copy()
        small_bottom_rect.h = 100
        pygame.draw.rect(surface,(255,255,255),small_bottom_rect.move(0,500),border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), rect, border_radius=10,width=2)
        self.save_button.draw(surface)


class FadeOutScreen(Screen):
    def __init__(self, on_faded_out : Callable[['FadeOutScreen'], None]):
        self.fade_out_surface = pygame.Surface((scene_handler.camera_size.x,scene_handler.camera_size.y))
        self.fade_out_surface.fill((0,0,0))
        self.on_faded_out = on_faded_out
        super().__init__()
    tick = 1
    fading_in = False
    has_called_on_faded_out = False
    frames = 60
    def fade_in(self):
        self.fading_in = True
        print("Fade In")
    def render(self,surface,events):
        super().render(surface,events)
        fade_out_dif = self.tick
        new_scale = Vector2i(scene_handler.camera_size.x / clamp(10 * fade_out_dif,1,self.frames), (scene_handler.camera_size.x / clamp(10 * self.tick,1,self.frames)) * (scene_handler.camera_size.x / scene_handler.camera_size.y))
        surface_copy = surface.copy()
        surface_copy = pygame.transform.scale(surface_copy,(new_scale.x,new_scale.y))
        surface_copy = pygame.transform.scale(surface_copy,(scene_handler.camera_size.x,scene_handler.camera_size.y))
        self.fade_out_surface.set_alpha(int(clamp((fade_out_dif / float(self.frames)) * 255, 0, 255)))
        if self.tick >= self.frames and not self.has_called_on_faded_out:
            self.on_faded_out(self)
            self.has_called_on_faded_out = True
        if self.fading_in:
            if self.tick == 0:
                self.close()

        surface_copy.blit(self.fade_out_surface,(0,0))
        surface.blit(surface_copy,(0,0))
        if self.fading_in:
            self.tick -= 1
        else:
            self.tick += 1
        self.tick = clamp(self.tick,0,self.frames)

