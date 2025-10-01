import pygame
import scene_handler
from elements.py_button import Button
from elements.text import Text, TextEdit
from pygame_scene import PyGameScene, PyGameUIHandler

from value_handler import TileChunk, Screen


class ModifyTileScreen(Screen):
    def __init__(self, tile_instance,chunk : TileChunk,tile_idx):
        self.save_button = None
        self.tile_instance = tile_instance
        self.chunk = chunk
        self.tile_idx = tile_idx
        for value in self.tile_instance.get_values():
            self.objects[value] = TextEdit("","","arial",pygame.Rect(0,0,0,0))
        super().__init__()
    objects : dict[str, PyGameUIHandler] = {}
    def update(self):
        y = 10
        def save():
            values = {}
            for value in self.tile_instance.get_values():
                values[value] = self.objects[value]
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
