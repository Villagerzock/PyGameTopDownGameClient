import pygame
from better_math import Vector2i

# Mapping von Minecraft-Farbcodes zu RGB
MC_COLORS = {
    '0': (0, 0, 0),  # Schwarz
    '1': (0, 0, 170),  # Dunkelblau
    '2': (0, 170, 0),  # Dunkelgrün
    '3': (0, 170, 170),  # Dunkel-Aqua
    '4': (170, 0, 0),  # Dunkelrot
    '5': (170, 0, 170),  # Lila
    '6': (255, 170, 0),  # Gold
    '7': (170, 170, 170),  # Grau
    '8': (85, 85, 85),  # Dunkelgrau
    '9': (85, 85, 255),  # Blau
    'a': (85, 255, 85),  # Hellgrün
    'b': (85, 255, 255),  # Aqua
    'c': (255, 85, 85),  # Hellrot
    'd': (255, 85, 255),  # Pink
    'e': (255, 255, 85),  # Gelb
    'f': (255, 255, 255),  # Weiß
}


class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def text(self, text: str, font: str, pos: Vector2i, size: int, color=(0, 0, 0), alpha: float = 1.0,upside_down : bool = False):
        """Zeichnet Text mit Minecraft-Farb- und Formatierungscodes (§c, §e, §f, §i, §n, §r)"""
        target = self.screen
        base_font = pygame.font.SysFont(font, size)

        x, y = int(pos.x), int(pos.y)
        lines = text.split("\n")
        line_h = base_font.get_linesize()
        if upside_down:
            lines.reverse()
        for line in lines:
            if line == "":
                if upside_down:
                    y -= line_h
                else:
                    y += line_h
                continue

            curr_color = color
            bold = False
            italic = False
            underline = False

            buffer = ""
            px = x
            i = 0
            while i < len(line):
                if line[i] == "§" and i + 1 < len(line):
                    # render vorherigen Textblock
                    if buffer:
                        fnt = pygame.font.SysFont(font, size)
                        fnt.set_bold(bold)
                        fnt.set_italic(italic)
                        fnt.set_underline(underline)
                        surf = fnt.render(buffer, True, curr_color)
                        target.blit(surf, (px, y))
                        px += surf.get_width()
                        buffer = ""
                    code = line[i + 1].lower()
                    # Farben
                    if code in MC_COLORS:
                        curr_color = MC_COLORS[code]
                    # Formatierungen
                    elif code == "l":  # fett
                        bold = True
                    elif code == "i":  # italic
                        italic = True
                    elif code == "n":  # underline
                        underline = True
                    elif code == "r":  # reset alles
                        curr_color = color
                        bold = italic = underline = False
                    i += 2
                    continue
                else:
                    buffer += line[i]
                    i += 1

            # Rest rendern
            if buffer:
                fnt = pygame.font.SysFont(font, size)
                fnt.set_bold(bold)
                fnt.set_italic(italic)
                fnt.set_underline(underline)
                surf = fnt.render(buffer, True, curr_color)
                surf.set_alpha(int(alpha * 255))
                target.blit(surf, (px, y))

            y += line_h
