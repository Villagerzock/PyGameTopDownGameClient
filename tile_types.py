import scene_handler
from better_math import Vector2i

import value_handler
from screens import FadeOutScreen
from value_handler import TileType


class DoorType(TileType):
    def on_faded_out(self, fade_out_screen : FadeOutScreen):
        scene_handler.current_scene = value_handler.tile_world_type(self.data["dim"])
        scene_handler.current_scene.position = Vector2i(int(self.get_data("x") if self.get_data("x") != "" else 0),int(self.get_data("y") if self.get_data("y") != "" else 0))
        fade_out_screen.fade_in()
    def on_player_enter(self):
        print("Door Entered")
        if self.get_data("dim") == "":
            return

        value_handler.open_screen = FadeOutScreen(self.on_faded_out)
    def get_values(self) -> dict[str, tuple[type[str | int | bool]]]:
        return {
            "dim":(str,),
            "x":(int,),
            "y":(int,)
        }