from value_handler import TileType


class DoorType(TileType):
    def on_player_enter(self):
        pass
    def get_values(self) -> dict[str, tuple[type[str | int | bool]]]:
        return {
            "dim":(str,)
        }