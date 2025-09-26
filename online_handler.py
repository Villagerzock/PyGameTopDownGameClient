import socket
import struct
import sys
import threading
from typing import Callable, Optional, List, Tuple
from uuid import UUID

from better_math import Vector2i

from byte_buffer import ByteBuffer
from player import Player

Addr = Tuple[str, int]
Handler = Callable[[bytes, Addr], None]

id : str = ""


class UdpClient:
    def __init__(self, server_ip: str, server_port: int = 9999, recv_timeout: float = 0.5):
        self.server_ip = server_ip
        self.server_port = server_port
        self.handlers: List[Optional[Handler]] = []
        self.stop_event = threading.Event()

        # Ein einziges Socket zum Senden & Empfangen
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Beliebigen lokalen Port wählen, damit Antworten ankommen
        self.sock.bind(("0.0.0.0", int(sys.argv[2])))
        self.sock.settimeout(recv_timeout)

        self._thr = threading.Thread(target=self._worker, name="udp-listener", daemon=True)
        self._thr.start()

    # ---------- Öffentliche API ----------

    def add_handler(self, fn: Handler) -> int:
        """Hängt einen Handler hinten an und gibt dessen Index zurück."""
        self.handlers.append(fn)
        return len(self.handlers) - 1

    def set_handler(self, index: int, fn: Handler) -> None:
        """Setzt/überschreibt Handler an bestimmtem Index; füllt Lücken mit None."""
        if index < 0:
            raise ValueError("index muss >= 0 sein")
        if index >= len(self.handlers):
            self.handlers += [None] * (index - len(self.handlers) + 1)
        self.handlers[index] = fn

    def join_server(self, playername: str, timeout: float = 2.0) -> int:
        """
		Sendet ein UDP-Paket an den Server:
		  Byte 0:  0x00
		  Byte 1-4: UINT32 (Big-Endian) = Länge des UTF-8-Namens
		  Rest:     UTF-8-Bytes des Namens
		Gibt die Anzahl gesendeter Bytes zurück.
		"""
        name_bytes = playername.encode("utf-8")
        pkt = struct.pack("!BI", 0x00, len(name_bytes)) + name_bytes

        # Optional separat ein kurzzeitiges Timeout setzen (nur fürs Senden/erste Antwort, falls gewünscht)
        old_timeout = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        try:
            sent = self.sock.sendto(pkt, (self.server_ip, self.server_port))
            return sent
        finally:
            self.sock.settimeout(old_timeout)

    def send_opcode(self, opcode: int, payload: bytes = b"") -> int:
        """Hilfsfunktion: schickt beliebiges Opcode+Payload (Client → Server)."""
        if not (0 <= opcode <= 255):
            raise ValueError("opcode muss zwischen 0..255 liegen")
        pkt = struct.pack("!B", opcode) + payload
        return self.sock.sendto(pkt, (self.server_ip, self.server_port))

    def close(self):
        """Sauber beenden."""
        self.stop_event.set()
        try:
            self.sock.close()
        except OSError:
            pass
        self._thr.join(timeout=2.0)

    # ---------- Intern: Listener-Thread ----------

    def _worker(self):
        try:
            while not self.stop_event.is_set():
                try:
                    data, addr = self.sock.recvfrom(2048)
                except socket.timeout:
                    continue
                except OSError:
                    break  # Socket ist zu

                if not data:
                    continue

                opcode = data[0]
                payload = data[1:]

                # Handler lookup
                if opcode < len(self.handlers) and self.handlers[opcode] is not None:
                    try:
                        self.handlers[opcode](payload, addr)
                    except Exception as e:
                        # Du kannst hier Logging einbauen
                        print(f"[Client] Handler[{opcode}] Fehler: {e}")
                else:
                    # Kein passender Handler vorhanden → ignorieren oder loggen
                    print(f"[Client] Unbekannter Opcode {opcode} von {addr}, {len(payload)} Bytes")
        finally:

            payload = struct.pack("!I", len(id)) + id.encode("utf-8")
            self.send_opcode(0x02, payload)

            print("[Client] Listener beendet.")


import struct, time, threading, math

SCALE_POS = 1000  # meter → millimeter
SCALE_VEL = 1000  # m/s → mm/s

import struct, time, math


class PosSender2D:
    def __init__(self, udp_client, send_hz=15, pos_eps_m=0.02):
        self.c = udp_client
        self.period = 1.0 / send_hz
        self.pos_eps = pos_eps_m
        self.acc = 0.0
        self.seq = 0
        self.last_sent = None  # (x, y)
        self._last_hb = 0.0
        self.hb_interval = 0.1  # 250 ms
        self._now = time.monotonic

    def tick(self, dt, x, y,dir, animation, animationTick):
        global id
        if id == "":
            return
        # dt kommt aus deinem Game-Loop / deiner Scene
        self.acc += dt
        if self.acc < self.period:
            return  # noch nicht dran
        self.acc -= self.period

        now = self._now()
        send_change = False
        if self.last_sent is None:
            send_change = True
        else:
            lx, ly = self.last_sent
            if math.hypot(x - lx, y - ly) > self.pos_eps:
                send_change = True

        send_hb = (now - self._last_hb) >= self.hb_interval

        if not (send_change or send_hb):
            return

        self.seq = (self.seq + 1) & 0xFFFF
        t_ms = int(self._now() * 1000)


        # 0x10 | seq | t_ms | x_mm | y_mm
        payload = struct.pack("!I",len(id)) + id.encode("utf-8") + struct.pack("!H I i i i i i", self.seq, t_ms, x, y, dir,animation,animationTick)
        self.c.send_opcode(0x01, payload)

        self.last_sent = (x, y)
        if send_hb:
            self._last_hb = now


client = UdpClient("localhost", 6969)
throttled_sender = PosSender2D(client)
online_players : dict[str,Player] = {}


def join_answer_packet(bytes, addr):
    global id
    if id:
        return
    length = int.from_bytes(bytes[1:4], byteorder="little")
    id = bytes[4:length + 5].decode("utf-8")

    print(f"UUID: {id}")

def update_player(bytes, addr):
    buffer = ByteBuffer(bytes)
    player_uuid = buffer.get_string()
    name = buffer.get_string()
    if name == sys.argv[1]:
        return
    x = buffer.get_int()
    y = buffer.get_int()
    dir = buffer.get_int()
    animation = buffer.get_int()
    animationTick = buffer.get_int()
    old_pos = Vector2i(0,0)
    if online_players.get(player_uuid):
        old_pos = online_players[player_uuid].position
    p = Player(player_uuid, name, Vector2i(x, y),old_pos,dir,animation,animationTick)
    online_players[player_uuid] = p
def player_disconnected(bytes, addr):
    buffer = ByteBuffer(bytes)
    player_uuid = buffer.get_string()
    online_players.__delitem__(player_uuid)

client.add_handler(join_answer_packet)
client.add_handler(update_player)
client.add_handler(player_disconnected)

