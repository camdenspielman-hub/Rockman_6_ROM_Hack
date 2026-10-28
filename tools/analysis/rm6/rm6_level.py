"""Rockman 6 (J) static level decoder / renderer (rm6-stages-b; docs/research/rm6/stages_b.md section 1).

    import sys; sys.path.insert(0, "tools/analysis"); sys.path.insert(0, "tools/analysis/rm6")
    from rm6_level import *
    lay = layout(2); chr_ = bytearray(0x2000); apply_chr(chr_, T["CHR"][2]); pal = palette(T["PAL"][2])
    render_screen(2, 0, chr_, pal, lay).save("plant00.png")   # screen 0 of Plant Man, start CHR/palette
    script(0x1C)                                              # screen script: init, mode, per-frame, exits

Run from the repo root (reads roms/rm6j.nes). The screen-graph/map builder that uses this is
build/research/rm6/rm6-stages-b/geom.py (needs the object lists dumped by objdump.py there).
"""
import sys; sys.path.insert(0, 'tools/analysis')
from PIL import Image
ROM = open('roms/rm6j.nes', 'rb').read()[16:]
def b(bank, off): return ROM[bank*0x2000 + off]
def fixed(a): return ROM[0x3E*0x2000 + a - 0xC000] if a < 0xE000 else ROM[0x3F*0x2000 + a - 0xE000]
T = {n: [fixed(a + s) for s in range(16)] for n, a in dict(L6F=0xDF25, P52=0xDF35, P53=0xDF45, T6E=0xDF55,
     P63=0xDF65, P67=0xDF75, CHR=0xDF85, PAL=0xDF95, MUS=0xDFA5).items()}
NAMES = ['blizzard','wind','plant','flame','yamato','tomahawk','knight','centaur','mrx1','mrx2','mrx3','mrx4','wily1','wily2','wily3','wily4']

def layout(st):
    L, p53 = T['L6F'][st], T['P53'][st]
    return [[b(L, (p53 - 0xA0 + r) * 256 + c) for c in range(256)] for r in range(8)]

def block(st, bid, q):
    return b(T['T6E'][st], (T['P67'][st] << 8) + bid * 4 + q - 0x8000)

def tile16(st, tid, alt=False):
    t, p = T['T6E'][st], (0x9B if alt else T['P63'][st])
    return [b(t, ((p + k) << 8) + tid - 0x8000) for k in range(5)]   # TL TR BL BR attr

def chrset(cid):
    d = ROM[0x37*0x2000 + cid*4: 0x37*0x2000 + cid*4 + 4]
    cnt = d[0] or 256; dest = d[1]*16 + (0x1000 if d[3] & 0x80 else 0)
    src = ((d[3] & 1)*256 + d[2])*16; bank = (d[3] & 0x7E) >> 1
    return dest, ROM[bank*0x2000 + src: bank*0x2000 + src + cnt*16], bank, src

def apply_chr(chr_, cid):
    dest, data, _, _ = chrset(cid)
    chr_[dest:dest+len(data)] = data

def palette(pid, buf=None, bank=0x37):
    buf = buf if buf is not None else [0x0F]*32
    lo = ROM[bank*0x2000 + 0x1000 + pid]; hi = ROM[bank*0x2000 + 0x1100 + pid]
    p = (hi << 8 | lo) - 0x8000; base = bank*0x2000
    x = ROM[base + p]; y = 1
    while True:
        v = ROM[base + p + y]
        if v & 0x40:
            if x < 32: buf[x] = 0x0F
            x += 1
        if x < 32: buf[x] = v & 0x3F
        x += 1; y += 1
        if v & 0x80: break
    return buf

def render_screen(st, scr, chr_, pal, lay=None, alt_ids=()):
    from emu import nes_rgb
    lay = lay or layout(st)
    im = Image.new('RGB', (256, 256))
    px = im.load()
    for r in range(8):
        for c in range(8):
            bid = lay[r][scr*8 + c]
            for q in range(4):
                tid = block(st, bid, q)
                t = tile16(st, tid, tid in alt_ids)
                for k in range(4):
                    ch = t[k]; pl = t[4] & 3
                    ox = c*32 + (q & 1)*16 + (k & 1)*8; oy = r*32 + (q >> 1)*16 + (k >> 1)*8
                    for yy in range(8):
                        lo = chr_[ch*16 + yy]; hi = chr_[ch*16 + 8 + yy]
                        for xx in range(8):
                            v = ((lo >> (7-xx)) & 1) | (((hi >> (7-xx)) & 1) << 1)
                            px[ox+xx, oy+yy] = nes_rgb(pal[pl*4 + v] if v else pal[0])
    return im.crop((0, 0, 256, 240))

