"""Rockman 6 (J) static stage decoder, route walker and map renderer (written by rm6-stages-a).
Docs: docs/research/rm6/stages_a.md section 0 (format) and the per-stage maps.

    python3 -I tools/analysis/rm6/rm6_stagemap.py <stage 0-15> out.png      # stitched map of the stage
    python3 -I tools/analysis/rm6/rm6_stagemap.py <stage>                   # print the screen graph

Library:
    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
    import rm6_stagemap as sm
    placed = sm.walk(7)            # {screen: (x, y, extra CHR set, 32-colour palette, how entered)}, sm.PID = last palette id
    sm.render(7, placed, 'centaur.png')
    R = sm.Renderer(7, sm.chr_for(7, 0), list(placed[0][3])); R.screen(0x0A); R.collision(0x0A)
    sm.objlist(7)                  # [(screen, x, y, type)], type $80 = screen script (y = script index)
    sm.scripts(7)                  # decoded screen scripts with exits

Format summary: layout = bank $DF25[s] at $A000, page $DF45[s]+row (8 rows of 32x32 blocks, col = screen*8+x/32);
blocks/metatiles = bank $DF55[s] at $8000 (blocks at page $DF75[s], metatile pages $DF65[s]+0..4: TL TR BL BR attr);
CHR sets bank $37 $8000+id*4; palettes bank $37 $9000/$9100+id (partial, cumulative); objects bank $3A.
"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, '..'))
from PIL import Image, ImageDraw
from emu import nes_rgb
_REPO = os.path.abspath(os.path.join(_HERE, '..', '..', '..'))
ROM = open(os.path.join(_REPO, 'roms', 'rm6j.nes'), 'rb').read()[16:]


def rb(bank, a): return ROM[bank * 0x2000 + (a & 0x1FFF)]
def t3e(a, s): return rb(0x3E, a + s)

def stage_params(s):
    return dict(b6e=t3e(0xDF55, s), b6f=t3e(0xDF25, s), lo52=t3e(0xDF35, s), hi53=t3e(0xDF45, s),
                p63=t3e(0xDF65, s), p67=t3e(0xDF75, s), chr=t3e(0xDF85, s), pal=t3e(0xDF95, s),
                music=t3e(0xDFA5, s))

def layout(s):
    P = stage_params(s)
    return [[rb(P['b6f'], ((P['hi53'] + r) << 8) + P['lo52'] + c) for c in range(256)] for r in range(8)]

def block(s, bid):
    P = stage_params(s); base = (P['p67'] << 8) + bid * 4
    return [rb(P['b6e'], base + k) for k in range(4)]

def metatile(s, mt, alt=False):
    P = stage_params(s)
    if alt:
        return [rb(P['b6e'], ((0x9B + k) << 8) + mt) for k in range(4)], rb(P['b6e'], 0x9F00 + mt)
    return [rb(P['b6e'], ((P['p63'] + k) << 8) + mt) for k in range(4)], rb(P['b6e'], ((P['p63'] + 4) << 8) + mt)

def chr_set(sid):
    e = [rb(0x37, 0x8000 + sid * 4 + k) for k in range(4)]
    cnt = e[0] or 256; ppu = e[1] * 16 + (0x1000 if e[3] & 0x80 else 0)
    bank = (e[3] & 0x7E) >> 1; src = (e[3] & 1) * 0x1000 + e[2] * 16
    data = bytes(ROM[bank * 0x2000 + src + i] if src + i < 0x2000 else ROM[(bank + 1) * 0x2000 + src + i - 0x2000]
                 for i in range(cnt * 16))
    return ppu, data, (bank, src, cnt)

def apply_chr(chrram, sid):
    ppu, data, _ = chr_set(sid)
    chrram[ppu:ppu + len(data)] = data
    return chrram

def palette(pid, revisit=False, buf=None):
    bank = 0x28 if revisit else 0x37
    p = rb(bank, 0x9000 + pid) | rb(bank, 0x9100 + pid) << 8
    buf = list(buf) if buf else [0x0F] * 32
    x = rb(bank, p); y = 1
    while True:
        v = rb(bank, p + y)
        if v & 0x40: buf[x & 31] = 0x0F; x += 1
        buf[x & 31] = v & 0x3F; x += 1; y += 1
        if v & 0x80: break
        if y > 64: break
    return buf

def tile_img(chrram, t, pal4, base=0):
    o = base + t * 16; im = Image.new('RGB', (8, 8)); px = im.load()
    for y in range(8):
        lo, hi = chrram[o + y], chrram[o + y + 8]
        for x in range(8):
            c = (lo >> (7 - x) & 1) | (hi >> (7 - x) & 1) << 1
            px[x, y] = nes_rgb(pal4[c])
    return im

class Renderer:
    def __init__(self, s, chrram, pal32, flags=None, bgbase=0):
        self.s = s; self.chr = chrram; self.pal = pal32; self.cache = {}; self.flags = flags or bytes(32)
        self.lay = layout(s); self.bgbase = bgbase
    def mt_img(self, mt):
        alt = bool(self.flags[mt >> 3] >> (mt & 7) & 1)
        k = (mt, alt)
        if k in self.cache: return self.cache[k]
        tiles, attr = metatile(self.s, mt, alt)
        p = attr & 3; pal4 = [self.pal[0]] + self.pal[p * 4 + 1:p * 4 + 4]
        im = Image.new('RGB', (16, 16))
        for q, t in enumerate(tiles):
            im.paste(tile_img(self.chr, t, pal4, self.bgbase), ((q & 1) * 8, (q >> 1) * 8))
        self.cache[k] = im
        return im
    def screen(self, scr, rows=8):
        im = Image.new('RGB', (256, rows * 32))
        for r in range(rows):
            for c in range(8):
                bid = self.lay[r][scr * 8 + c]
                for q, mt in enumerate(block(self.s, bid)):
                    im.paste(self.mt_img(mt), (c * 32 + (q & 1) * 16, r * 32 + (q >> 1) * 16))
        return im.crop((0, 0, 256, 240))
    def collision(self, scr):
        """16x15 grid of collision nibbles (attr >> 4) for a screen."""
        g = [[0] * 16 for _ in range(16)]
        for r in range(8):
            for c in range(8):
                bid = self.lay[r][scr * 8 + c]
                for q, mt in enumerate(block(self.s, bid)):
                    alt = bool(self.flags[mt >> 3] >> (mt & 7) & 1)
                    g[r * 2 + (q >> 1)][c * 2 + (q & 1)] = metatile(self.s, mt, alt)[1] >> 4
        return g[:15]

# ---- object lists and screen scripts ----

def r3a(a): return ROM[(0x3A if a<0xA000 else 0x3B)*0x2000+(a&0x1FFF)]
def objlist(st):
    P=r3a(0x80BF+st)|r3a(0x80CF+st)<<8; n=r3a(0x80DF+st)
    return [(r3a(P+1+i), r3a(P+2+n+i), r3a(P+3+2*n+i), r3a(P+4+3*n+i)) for i in range(n)]
def ai(t):
    return r3a(0x84C9+t), r3a(0x83C9+t)<<8|r3a(0x82C9+t), r3a(0x85C9+(t>>4))

def scripts(st):
    out=[]
    for (scr,x,y,t) in objlist(st):
        if t==0x80:
            p,init,mode,pf,ex=script(y)
            out.append(dict(scr=scr,x=x,idx=y,init=init,mode=mode,pf=routine_desc(pf),exits=ex))
    return out

def b39(a): return ROM[(0x39 if a<0xA000 else 0x3A)*0x2000 + (a&0x1FFF)]
DIRS={1:'down',2:'up',3:'down*',4:'up*',5:'right',6:'left'}
def script(idx):
    p=b39(0x82EB+idx) | b39(0x836B+idx)<<8
    s=[b39(p+k) for k in range(24)]
    y=0; init=None
    if s[0]&0x80: init=s[0]<<8|s[1]; mode=s[2]; y=3
    else: mode=s[0]; y=1
    pf = (s[y]<<8|s[y+1]) if s[y] else None
    y+=2; exits=[]
    while s[y] and not s[y]&0x80:
        d=s[y]; chr_=s[y+1]; pal=s[y+2]; y+=3; tgt=None
        if s[y]&0x80: tgt=s[y]&0x7F; y+=1
        exits.append((DIRS.get(d,d),chr_,pal,tgt))
    return p,init,mode,pf,exits
def routine_desc(pf):
    if pf is None: return '-'
    o=[b39(pf+k) for k in range(6)]
    if o[0]==0xA9 and o[2]==0x4C and o[3]==0x16 and o[4]==0x84: return 'CKPT@%02X'%o[1]
    if o[0]==0xA5 and o[1]==0x57 and o[2]==0x4C and o[3]==0x16: return 'CKPT@here'
    if o[0]==0xA9 and o[2]==0x20 and o[3]==0x16 and o[4]==0x84: return 'CKPT@%02X+'%o[1]
    return '%04X'%pf

# ---- route walker and map renderer ----


# script idx -> (chr set, palette, mode) applied by its init routine (p0C: $39:$849B, Flame screen 0C)
SPECIAL = {0x0C: (0x87, 0x1F, 3)}   # only Flame's script 0C is covered; scripts whose init never returns (e.g. Plant's 1E/1F) may need entries
DX = {'down': (0, 1), 'up': (0, -1), 'right': (1, 0), 'left': (-1, 0)}

def _b39(a): return ROM[(0x39 if a < 0xA000 else 0x3A) * 0x2000 + (a & 0x1FFF)]
def routine_pals(d):
    """Palette ids a script's init / per-frame routine loads (LDA #id + JSR $C9EF, or STA $069E)."""
    out = []
    for a in [d['init']] + ([int(d['pf'], 16)] if d['pf'] not in ('-',) and not d['pf'].startswith('CKPT') else []):
        if not a or a == 0xFFFF or a < 0x8000: continue
        b = [_b39(a + k) for k in range(32)]
        for k in range(29):
            if b[k] == 0x60 or (b[k] == 0x4C and b[k+1:k+3] != [0xEF, 0xC9]): break
            if b[k] == 0xA9 and ((b[k+2:k+5] == [0x20, 0xEF, 0xC9]) or (b[k+2:k+5] == [0x8D, 0x9E, 0x06])):
                out.append(b[k + 1])
    return out

