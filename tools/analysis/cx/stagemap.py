"""Static stage-map renderer for Rockman CX (RM2 level format, decoded from the engine; see docs/research/cx/stages_1.md).

Level format of a 16 KB stage bank (stage & 7 -> 8 KB banks 2n, 2n+1 at $8000-$BFFF), shared by the robot-master
stage and its fortress/opening partner (room numbers are one shared space):
    $8000 + 4*b   32x32 block b = four 16x16 tiles (TL, BL, TR, BR); 16x16 tile m = CHR tiles (4m..4m+3) & $FF,
                  column-major (4m TL, 4m+1 BL, 4m+2 TR, 4m+3 BR)                      [code $C968-$C9AB]
    $8400 + b     attribute byte of block b (2-bit palettes of its four 16x16 tiles)    [code $C979]
    $8500 + 64*r  room r: 8 columns x 8 blocks, column-major (byte i = column i>>3, row i&7) [code $C9E4, restart table]
    $B400 + k     segment k: low 5 bits = rooms-1; exit flags $80 = up (climb off the top), $20 = right (walk
                  off the last room), $40 = down (fall/climb off the bottom); none = shutter or end [code $3C:8284-$82A7, $8925]
    $B600/$B700/$B800/$B900 + i   enemy i: room, x, y, object id (256 slots, $FF room = end)  [code $D764]
    $BA00/$BA40/$BA80/$BAC0 + i   special object i: room, x, y, id (64 slots; $2E/$2F shutters, $B5-$BB items,
                  $BB = item 6 = heart tank)                                              [code $D7DE]
    $BB06..       checkpoint/restart tables (see cheats.md section 5)

    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx')
    import stagemap as sm
    rom = sm.load_rom()
    segs = sm.segments(rom, 0)                     # [(first_room, last_room, flags), ...] from seg 0 / room 0
    pos = sm.layout(rom, 15, 0x17, 0x29, anchor=(0x17, 0x11))   # room -> (col, row); anchor = (room, seg)
    im = sm.render_map(rom, 0, 0x00, 0x18, chr_states=[(0, 'build/research/cx/states/cheat_man.state')],
                       overlay=True)                # PIL image; CHR+palette taken from live savestates
    im.save('map.png')

CHR and palettes are not decoded from ROM: they are taken from savestates (one Emu per process, so pass an existing Emu
as emu= if you have one). chr_states = [(first_room, state_path), ...]: each room uses the last entry whose first_room
is <= the room, so give one state per segment whose tiles differ.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools', 'analysis'))
import numpy as np
from PIL import Image, ImageDraw


def load_rom(path=os.path.join(REPO, 'roms', 'cx_en.nes')):
    return open(path, 'rb').read()[16:]


def bank(rom, stage):
    s = stage & 7
    return rom[s * 0x4000:(s + 1) * 0x4000]


def rd(b, a): return b[a - 0x8000]


def segments(rom, stage, anchor=(0, 0), count=0x60, inplace=()):
    """[(first_room, last_room, flags)] for segments anchor_seg.. (rooms counted from anchor_room).
    The game computes each segment's rooms from the previous one at every transition ($14 = old $15 + 1,
    $15 = $14 + len), and checkpoints set them directly, so anchor at a stage start / checkpoint.
    inplace = segment indices that an event script enters without moving on a room (they start in the last
    room of the previous segment; e.g. Cheat Man's segment 5)."""
    b = bank(rom, stage); out = []; r, k0 = anchor
    for k in range(k0, k0 + count):
        v = rd(b, 0xB400 + k)
        if v == 0xFF: break
        if k in inplace: r -= 1
        n = (v & 0x1F) + 1; out.append((r, r + n - 1, v & 0xE0)); r += n
    return out


def exit_dir(f, prefer='^>v'):
    """'^' up ($80), '>' right ($20), 'v' down ($40), '|' none (shutter / end); several bits: first in prefer."""
    have = {'^': f & 0x80, '>': f & 0x20, 'v': f & 0x40}
    for c in prefer:
        if have[c]: return c
    return '|'


def room_blocks(rom, stage, room):
    b = bank(rom, stage); base = 0x8500 + 64 * room
    return [rd(b, base + i) for i in range(64)]


def room_tiles(rom, stage, room):
    """32x32 nametable-like arrays (tile index, palette 0-3)."""
    b = bank(rom, stage); tiles = np.zeros((32, 32), np.int32); pals = np.zeros((32, 32), np.int32)
    for i, bid in enumerate(room_blocks(rom, stage, room)):
        bx, by = i >> 3, i & 7
        d = [rd(b, 0x8000 + 4 * bid + k) for k in range(4)]
        at = rd(b, 0x8400 + bid)
        for k, (dx, dy) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
            m = d[k]; pal = (at >> ((dy * 2 + dx) * 2)) & 3   # attribute: TL, TR, BL, BR in bits 0-1, 2-3, 4-5, 6-7
            for j, (ex, ey) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
                y, x = by * 4 + dy * 2 + ey, bx * 4 + dx * 2 + ex
                tiles[y, x] = (4 * m + j) & 0xFF; pals[y, x] = pal
    return tiles, pals


def enemies(rom, stage, special=False):
    """[(room, x, y, id)] from the enemy table ($B600..) or the special-object table ($BA00..)."""
    b = bank(rom, stage); out = []
    if special:
        for i in range(64):
            r = rd(b, 0xBA00 + i)
            if r == 0xFF: break
            out.append((r, rd(b, 0xBA40 + i), rd(b, 0xBA80 + i), rd(b, 0xBAC0 + i)))
    else:
        for i in range(256):
            r = rd(b, 0xB600 + i)
            if r == 0xFF: break
            out.append((r, rd(b, 0xB700 + i), rd(b, 0xB800 + i), rd(b, 0xB900 + i)))
    return out


def layout(rom, stage, first, last, anchor=None, override=None, inplace=()):
    """room -> (col, row): segments laid out right / up / down by their exit flags, starting at anchor
    (room, seg) (default (first, 0)).  override = {seg_index: '^' / '>' / 'v'} for multi-bit segments."""
    pos = {}; col = row = 0
    override = override or {}
    for k, (a, z, f) in enumerate(segments(rom, stage, anchor or (first, 0), inplace=inplace)):
        if a > last: break
        if (anchor or (first, 0))[1] + k in inplace: col -= 1
        for r in range(a, z + 1):
            pos[r] = (col, row)
            if r != z: col += 1
        kk = (anchor or (first, 0))[1] + k
        d = override.get(kk) or exit_dir(f)
        if d == '^': row -= 1
        elif d == 'v': row += 1
        else: col += 1
    pos = {k: v for k, v in pos.items() if first <= k <= last}
    mc = min(c for c, _ in pos.values()); mr = min(r for _, r in pos.values())
    return {k: (c - mc, r - mr) for k, (c, r) in pos.items()}


_E = None
def _emu():
    global _E
    if _E is None:
        from emu import Emu
        _E = Emu(os.path.join(REPO, 'roms', 'cx_en.nes'))
    return _E


def ppu_from_state(path, emu=None, frames=1):
    e = emu or _emu(); e.load(path); e.run(frames); p = e.ppu()
    return p['chr'], p['pal'], (256 if p['ctrl'] & 0x10 else 0)


def _render_room(tiles, pals, chr_, pal, base):
    from emu import nes_rgb
    cache = {}
    img = np.zeros((240, 256, 3), np.uint8)
    for y in range(30):
        for x in range(32):
            key = (tiles[y, x], pals[y, x])
            if key not in cache:
                t = chr_[(base + key[0]) * 16:(base + key[0]) * 16 + 16]
                p4 = [nes_rgb(pal[0])] + [nes_rgb(pal[key[1] * 4 + k]) for k in (1, 2, 3)]
                px = np.zeros((8, 8, 3), np.uint8)
                for yy in range(8):
                    lo, hi = t[yy], t[yy + 8]
                    for xx in range(8):
                        px[yy, xx] = p4[((lo >> (7 - xx)) & 1) | (((hi >> (7 - xx)) & 1) << 1)]
                cache[key] = px
            img[y * 8:y * 8 + 8, x * 8:x * 8 + 8] = cache[key]
    return img


def render_room(rom, stage, room, chr_, pal, base):
    t, p = room_tiles(rom, stage, room)
    return Image.fromarray(_render_room(t, p, chr_, pal, base))


def render_map(rom, stage, first, last, chr_states, overlay=True, emu=None, scale=1, labels=True, pos=None, anchor=None):
    """Whole-stage map, rooms first..last, laid out by segment flags. Overlay: red = enemy ids, yellow = special."""
    pos = pos or layout(rom, stage, first, last, anchor)
    ppus = sorted(((r, ppu_from_state(s, emu)) for r, s in chr_states), key=lambda t: t[0])
    W = (max(c for c, _ in pos.values()) + 1) * 256; H = (max(r for _, r in pos.values()) + 1) * 240
    im = Image.new('RGB', (W, H), (40, 40, 40)); dr = ImageDraw.Draw(im)
    for room, (c, r) in pos.items():
        src = [p for fr, p in ppus if fr <= room] or [ppus[0][1]]
        chr_, pal, base = src[-1]
        im.paste(render_room(rom, stage, room, chr_, pal, base), (c * 256, r * 240))
        if labels:
            dr.rectangle((c * 256, r * 240, c * 256 + 34, r * 240 + 10), fill=(0, 0, 0))
            dr.text((c * 256 + 2, r * 240), 'r%02X' % room, fill=(255, 255, 255))
    if overlay:
        for special, colr in ((False, (255, 60, 60)), (True, (255, 230, 0))):
            for (room, x, y, oid) in enemies(rom, stage, special):
                if room not in pos: continue
                c, r = pos[room]; px, py = c * 256 + x, r * 240 + y
                dr.rectangle((px - 3, py - 3, px + 3, py + 3), outline=colr)
                dr.text((px + 4, py - 5), '%02X' % oid, fill=colr)
    if scale != 1: im = im.resize((int(W * scale), int(H * scale)), Image.NEAREST)
    return im
