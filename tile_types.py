import scene_handler

import value_handler
from screens import FadeOutScreen
from value_handler import TileType


class DoorType(TileType):
    def on_faded_out(self, fade_out_screen : FadeOutScreen):
        scene_handler.current_scene = value_handler.tile_world_type(self.data["dim"])
        fade_out_screen.fade_in()
    def on_player_enter(self):
        print("Door Entered")
        value_handler.open_screen = FadeOutScreen(self.on_faded_out)
    def get_values(self) -> dict[str, tuple[type[str | int | bool]]]:
        return {
            "dim":(str,)
        }