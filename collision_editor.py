import json
import os

import pygame
import pygameui
import scene_handler
from elements.py_button import Button
from pygame_scene import PyGameScene



class CollisionEditor(PyGameScene):
    IMG_SIZE = (256, 256)  # Breite, Höhe der dargestellten Textur/ des Bilds
    POINT_RADIUS = 6       # sichtbarer Punkt-Radius für das Zeichnen
    HIT_RADIUS = 10        # Klick-Radius für die Erkennung

    def __init__(self,image_paths = None,initial_points : list[list[bool]] = None):
        super().__init__()

        # ----------------------------
        # Liste von Bildpfaden (ANPASSEN!)
        # ----------------------------
        self.image_paths = image_paths if image_paths is not None else []
        self.points_state = initial_points if initial_points is not None else [[False] * 9 for _ in range(len(self.images))]

    # --- Button-Callbacks ---
    def _prev_image(self, *args):
        n = len(self.images)
        self.current_image = (self.current_image - 1) % n

    def _next_image(self, *args):
        n = len(self.images)
        self.current_image = (self.current_image + 1) % n

    def update(self):

        # Bilder laden (wenn Pfad fehlt, Dummy-Textur erzeugen)
        self.images = []
        for path in self.image_paths:
            p = "tiles/" + path + ".png"
            img = pygame.Surface(self.IMG_SIZE, pygame.SRCALPHA).convert_alpha()
            for y in range(0, 256, 32):
                for x in range(0, 256, 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    if (x // 32 + y // 32) % 2 == 0:
                        pygame.draw.rect(img, (70, 70, 70), rect)
                    else:
                        pygame.draw.rect(img, (50, 50, 50), rect)
            if os.path.isfile(p):
                img.blit(pygame.transform.scale(pygame.image.load(p).convert_alpha(), self.IMG_SIZE),(0,0))
            self.images.append(img)

        # Wenn keine Bilder angegeben wurden, wenigstens eins haben:
        if not self.images:
            dummy = pygame.Surface(self.IMG_SIZE, pygame.SRCALPHA).convert_alpha()
            dummy.fill((30, 30, 30))
            pygame.draw.rect(dummy, (120, 180, 255), dummy.get_rect(), 2)
            self.images = [dummy]

        self.current_image = 0


        # UI/Buttons
        self.drawables = []
        self._buttons_initialized = False
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 22)

        # Buttons einmalig erzeugen, oben links in der Ecke
        if not self._buttons_initialized:
            # Kompakte Buttons für "<" und ">"
            btn_prev = Button(
                text="<",
                center=(24, 18),     # sehr nahe oben links
                size=(36, 28),
                font=self.font,
                on_click=self._prev_image,
            )
            btn_next = Button(
                text=">",
                center=(24 + 44, 18),  # rechts daneben
                size=(36, 28),
                font=self.font,
                on_click=self._next_image,
            )
            btn_save = Button(
                text="Save",
                center=(24 + 104, 18),
                size=(72, 28),
                font=self.font,
                on_click=self._save
            )
            self.drawables.append(btn_prev)
            self.drawables.append(btn_next)
            self.drawables.append(btn_save)
            self._buttons_initialized = True

    def _image_rect_centered(self):
        """Berechnet den zentrierten Ziel-Rect für das 256x256 Bild."""
        # Fenstergröße aus scene_handler
        cam_w = int(scene_handler.camera_size.x)
        cam_h = int(scene_handler.camera_size.y)
        img_w, img_h = self.IMG_SIZE
        x = (cam_w - img_w) // 2
        y = (cam_h - img_h) // 2
        return pygame.Rect(x, y, img_w, img_h)

    def _grid_points_for_rect(self, rect: pygame.Rect):
        """Gibt 9 Punkt-Positionen (x, y) für ein 3x3-Raster über rect zurück."""
        xs = [rect.left, rect.left + rect.width // 2, rect.right]
        ys = [rect.top, rect.top + rect.height // 2, rect.bottom]
        points = [
            (xs[0], ys[0]), (xs[1], ys[0]), (xs[2], ys[0]),
            (xs[0], ys[1]), (xs[1], ys[1]), (xs[2], ys[1]),
            (xs[0], ys[2]), (xs[1], ys[2]), (xs[2], ys[2]),
        ]
        return points

    def _handle_point_clicks(self, events, points, states):
        """Setzt Punkte von False->True (rot->blau), wenn angeklickt."""
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                for i, (px, py) in enumerate(points):
                    dx = mx - px
                    dy = my - py
                    if dx * dx + dy * dy <= self.HIT_RADIUS * self.HIT_RADIUS:
                        # Nur von False nach True schalten (kein Toggle zurück)
                        states[i] = not states[i]

    def render(self, screen, events) -> bool:
        # Hintergrund löschen
        screen.fill((18, 18, 18))

        # Bild-Rect berechnen und aktuelles Bild holen
        img_rect = self._image_rect_centered()
        img = self.images[self.current_image]

        # Bild zeichnen (zentriert)
        screen.blit(img, img_rect.topleft)

        # Punkte berechnen + Klicks verarbeiten
        points = self._grid_points_for_rect(img_rect)
        states = self.points_state[self.current_image]
        self._handle_point_clicks(events, points, states)

        # Punkte zeichnen (False=rot, True=blau), leicht gefüllt + Outline
        for i, (px, py) in enumerate(points):
            color = (70, 140, 255) if states[i] else (220, 60, 60)
            pygame.draw.circle(screen, color, (px, py), self.POINT_RADIUS)
            pygame.draw.circle(screen, (10, 10, 10), (px, py), self.POINT_RADIUS, 2)

        # Buttons/UI rendern
        for d in self.drawables:
            if hasattr(d, "render"):
                d.render(screen, events)
            elif hasattr(d, "draw"):
                d.draw(screen)
        super().render(screen, events)
        return True

    def _save(self):
        data = [

        ]
        for i in range(len(self.image_paths)):
            texture_path = self.image_paths[i]
            collision_points = self.points_state[i]
            entry = {
                "texture":texture_path,
                "collision":collision_points
            }
            data.append(entry)
        with open("tiles.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


tiles : list[dict[str,str | list[bool]]] = [{'texture': 'Overworld_Tileset_00_00'}, {'texture': 'Overworld_Tileset_00_01'}, {'texture': 'Overworld_Tileset_00_02'}, {'texture': 'Overworld_Tileset_00_03'}, {'texture': 'Overworld_Tileset_00_04'}, {'texture': 'Overworld_Tileset_00_05'}, {'texture': 'Overworld_Tileset_00_06'}, {'texture': 'Overworld_Tileset_00_07'}, {'texture': 'Overworld_Tileset_00_08'}, {'texture': 'Overworld_Tileset_00_09'}, {'texture': 'Overworld_Tileset_00_10'}, {'texture': 'Overworld_Tileset_00_11'}, {'texture': 'Overworld_Tileset_00_12'}, {'texture': 'Overworld_Tileset_00_13'}, {'texture': 'Overworld_Tileset_00_14'}, {'texture': 'Overworld_Tileset_00_15'}, {'texture': 'Overworld_Tileset_00_16'}, {'texture': 'Overworld_Tileset_00_17'}, {'texture': 'Overworld_Tileset_01_00'}, {'texture': 'Overworld_Tileset_01_01'}, {'texture': 'Overworld_Tileset_01_02'}, {'texture': 'Overworld_Tileset_01_03'}, {'texture': 'Overworld_Tileset_01_04'}, {'texture': 'Overworld_Tileset_01_05'}, {'texture': 'Overworld_Tileset_01_06'}, {'texture': 'Overworld_Tileset_01_07'}, {'texture': 'Overworld_Tileset_01_08'}, {'texture': 'Overworld_Tileset_01_09'}, {'texture': 'Overworld_Tileset_01_10'}, {'texture': 'Overworld_Tileset_01_11'}, {'texture': 'Overworld_Tileset_01_12'}, {'texture': 'Overworld_Tileset_01_13'}, {'texture': 'Overworld_Tileset_01_14'}, {'texture': 'Overworld_Tileset_01_15'}, {'texture': 'Overworld_Tileset_01_16'}, {'texture': 'Overworld_Tileset_01_17'}, {'texture': 'Overworld_Tileset_02_00'}, {'texture': 'Overworld_Tileset_02_01'}, {'texture': 'Overworld_Tileset_02_02'}, {'texture': 'Overworld_Tileset_02_03'}, {'texture': 'Overworld_Tileset_02_04'}, {'texture': 'Overworld_Tileset_02_05'}, {'texture': 'Overworld_Tileset_02_06'}, {'texture': 'Overworld_Tileset_02_07'}, {'texture': 'Overworld_Tileset_02_08'}, {'texture': 'Overworld_Tileset_02_09'}, {'texture': 'Overworld_Tileset_02_10'}, {'texture': 'Overworld_Tileset_02_11'}, {'texture': 'Overworld_Tileset_02_12'}, {'texture': 'Overworld_Tileset_02_13'}, {'texture': 'Overworld_Tileset_02_14'}, {'texture': 'Overworld_Tileset_02_15'}, {'texture': 'Overworld_Tileset_02_16'}, {'texture': 'Overworld_Tileset_02_17'}, {'texture': 'Overworld_Tileset_03_00'}, {'texture': 'Overworld_Tileset_03_01'}, {'texture': 'Overworld_Tileset_03_02'}, {'texture': 'Overworld_Tileset_03_03'}, {'texture': 'Overworld_Tileset_03_04'}, {'texture': 'Overworld_Tileset_03_05'}, {'texture': 'Overworld_Tileset_03_06'}, {'texture': 'Overworld_Tileset_03_07'}, {'texture': 'Overworld_Tileset_03_08'}, {'texture': 'Overworld_Tileset_03_09'}, {'texture': 'Overworld_Tileset_03_10'}, {'texture': 'Overworld_Tileset_03_11'}, {'texture': 'Overworld_Tileset_03_12'}, {'texture': 'Overworld_Tileset_03_13'}, {'texture': 'Overworld_Tileset_03_14'}, {'texture': 'Overworld_Tileset_03_15'}, {'texture': 'Overworld_Tileset_03_16'}, {'texture': 'Overworld_Tileset_03_17'}, {'texture': 'Overworld_Tileset_04_00'}, {'texture': 'Overworld_Tileset_04_01'}, {'texture': 'Overworld_Tileset_04_02'}, {'texture': 'Overworld_Tileset_04_03'}, {'texture': 'Overworld_Tileset_04_04'}, {'texture': 'Overworld_Tileset_04_05'}, {'texture': 'Overworld_Tileset_04_06'}, {'texture': 'Overworld_Tileset_04_07'}, {'texture': 'Overworld_Tileset_04_08'}, {'texture': 'Overworld_Tileset_04_09'}, {'texture': 'Overworld_Tileset_04_10'}, {'texture': 'Overworld_Tileset_04_11'}, {'texture': 'Overworld_Tileset_04_12'}, {'texture': 'Overworld_Tileset_04_13'}, {'texture': 'Overworld_Tileset_04_14'}, {'texture': 'Overworld_Tileset_04_15'}, {'texture': 'Overworld_Tileset_04_16'}, {'texture': 'Overworld_Tileset_04_17'}, {'texture': 'Overworld_Tileset_05_00'}, {'texture': 'Overworld_Tileset_05_01'}, {'texture': 'Overworld_Tileset_05_02'}, {'texture': 'Overworld_Tileset_05_03'}, {'texture': 'Overworld_Tileset_05_04'}, {'texture': 'Overworld_Tileset_05_05'}, {'texture': 'Overworld_Tileset_05_06'}, {'texture': 'Overworld_Tileset_05_07'}, {'texture': 'Overworld_Tileset_05_08'}, {'texture': 'Overworld_Tileset_05_09'}, {'texture': 'Overworld_Tileset_05_10'}, {'texture': 'Overworld_Tileset_05_11'}, {'texture': 'Overworld_Tileset_05_12'}, {'texture': 'Overworld_Tileset_05_13'}, {'texture': 'Overworld_Tileset_05_14'}, {'texture': 'Overworld_Tileset_05_15'}, {'texture': 'Overworld_Tileset_05_16'}, {'texture': 'Overworld_Tileset_05_17'}, {'texture': 'Overworld_Tileset_06_00'}, {'texture': 'Overworld_Tileset_06_01'}, {'texture': 'Overworld_Tileset_06_02'}, {'texture': 'Overworld_Tileset_06_03'}, {'texture': 'Overworld_Tileset_06_04'}, {'texture': 'Overworld_Tileset_06_05'}, {'texture': 'Overworld_Tileset_06_06'}, {'texture': 'Overworld_Tileset_06_07'}, {'texture': 'Overworld_Tileset_06_08'}, {'texture': 'Overworld_Tileset_06_09'}, {'texture': 'Overworld_Tileset_06_10'}, {'texture': 'Overworld_Tileset_06_11'}, {'texture': 'Overworld_Tileset_06_12'}, {'texture': 'Overworld_Tileset_06_13'}, {'texture': 'Overworld_Tileset_06_14'}, {'texture': 'Overworld_Tileset_06_15'}, {'texture': 'Overworld_Tileset_06_16'}, {'texture': 'Overworld_Tileset_06_17'}, {'texture': 'Overworld_Tileset_07_00'}, {'texture': 'Overworld_Tileset_07_01'}, {'texture': 'Overworld_Tileset_07_02'}, {'texture': 'Overworld_Tileset_07_03'}, {'texture': 'Overworld_Tileset_07_04'}, {'texture': 'Overworld_Tileset_07_05'}, {'texture': 'Overworld_Tileset_07_06'}, {'texture': 'Overworld_Tileset_07_07'}, {'texture': 'Overworld_Tileset_07_08'}, {'texture': 'Overworld_Tileset_07_09'}, {'texture': 'Overworld_Tileset_07_10'}, {'texture': 'Overworld_Tileset_07_11'}, {'texture': 'Overworld_Tileset_07_12'}, {'texture': 'Overworld_Tileset_07_13'}, {'texture': 'Overworld_Tileset_07_14'}, {'texture': 'Overworld_Tileset_07_15'}, {'texture': 'Overworld_Tileset_07_16'}, {'texture': 'Overworld_Tileset_07_17'}, {'texture': 'Overworld_Tileset_08_00'}, {'texture': 'Overworld_Tileset_08_01'}, {'texture': 'Overworld_Tileset_08_02'}, {'texture': 'Overworld_Tileset_08_03'}, {'texture': 'Overworld_Tileset_08_04'}, {'texture': 'Overworld_Tileset_08_05'}, {'texture': 'Overworld_Tileset_08_06'}, {'texture': 'Overworld_Tileset_08_07'}, {'texture': 'Overworld_Tileset_08_08'}, {'texture': 'Overworld_Tileset_08_09'}, {'texture': 'Overworld_Tileset_08_10'}, {'texture': 'Overworld_Tileset_08_11'}, {'texture': 'Overworld_Tileset_08_12'}, {'texture': 'Overworld_Tileset_08_13'}, {'texture': 'Overworld_Tileset_08_14'}, {'texture': 'Overworld_Tileset_08_15'}, {'texture': 'Overworld_Tileset_08_16'}, {'texture': 'Overworld_Tileset_08_17'}, {'texture': 'Overworld_Tileset_09_00'}, {'texture': 'Overworld_Tileset_09_01'}, {'texture': 'Overworld_Tileset_09_02'}, {'texture': 'Overworld_Tileset_09_03'}, {'texture': 'Overworld_Tileset_09_04'}, {'texture': 'Overworld_Tileset_09_05'}, {'texture': 'Overworld_Tileset_09_06'}, {'texture': 'Overworld_Tileset_09_07'}, {'texture': 'Overworld_Tileset_09_08'}, {'texture': 'Overworld_Tileset_09_09'}, {'texture': 'Overworld_Tileset_09_10'}, {'texture': 'Overworld_Tileset_09_11'}, {'texture': 'Overworld_Tileset_09_12'}, {'texture': 'Overworld_Tileset_09_13'}, {'texture': 'Overworld_Tileset_09_14'}, {'texture': 'Overworld_Tileset_09_15'}, {'texture': 'Overworld_Tileset_09_16'}, {'texture': 'Overworld_Tileset_09_17'}, {'texture': 'Overworld_Tileset_10_00'}, {'texture': 'Overworld_Tileset_10_01'}, {'texture': 'Overworld_Tileset_10_02'}, {'texture': 'Overworld_Tileset_10_03'}, {'texture': 'Overworld_Tileset_10_04'}, {'texture': 'Overworld_Tileset_10_05'}, {'texture': 'Overworld_Tileset_10_06'}, {'texture': 'Overworld_Tileset_10_07'}, {'texture': 'Overworld_Tileset_10_08'}, {'texture': 'Overworld_Tileset_10_09'}, {'texture': 'Overworld_Tileset_10_10'}, {'texture': 'Overworld_Tileset_10_11'}, {'texture': 'Overworld_Tileset_10_12'}, {'texture': 'Overworld_Tileset_10_13'}, {'texture': 'Overworld_Tileset_10_14'}, {'texture': 'Overworld_Tileset_10_15'}, {'texture': 'Overworld_Tileset_10_16'}, {'texture': 'Overworld_Tileset_10_17'}, {'texture': 'Overworld_Tileset_11_00'}, {'texture': 'Overworld_Tileset_11_01'}, {'texture': 'Overworld_Tileset_11_02'}, {'texture': 'Overworld_Tileset_11_03'}, {'texture': 'Overworld_Tileset_11_04'}, {'texture': 'Overworld_Tileset_11_05'}, {'texture': 'Overworld_Tileset_11_06'}, {'texture': 'Overworld_Tileset_11_07'}, {'texture': 'Overworld_Tileset_11_08'}, {'texture': 'Overworld_Tileset_11_09'}, {'texture': 'Overworld_Tileset_11_10'}, {'texture': 'Overworld_Tileset_11_11'}, {'texture': 'Overworld_Tileset_11_12'}, {'texture': 'Overworld_Tileset_11_13'}, {'texture': 'Overworld_Tileset_11_14'}, {'texture': 'Overworld_Tileset_11_15'}, {'texture': 'Overworld_Tileset_11_16'}, {'texture': 'Overworld_Tileset_11_17'}, {'texture': 'Overworld_Tileset_12_00'}, {'texture': 'Overworld_Tileset_12_01'}, {'texture': 'Overworld_Tileset_12_02'}, {'texture': 'Overworld_Tileset_12_03'}, {'texture': 'Overworld_Tileset_12_04'}, {'texture': 'Overworld_Tileset_12_05'}, {'texture': 'Overworld_Tileset_12_06'}, {'texture': 'Overworld_Tileset_12_07'}, {'texture': 'Overworld_Tileset_12_08'}, {'texture': 'Overworld_Tileset_12_09'}, {'texture': 'Overworld_Tileset_12_10'}, {'texture': 'Overworld_Tileset_12_11'}, {'texture': 'Overworld_Tileset_12_12'}, {'texture': 'Overworld_Tileset_12_13'}, {'texture': 'Overworld_Tileset_12_14'}, {'texture': 'Overworld_Tileset_12_15'}, {'texture': 'Overworld_Tileset_12_16'}, {'texture': 'Overworld_Tileset_12_17'}, {'texture': 'Dungeon_Tileset_00_00'}, {'texture': 'Dungeon_Tileset_00_01'}, {'texture': 'Dungeon_Tileset_00_02'}, {'texture': 'Dungeon_Tileset_00_03'}, {'texture': 'Dungeon_Tileset_00_04'}, {'texture': 'Dungeon_Tileset_00_05'}, {'texture': 'Dungeon_Tileset_00_06'}, {'texture': 'Dungeon_Tileset_00_07'}, {'texture': 'Dungeon_Tileset_00_08'}, {'texture': 'Dungeon_Tileset_00_09'}, {'texture': 'Dungeon_Tileset_00_10'}, {'texture': 'Dungeon_Tileset_00_11'}, {'texture': 'Dungeon_Tileset_01_00'}, {'texture': 'Dungeon_Tileset_01_01'}, {'texture': 'Dungeon_Tileset_01_02'}, {'texture': 'Dungeon_Tileset_01_03'}, {'texture': 'Dungeon_Tileset_01_04'}, {'texture': 'Dungeon_Tileset_01_05'}, {'texture': 'Dungeon_Tileset_01_06'}, {'texture': 'Dungeon_Tileset_01_07'}, {'texture': 'Dungeon_Tileset_01_08'}, {'texture': 'Dungeon_Tileset_01_09'}, {'texture': 'Dungeon_Tileset_01_10'}, {'texture': 'Dungeon_Tileset_01_11'}, {'texture': 'Dungeon_Tileset_02_00'}, {'texture': 'Dungeon_Tileset_02_01'}, {'texture': 'Dungeon_Tileset_02_02'}, {'texture': 'Dungeon_Tileset_02_03'}, {'texture': 'Dungeon_Tileset_02_04'}, {'texture': 'Dungeon_Tileset_02_05'}, {'texture': 'Dungeon_Tileset_02_06'}, {'texture': 'Dungeon_Tileset_02_07'}, {'texture': 'Dungeon_Tileset_02_08'}, {'texture': 'Dungeon_Tileset_02_09'}, {'texture': 'Dungeon_Tileset_02_10'}, {'texture': 'Dungeon_Tileset_02_11'}, {'texture': 'Dungeon_Tileset_03_00'}, {'texture': 'Dungeon_Tileset_03_01'}, {'texture': 'Dungeon_Tileset_03_02'}, {'texture': 'Dungeon_Tileset_03_03'}, {'texture': 'Dungeon_Tileset_03_04'}, {'texture': 'Dungeon_Tileset_03_05'}, {'texture': 'Dungeon_Tileset_03_06'}, {'texture': 'Dungeon_Tileset_03_07'}, {'texture': 'Dungeon_Tileset_03_08'}, {'texture': 'Dungeon_Tileset_03_09'}, {'texture': 'Dungeon_Tileset_03_10'}, {'texture': 'Dungeon_Tileset_03_11'}, {'texture': 'Dungeon_Tileset_04_00'}, {'texture': 'Dungeon_Tileset_04_01'}, {'texture': 'Dungeon_Tileset_04_02'}, {'texture': 'Dungeon_Tileset_04_03'}, {'texture': 'Dungeon_Tileset_04_04'}, {'texture': 'Dungeon_Tileset_04_05'}, {'texture': 'Dungeon_Tileset_04_06'}, {'texture': 'Dungeon_Tileset_04_07'}, {'texture': 'Dungeon_Tileset_04_08'}, {'texture': 'Dungeon_Tileset_04_09'}, {'texture': 'Dungeon_Tileset_04_10'}, {'texture': 'Dungeon_Tileset_04_11'}, {'texture': 'Dungeon_Tileset_05_00'}, {'texture': 'Dungeon_Tileset_05_01'}, {'texture': 'Dungeon_Tileset_05_02'}, {'texture': 'Dungeon_Tileset_05_03'}, {'texture': 'Dungeon_Tileset_05_04'}, {'texture': 'Dungeon_Tileset_05_05'}, {'texture': 'Dungeon_Tileset_05_06'}, {'texture': 'Dungeon_Tileset_05_07'}, {'texture': 'Dungeon_Tileset_05_08'}, {'texture': 'Dungeon_Tileset_05_09'}, {'texture': 'Dungeon_Tileset_05_10'}, {'texture': 'Dungeon_Tileset_05_11'}, {'texture': 'Dungeon_Tileset_06_00'}, {'texture': 'Dungeon_Tileset_06_01'}, {'texture': 'Dungeon_Tileset_06_02'}, {'texture': 'Dungeon_Tileset_06_03'}, {'texture': 'Dungeon_Tileset_06_04'}, {'texture': 'Dungeon_Tileset_06_05'}, {'texture': 'Dungeon_Tileset_06_06'}, {'texture': 'Dungeon_Tileset_06_07'}, {'texture': 'Dungeon_Tileset_06_08'}, {'texture': 'Dungeon_Tileset_06_09'}, {'texture': 'Dungeon_Tileset_06_10'}, {'texture': 'Dungeon_Tileset_06_11'}, {'texture': 'Dungeon_Tileset_07_00'}, {'texture': 'Dungeon_Tileset_07_01'}, {'texture': 'Dungeon_Tileset_07_02'}, {'texture': 'Dungeon_Tileset_07_03'}, {'texture': 'Dungeon_Tileset_07_04'}, {'texture': 'Dungeon_Tileset_07_05'}, {'texture': 'Dungeon_Tileset_07_06'}, {'texture': 'Dungeon_Tileset_07_07'}, {'texture': 'Dungeon_Tileset_07_08'}, {'texture': 'Dungeon_Tileset_07_09'}, {'texture': 'Dungeon_Tileset_07_10'}, {'texture': 'Dungeon_Tileset_07_11'}, {'texture': 'Dungeon_Tileset_08_00'}, {'texture': 'Dungeon_Tileset_08_01'}, {'texture': 'Dungeon_Tileset_08_02'}, {'texture': 'Dungeon_Tileset_08_03'}, {'texture': 'Dungeon_Tileset_08_04'}, {'texture': 'Dungeon_Tileset_08_05'}, {'texture': 'Dungeon_Tileset_08_06'}, {'texture': 'Dungeon_Tileset_08_07'}, {'texture': 'Dungeon_Tileset_08_08'}, {'texture': 'Dungeon_Tileset_08_09'}, {'texture': 'Dungeon_Tileset_08_10'}, {'texture': 'Dungeon_Tileset_08_11'}, {'texture': 'Dungeon_Tileset_09_00'}, {'texture': 'Dungeon_Tileset_09_01'}, {'texture': 'Dungeon_Tileset_09_02'}, {'texture': 'Dungeon_Tileset_09_03'}, {'texture': 'Dungeon_Tileset_09_04'}, {'texture': 'Dungeon_Tileset_09_05'}, {'texture': 'Dungeon_Tileset_09_06'}, {'texture': 'Dungeon_Tileset_09_07'}, {'texture': 'Dungeon_Tileset_09_08'}, {'texture': 'Dungeon_Tileset_09_09'}, {'texture': 'Dungeon_Tileset_09_10'}, {'texture': 'Dungeon_Tileset_09_11'}, {'texture': 'Dungeon_Tileset_10_00'}, {'texture': 'Dungeon_Tileset_10_01'}, {'texture': 'Dungeon_Tileset_10_02'}, {'texture': 'Dungeon_Tileset_10_03'}, {'texture': 'Dungeon_Tileset_10_04'}, {'texture': 'Dungeon_Tileset_10_05'}, {'texture': 'Dungeon_Tileset_10_06'}, {'texture': 'Dungeon_Tileset_10_07'}, {'texture': 'Dungeon_Tileset_10_08'}, {'texture': 'Dungeon_Tileset_10_09'}, {'texture': 'Dungeon_Tileset_10_10'}, {'texture': 'Dungeon_Tileset_10_11'}, {'texture': 'Dungeon_Tileset_11_00'}, {'texture': 'Dungeon_Tileset_11_01'}, {'texture': 'Dungeon_Tileset_11_02'}, {'texture': 'Dungeon_Tileset_11_03'}, {'texture': 'Dungeon_Tileset_11_04'}, {'texture': 'Dungeon_Tileset_11_05'}, {'texture': 'Dungeon_Tileset_11_06'}, {'texture': 'Dungeon_Tileset_11_07'}, {'texture': 'Dungeon_Tileset_11_08'}, {'texture': 'Dungeon_Tileset_11_09'}, {'texture': 'Dungeon_Tileset_11_10'}, {'texture': 'Dungeon_Tileset_11_11'}, {'texture': 'Dungeon_Tileset_12_00'}, {'texture': 'Dungeon_Tileset_12_01'}, {'texture': 'Dungeon_Tileset_12_02'}, {'texture': 'Dungeon_Tileset_12_03'}, {'texture': 'Dungeon_Tileset_12_04'}, {'texture': 'Dungeon_Tileset_12_05'}, {'texture': 'Dungeon_Tileset_12_06'}, {'texture': 'Dungeon_Tileset_12_07'}, {'texture': 'Dungeon_Tileset_12_08'}, {'texture': 'Dungeon_Tileset_12_09'}, {'texture': 'Dungeon_Tileset_12_10'}, {'texture': 'Dungeon_Tileset_12_11'}]

if __name__ == "__main__":
    image_paths = []
    for tile in tiles:
        image_paths.append(tile["texture"])
    initial_points = []
    with open("tiles.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        initial_points.append(entry["collision"])
    pygameui.setup(CollisionEditor(image_paths,initial_points),"Collision Editor")