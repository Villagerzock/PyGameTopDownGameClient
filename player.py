from better_math import Vector2i


class Player:
    def __init__(self, uuid : str,name : str, position : Vector2i,old_pos : Vector2i,direction : int,animation : int,animation_tick : int):
        self.uuid = uuid
        self.name = name
        self.position = position
        self.old_pos = old_pos
        self.direction = direction
        self.animation = animation
        self.animation_tick = animation_tick
        self.tick = 0