def walk(st, start=0, chr_extra=0, pal=None, limit=40, extra_starts=()):
    P = stage_params(st)
    S = {d['scr']: d for d in scripts(st)}
    pal = tuple(palette(pal if pal is not None else P['pal']))
    placed = {}    # screen -> (x, y, chr_extra, pal, how)
    global PID; PID = {}
    todo = [(start, 0, 0, chr_extra, pal, 'start', 1, 0)] + list(extra_starts)
    mode = 1
    while todo:
        s, x, y, ce, pl, how, mode, pid = todo.pop(0)
        if s in placed or s > 31 or len(placed) > limit: continue
        placed[s] = (x, y, ce, pl, how); PID[s] = pid
        d = S.get(s)
        if d is not None and d['mode'] != 255: mode = d['mode']
        if d is not None:
            for pid in routine_pals(d): pl = tuple(palette(pid, buf=pl)); PID[s] = pid
            placed[s] = (x, y, ce, pl, how)
        if d is not None and d['mode'] == 255: continue      # boss room
        fwd = [(a, c, p, t) for a, c, p, t in (d['exits'] if d else []) if a in DX]
        if d is not None and d['idx'] in SPECIAL:          # init routine that never returns to the exit list
            c, p, m = SPECIAL[d['idx']]; ce = c or ce; mode = m; fwd = []
            if p: pl = tuple(palette(p, buf=pl)); PID[s] = p
        for a, c, p, t in fwd:
            n = (t if t is not None else s) + 1; dx, dy = DX[a]
            todo.append((n, x + dx, y + dy, c or ce, tuple(palette(p, buf=pl)) if p else pl, a, mode, p or PID[s]))
        shutter = d is not None and d['pf'] in ('8480', '848E')
        if (not fwd and (mode & 1)) or shutter or (d is not None and d['mode'] & 1 and not fwd):
            todo.append((s + 1, x + 1, y, ce, pl, 'shutter' if shutter else 'scroll', mode, PID[s]))
    return placed

