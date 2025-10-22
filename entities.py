from typing import Callable, Protocol, Type

import pygame
from better_math import Vector2i
from pygame import Rect

import animation_handler
from byte_buffer import ByteBuffer


def get_position(tile_size, position_offset: Vector2i = Vector2i(0, 0)) -> Vector2i:
    # print(self.position.x * (self.tile_size / 64.0))
    return Vector2i(int(position_offset.x * (tile_size / 64.0)),int(position_offset.y * (tile_size / 64.0)))


def create_new_entity(entity_type : str, uuid,buffer : ByteBuffer):
    entity_constructor = entity_types.get(entity_type)
    if entity_constructor is None:
        raise ValueError(f"{entity_type} is not a valid entity type")
    return entity_constructor(buffer,uuid)
class Entity(Protocol):
    def __init__(self, buffer,uuid):
        self.uuid = uuid
        self.animationTick = buffer.get_int()
        self.animation = buffer.get_int()
        self.position = Vector2i(buffer.get_int(),buffer.get_int())
        self.direction = buffer.get_int()
        self.dimension = buffer.get_string()
        self.old_pos = self.position
        self.tick = 0
    def update(self, buffer : ByteBuffer):
        pass
    def render(self, surface, tile_size):
        pygame.draw.rect(surface, (255,255,255), (0,0, tile_size, tile_size))

    def get_rect(self,tile_size):
        return Rect(self.position.x,self.position.y,tile_size,tile_size)


class SpinnerEntity(Entity):

    def render(self, surface, tile_size):
        surface.blit(pygame.transform.scale(animation_handler.get_texture("spinner/spinner",self.animationTick,self.animation),(tile_size,tile_size)),(0,0))


entity_types : dict[str, Type[Entity]] = {
    "spinner":SpinnerEntity
}