# ---- object lists (bank $3A pointer tables $80BF/$80CF -> 4 parallel arrays: screen, X, Y/param, type) ----
def r3a(a): return ROM[(0x3A if a < 0xA000 else 0x3B)*0x2000 + (a & 0x1FFF)]
def objects(st):
    """[(screen, x, y_or_param, type)] in list order; type $80 = screen script (param = script id)."""
    import struct
    # pointers as seen in RAM $74/$78/$7C/$7E: derive from the bank-3A per-stage tables
    lo = r3a(0x80BF + st); hi = r3a(0x80CF + st); base = lo | hi << 8
    return base

def b39(a): return ROM[(0x39 if a < 0xA000 else 0x3A)*0x2000 + (a & 0x1FFF)]
DIRS = {1: 'down', 2: 'up', 3: 'down*', 4: 'up*', 5: 'right', 6: 'left'}
def script(idx):
    p = b39(0x82EB + idx) | b39(0x836B + idx) << 8
    s = [b39(p + k) for k in range(32)]
    y = 0; init = None
    if s[0] & 0x80: init = s[0] << 8 | s[1]; mode = s[2]; y = 3
    else: mode = s[0]; y = 1
    pf = (s[y] << 8 | s[y+1]) if s[y] else None
    y += 2; exits = []
    if init: y = 5
    while s[y] and not s[y] & 0x80 and s[y] <= 6:
        d = s[y]; chr_ = s[y+1]; pal = s[y+2]; y += 3; tgt = None
        if s[y] & 0x80: tgt = s[y] & 0x7F; y += 1
        exits.append((d, chr_, pal, tgt))
    return dict(addr=p, init=init, mode=mode, pf=pf, exits=exits)

def init_effects(init, n=64):
    """scan an init routine for 'LDA #x / JSR $C9EF' (palette) and 'LDA #x / STA $064F' or 'JSR $CAA4/$CAAA' (CHR)."""
    if not init: return [], [], []
    c = [b39(init + k) for k in range(n)]
    pals, chrs = [], []
    post = []
    for i in range(n - 7):
        if c[i] == 0xA9 and c[i+2:i+8] == [0x8D, 0x9E, 0x06, 0x20, 0xEF, 0xC9]: post.append(c[i+1])
    for i in range(n - 4):
        if c[i] == 0xA9 and c[i+2] == 0x20 and c[i+3] == 0xEF and c[i+4] == 0xC9: pals.append(c[i+1])
        if c[i] == 0xA9 and ((c[i+2] == 0x8D and c[i+3] == 0x4F and c[i+4] == 0x06) or (c[i+2] == 0x20 and c[i+4] == 0xCA and c[i+3] in (0xA4, 0xAA))): chrs.append(c[i+1])
        if c[i] == 0x4C and c[i+1] == 0x5A and c[i+2] == 0xE4: break
        if c[i] == 0x60: break
    return chrs, pals, post

def coll_overlay(st, scr, base_im, lay=None):
    """overlay raw collision nibble (attr>>4) on a rendered screen (16x16 grid, hex digit, tinted)"""
    from PIL import ImageDraw
    lay = lay or layout(st); im = base_im.copy().convert('RGB'); d = ImageDraw.Draw(im, 'RGBA')
    COL = {1: (255, 255, 255, 60), 3: (255, 0, 255, 120), 4: (0, 255, 0, 110), 5: (0, 128, 255, 110), 6: (255, 128, 0, 110),
           7: (255, 255, 0, 110), 8: (0, 255, 255, 110), 9: (128, 0, 255, 110), 10: (128, 255, 128, 110), 11: (255, 128, 128, 90),
           12: (128, 128, 255, 110), 13: (255, 64, 64, 130), 14: (64, 255, 64, 110), 15: (255, 0, 0, 140), 2: (0, 0, 255, 110)}
    for r in range(8):
        for c in range(8):
            bid = lay[r][scr*8 + c]
            for q in range(4):
                ty = tile16(st, block(st, bid, q))[4] >> 4
                if ty == 0: continue
                x = c*32 + (q & 1)*16; y = r*32 + (q >> 1)*16
                if y >= 240: continue
                d.rectangle([x, y, x+15, y+15], fill=COL.get(ty, (255, 255, 255, 100)))
                if ty != 1: d.text((x+4, y+3), '%X' % ty, fill=(0, 0, 0, 255))
    return im
