# TileWorld (PyGame) – Client, Editor & Online-Anbindung

Ein 2D-Spiel/Editor auf Basis von **PyGame** mit
- Online-Client (UDP) für Position/Chat/Entities,
- Level-Renderer inkl. **Tile-Editor** (mit „Kachelauswahl-Overlay“),
- einfacher **Animations-Pipeline** über JSON,
- Login/Registration gegen einen HTTP-API-Server.

## Inhaltsverzeichnis
- [Features](#features)
- [Schnellstart](#schnellstart)
- [Abhängigkeiten](#abhängigkeiten)
- [Projektstruktur](#projektstruktur)
- [Architektur in Kürze](#architektur-in-kürze)
- [Level & Tiles](#level--tiles)
- [Animationen](#animationen)
- [Entities](#entities)
- [Netzwerk & Protokoll](#netzwerk--protokoll)
- [Bedienung & Shortcuts](#bedienung--shortcuts)
- [Troubleshooting](#troubleshooting)
- [Lizenz](#lizenz)

---

## Features

- **Login/Registrierung** gegen REST-API; Token wird gespeichert und für den Online-Client genutzt.  
- **Tile-basierte Welt** mit Chunks, Speichern/Laden aus `dim/<dimension>.json`.  
- **Integrierter Editor:**
  - **Kachel-Overlay** mit Scrollen (W/A/S/D), Auswahlbereich (Drag), optionaler Entity-Vorschau.
  - **Kachel-Eigenschaften** (z. B. Door/Teleport) können per UI bearbeitet werden.
  - **Collision-Editor** im 3×3-Raster pro Tile, Export nach `tiles.json`.
- **Animationen** per `textures/<name>.json` (Sprites + `wait`), automatische Auswahl des Frames.
- **Minecraft-Style Farben/Formatierungen** in Text (z. B. `§e`, `§l`, `§n`, `§r`).

---

## Schnellstart

### 1) Voraussetzungen
- Python 3.10+
- Systempakete für SDL/pygame (je nach OS)
- Assets-Ordner (`textures/`, `tiles/`, `font/`, `dim/`) vorhanden

### 2) Installation
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

**Minimaler Satz an PyPI-Packages:**
```
simple-pygame-ui
pygame
requests
```

> simple-pygame-ui auch bekannt als PyGameUI wurde von mir selber entwickelt und auf PyPI hochgeladen.

### 3) Starten

Standardstart (Fenstername per Arg):
```bash
python main.py "TileWorld"
```

- Das Programm öffnet das **Login-Menü**. Benutzer/Passwort eingeben, „Login“. Bei Erfolg wird in das **Hauptmenü** gewechselt und anschließend die **Welt** geladen.
- Alternativ: Übergabe von Login-Daten über CLI-Argumente (E-Mail und Passwort). Wenn vorhanden, startet direkt ein **LoadingScreen** mit Login-Versuch.

**Hinweis zur Fenstergröße/FPS:** Die Basis-Loop wird in `main.py` initialisiert; `scene_handler` verwaltet Kamera/Delta/FPS.

---

## Abhängigkeiten

- **PyGame** – Rendering, Input, Cursor, Fonts  
- **Requests** – HTTP-Login/Register (REST)  
- Interne Module:
  - **level_renderer.TileWorld** – Welt/Editor/Chunks/Chat/Speichern+Laden
  - **custom_elements.EditorTileOverlay** – Kachel-/Entity-Auswahl
  - **collision_editor.CollisionEditor** – 3×3 Kollision-Tool, Export `tiles.json`
  - **custom_renderer.Renderer** – Text mit §-Codes
  - **animation_handler** – JSON-Animationen → `pygame.Surface`
  - **entities** – Factory & Basistypen (z. B. Spinner)
  - **byte_buffer.ByteBuffer** – Big-Endian-Reader für Netzwerkdaten (String/Int/Bool)
  - **menus** – Login/Register Flows (HTTP)

---

## Projektstruktur

```
.
├─ main.py                 # App-Entry, Game-Loop, Fenster
├─ menus.py                # Login/Registrierung/Loading-Screen (HTTP)
├─ level_renderer.py       # TileWorld-Scene: Welt/Editor/Chunks/Netz
├─ custom_elements.py      # EditorTileOverlay (Kachelauswahl)
├─ collision_editor.py     # 3×3 Kollision-Tool, Export tiles.json
├─ custom_renderer.py      # Minecraft-Style Textfarben/-formatierung
├─ animation_handler.py    # JSON-Animationsloader
├─ entities.py             # Entity-Basistyp + Factory
├─ byte_buffer.py          # Längen-/BE-Reader für Netzwerkbytes
├─ gen_tile_list.py        # Hilfsskript: Liste von Tile-Namen generieren
├─ dim/                    # gespeicherte Dimensionen (*.json)
├─ textures/               # Texturen + <name>.json Animationsbeschreibungen
├─ tiles/                  # Kachelbilder (PNG)
└─ tiles.json              # Kollisions-/Tile-Metadaten (vom Editor)
```

---

## Architektur in Kürze

### Scenes & Rendering
- **`TileWorld`** ist die zentrale Scene. Sie lädt **Chunks** (Dictionary `(x,y) → TileChunk`), hält Kamera/Spielerposition, und rendert Tiles, Entities & UI. Speichern/Laden nutzt ein `meta`-Objekt (Floor-Tile, Kamera-Regel, Chunk-Größe, Render-Distanz) plus Liste aktiver/nicht-leerer Chunks.  
- **Caching:** Texturen werden skaliert gecacht; Tilegröße richtet sich dynamisch nach Fenstergröße.

### UI/Editor
- **EditorTileOverlay** (rechts) zeigt ein scrollbares Raster des Tilesets (18 Spalten). Auswahl per Klick/Drag; Umschalten auf **Entity-Modus** möglich. Scrollen mit **W/A/S/D**.  
- **CollisionEditor** zeichnet pro Tile ein **3×3-Raster** mit klickbaren Punkten (rot/blau) und speichert das Ergebnis in **`tiles.json`**.

### Login & HTTP
- **`menus.login`** ruft `POST /api/auth/login` auf; bei Erfolg wird der **Token** gespeichert und weiter navigiert. **Register** analog (zusätzliche Player-Metadaten).

---

## Level & Tiles

### Tile-Daten
- **`TileChunk`** verwaltet eine flache Liste von Tile-IDs; wahlweise auch Tupel `(id, data)` für Tiles mit Metadaten (z. B. Door). Getter abstrahieren ID vs. `(ID, Data)` und liefern `get_type()`/`get_data()`.  
- **Speichern:** `TileWorld.save_world()` schreibt `dim/<dimension>.json` mit `meta` und **nur** den Chunks, die nicht komplett leer sind.  
- **Laden:** `TileWorld.load_world()` stellt Chunks, `floor`, `camera_rule`, `chunk_size`, `render_distance` wieder her.

### Kachellisten
- Ein Hilfsskript erzeugt eine Liste aus vordefinierten Tileset-Namen (`Overworld_Tileset_XX_YY`, `Dungeon_Tileset_XX_YY`).

### Türen/Teleport
- Es gibt einen **`DoorType`** (Tile-Typ), der eine **Dimension + Ziel-Koordinate** aus den Tile-Metadaten liest und beim Betreten überblendet/teleportiert. (Bearbeitung der Werte erfolgt über den UI-Dialog „Modify“)

---

## Animationen

- **`animation_handler.get_texture(name, tick, animation)`** lädt **`textures/<name>.json`** (falls vorhanden), ermittelt aus `animations[animation]` die **Frames** und `wait`, und gibt den **aktuellen Frame** als `Surface` zurück. Fallback: direktes Laden `textures/<animation>.png`.

**Beispiel `textures/spinner/spinner.json`** (Schema):
```json
{
  "animations": {
    "0": { "wait": 4, "textures": ["spinner_0","spinner_1","spinner_2","spinner_3"] }
  }
}
```

---

## Entities

- **Basistyp/Protokoll:** `Entity` liest Animation/Position/Richtung/Dimension über einen **ByteBuffer** aus dem Netzwerk (BE-Int, Längen-Strings). `render()` und `update()` sind überschreibbar.  
- **Factory:** `create_new_entity(entity_type, uuid, buffer)` mappt String-Typen auf Klassen (siehe `entity_types`).  
- **Beispiel:** `SpinnerEntity` rendert eine animierte Textur via `animation_handler`.

---

## Netzwerk & Protokoll

> Kurzüberblick (Client-Seite).  
> Der Code nutzt einen **UDP-Client** mit **Opcode-Handlers** und einem **ByteBuffer** für Big-Endian-Parsing.  
> Wichtige Strukturen:

- **ByteBuffer**
  - `get_string()` liest **4-Byte Längenpräfix (BE)** gefolgt von UTF-8-Bytes.  
  - `get_int()` liest **4-Byte BE-Integer** (signed).  
  - `get_bool()` liest 1-Byte Boolean.

- **TileWorld → Online**  
  Beim Szenenwechsel/Join/Close werden **Opcodes** mit `id`/`dimension` gesendet (siehe `initialize_packet()`/`close()`). Die Scene hält außerdem Chat-Eingabe und Serverdatenanzeigen bereit.

---

## Bedienung & Shortcuts

- **Editor umschalten:** UI-Buttons oben links (Stift / Entities / Save) – werden per `toggle_editor()` sichtbar/unsichtbar gemacht.  
- **Kachelauswahl:** Rechts im **EditorTileOverlay** – **W/A/S/D** scrollt die Ansicht, Klick/Drag markiert einen Bereich.  
- **Kachel-Eigenschaften** (z. B. Door): „Modify“ → Werte editieren → „Save“. (speichert in den Chunk-Tiles eine `(id, data)` Struktur)  
- **Collision-Editor:** Punkte anklicken (rot ⇄ blau), `Save` schreibt `tiles.json`.  
- **Chat:** Texteingabe unten; Versand/Handling im `TileWorld`/Online-Code.  
- **Textfarben:** `§0..§f` und Formatierungen `§l` (fett), `§i` (italic), `§n` (underline), `§r` (reset).

---

## Troubleshooting

- **Schwarzes Fenster / fehlende Texturen:** Prüfe, ob `textures/` und `tiles/` existieren und Pfade stimmen. `TileWorld.get_texture()` lädt `<prefix><name>.png` und cached skaliert.  
- **Keine Tiles im Overlay:** Stelle sicher, dass `tiles.json` vorliegt oder die interne Liste/Generierung (`gen_tile_list.py`) korrekt eingebunden ist.  
- **Login schlägt fehl:** HTTP-Endpoint/Port erreichbar? Siehe Konfiguration und Konsolen-Logs.  
- **Netzwerk-Desync/IDs leer:** Der Online-Client erwartet gültiges `id`/Token und konsistente Opcodes. Byte-Order muss **Big-Endian** sein.

---

## Lizenz

*(Bitte ergänzen – z. B. MIT, GPL, proprietär.)*

---

### Anhang: Nützliche Skripte

- **Kachelliste generieren**
  ```bash
  python gen_tile_list.py > tiles_seed.json
  ```
  (Erzeugt eine Liste aller Overworld/Dungeon-Tiles; kann als Grundlage für `tiles.json` dienen.)
