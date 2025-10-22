import math
import struct

import pygame
from better_math import Vector2i
from pygame.math import clamp
from pygame_scene import PyOverlay, PyGameScene

import entities
from byte_buffer import ByteBuffer


class EditorTileOverlay(PyOverlay):
    def __init__(self, rect: pygame.Rect, tile_size: int = 64,
                 tiles: list[dict[str, str | list[bool]]] = None,
                 scene: PyGameScene = None):
        super().__init__(rect)
        self.scene = scene
        self.is_entity_mode = False
        self.tile_size = tile_size
        self.tiles = tiles or []
        self.selected = (Vector2i(0, 0),Vector2i(0, 0))
        # Scroll-Offset in TILE-Einheiten (negativ = nach links/oben gescrollt)
        self.editor_offset = Vector2i(0, 0)

    # Wie viele Spalten hat das gesamte Tileset-Raster?
    # (Deine Liste ist in 18er-Reihen organisiert: ..._00 bis ..._17)
    GRID_COLS = 18

    @property
    def cols_visible(self) -> int:
        return max(1, self.get_rect().width // self.tile_size)

    @property
    def rows_total(self) -> int:
        return math.ceil(len(self.tiles) / self.GRID_COLS)

    @property
    def rows_visible(self) -> int:
        return max(1, self.get_rect().height // self.tile_size)

    def _clamp_offset(self):
        # Negative Offsets, damit Content nach links/oben „rein“ geschoben wird.
        max_left = -(max(0, self.GRID_COLS - self.cols_visible))
        max_up = -(max(0, self.rows_total - self.rows_visible))
        self.editor_offset.x = clamp(self.editor_offset.x, max_left, 0)
        self.editor_offset.y = clamp(self.editor_offset.y, max_up, 0)

    pressed = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.get_rect().collidepoint(*event.pos):
            self.pressed = True
            rect = self.get_rect()
            # Maus -> lokale Overlay-Koordinate
            local_x = (event.pos[0] - rect.x) // self.tile_size
            local_y = (event.pos[1] - rect.y) // self.tile_size

            # Lokale sichtbare Zelle -> globale Rasterzelle (Offset beachten; offset ist <= 0)
            grid_x = local_x - self.editor_offset.x
            grid_y = local_y - self.editor_offset.y

            # Bounds prüfen
            if 0 <= grid_x < self.GRID_COLS and 0 <= grid_y < self.rows_total:
                tile_idx = grid_y * self.GRID_COLS + grid_x
                if 0 <= tile_idx < len(self.tiles):
                    self.selected = (Vector2i(grid_x, grid_y),Vector2i(grid_x, grid_y))
        if event.type == pygame.MOUSEMOTION and self.get_rect().collidepoint(*event.pos) and self.pressed:
            print("Changing Selection")
            rect = self.get_rect()
            # Maus -> lokale Overlay-Koordinate
            local_x = (event.pos[0] - rect.x) // self.tile_size
            local_y = (event.pos[1] - rect.y) // self.tile_size

            # Lokale sichtbare Zelle -> globale Rasterzelle (Offset beachten; offset ist <= 0)
            grid_x = local_x - self.editor_offset.x
            grid_y = local_y - self.editor_offset.y

            # Bounds prüfen
            if 0 <= grid_x < self.GRID_COLS and 0 <= grid_y < self.rows_total:
                tile_idx = grid_y * self.GRID_COLS + grid_x
                if 0 <= tile_idx < len(self.tiles):
                    self.selected = (Vector2i(self.selected[0].x, self.selected[0].y),Vector2i(grid_x,grid_y))
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False

    def draw(self, surface, offset: Vector2i = Vector2i(0, 0)):
        super().draw(surface, offset)

        rect = self.get_rect()
        mx, my = pygame.mouse.get_pos()
        local_mx, local_my = mx - rect.x, my - rect.y

        # Scroll per WASD nur, wenn Maus im Overlay
        if rect.collidepoint(mx, my):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.editor_offset.x -= 1
            if keys[pygame.K_d]:
                self.editor_offset.x += 1
            if keys[pygame.K_w]:
                self.editor_offset.y -= 1
            if keys[pygame.K_s]:
                self.editor_offset.y += 1
            self._clamp_offset()

        # Sichtbares Fenster im globalen Raster
        start_col = max(0, -self.editor_offset.x)
        end_col = min(self.GRID_COLS, start_col + self.cols_visible)
        start_row = max(0, -self.editor_offset.y)
        end_row = min(self.rows_total, start_row + self.rows_visible)

        # Zeichnen nur der sichtbaren Zellen
        selected_surface = pygame.Surface((self.tile_size, self.tile_size))
        pygame.draw.rect(selected_surface, (120, 120, 255), (0, 0, self.tile_size, self.tile_size))
        selected_surface.set_alpha(127)
        if self.is_entity_mode:
            for gy in range(start_row, end_row):
                for gx in range(start_col, end_col):
                    idx = gy * self.GRID_COLS + gx
                    if idx >= len(entities.entity_types.values()):
                        break
                    screen_x = rect.x + (gx + self.editor_offset.x) * self.tile_size
                    screen_y = rect.y + (gy + self.editor_offset.y) * self.tile_size
                    surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert()
                    fake_buffer = ByteBuffer(struct.pack("!IIIIIII",0,0,0,0,0,0,0))
                    entity : entities.Entity = entities.create_new_entity(list(entities.entity_types.keys())[idx],buffer=fake_buffer,uuid="")
                    entity.render(surf, self.tile_size)
                    surface.blit(surf, (screen_x, screen_y))
                    if self.selected[0].x -1 == gx and gy == self.selected[0].y:
                        surface.blit(selected_surface, (screen_x, screen_y))


        else:
            for gy in range(start_row, end_row):
                for gx in range(start_col, end_col):
                    idx = gy * self.GRID_COLS + gx
                    if idx >= len(self.tiles):
                        continue
                    screen_x = rect.x + (gx + self.editor_offset.x) * self.tile_size
                    screen_y = rect.y + (gy + self.editor_offset.y) * self.tile_size
                    tex = self.scene.get_texture(self.tiles[idx]["texture"])
                    surface.blit(tex, (screen_x, screen_y))
                    if (min(self.selected[0].x, self.selected[1].x) - 1 < gx < max(self.selected[0].x,
                                                                                   self.selected[1].x) + 1) and min(
                            self.selected[0].y, self.selected[1].y) - 1 < gy < max(self.selected[0].y,
                                                                                   self.selected[1].y) + 1:
                        surface.blit(selected_surface, (screen_x, screen_y))

        # Hover/Highlight im Overlay
        if rect.collidepoint(mx, my):
            hover_cx = (local_mx // self.tile_size)
            hover_cy = (local_my // self.tile_size)
            highlight_x = rect.x + hover_cx * self.tile_size
            highlight_y = rect.y + hover_cy * self.tile_size
            pygame.draw.rect(
                surface, (255, 255, 255),
                (highlight_x, highlight_y, self.tile_size, self.tile_size), 2
            )