def chr_for(st, ce):
    P = stage_params(st); c = bytearray(0x2000)
    apply_chr(c, P['chr'])
    if ce: apply_chr(c, ce)
    return c

def render(st, placed, path, scale=1, label=True, objects=True, flags=None, revisit=False, chrs=None, crop=None):
    xs = [v[0] for v in placed.values()]; ys = [v[1] for v in placed.values()]
    x0, y0 = min(xs), min(ys); W = (max(xs) - x0 + 1) * 256; H = (max(ys) - y0 + 1) * 240
    im = Image.new('RGB', (W, H), (40, 40, 40)); dr = ImageDraw.Draw(im)
    R = {}
    OL = objlist(st)
    for s, (x, y, ce, pl, how) in placed.items():
        key = (ce, pl)
        if key not in R:
            c = chrs.get(s) if chrs and s in chrs else chr_for(st, ce)
            R[key] = Renderer(st, c, list(pl), flags=flags)
        px, py = (x - x0) * 256, (y - y0) * 240
        im.paste(R[key].screen(s), (px, py))
        if label:
            dr.rectangle([px, py, px + 44, py + 10], fill=(0, 0, 0))
            dr.text((px + 2, py), 'scr %02X' % s, fill=(255, 255, 0))
        if objects:
            for (os_, ox, oy, t) in OL:
                if os_ != s: continue
                if t == 0x80:
                    dr.rectangle([px + ox - 1, py + 12, px + ox + 22, py + 22], fill=(0, 0, 160))
                    dr.text((px + ox, py + 12), 'S%02X' % oy, fill=(255, 255, 255))
                else:
                    oy2 = min(oy, 232)
                    dr.rectangle([px + ox - 8, py + oy2 - 5, px + ox + 8, py + oy2 + 5], outline=(255, 0, 255), fill=(0, 0, 0))
                    dr.text((px + ox - 6, py + oy2 - 6), '%02X' % t, fill=(255, 128, 255))
        dr.rectangle([px, py, px + 255, py + 239], outline=(90, 90, 90))
    if crop: im = im.crop(crop)
    if scale != 1: im = im.resize((im.width * scale, im.height * scale))
    im.save(path)
    return im, (x0, y0)


if __name__ == '__main__':
    st = int(sys.argv[1]); pl = walk(st)
    for s in sorted(pl): print('%02X' % s, pl[s][:3], pl[s][4], 'pal %02X' % PID[s])
    if len(sys.argv) > 2: render(st, pl, sys.argv[2]); print('wrote', sys.argv[2])
