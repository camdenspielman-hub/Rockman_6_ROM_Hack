"""Rockman 6 (J) level data: decoder, encoder (byte-exact round trip) and full-map renderer (rm6-levels).

Docs: docs/research/rm6/levels.md (byte-level format reference for all 16 stages).

    python3 -I tools/analysis/rm6/levels.py info [stage]          # header, scripts, exits, objects, graph
    python3 -I tools/analysis/rm6/levels.py roundtrip              # re-encode everything, compare with the ROM
    python3 -I tools/analysis/rm6/levels.py maps [stage ...]       # docs/research/rm6/img/maps/<nn>_<name>.png
    python3 -I tools/analysis/rm6/levels.py strips [stage ...]     # raw 32-screen strips (unused screens too)
    python3 -I tools/analysis/rm6/levels.py json <outdir>          # structured export (one JSON per stage)
    python3 -I tools/analysis/rm6/levels.py appendix               # docs/research/rm6/levels_stages.md

Editing: js = [export(s) for s in range(16)]; edit the dicts; build_rom(js, 'out.nes') re-encodes every stage
(object lists are re-packed and their pointers rewritten).  roundtrip() / json_roundtrip() prove the encoders
reproduce the original bytes.

Library:
    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
    import levels as L
    st = L.Stage(7)                      # Centaur Man: st.hdr, st.screens, st.metatiles, st.blocks, st.objects
    g = L.walk(7)                        # screen graph: {screen: Node(x, y, comp, chr ids, pal32, how, mode)}
    L.render_map(7, 'centaur.png')       # stitched full map from ROM data alone
    L.Renderer(st, L.chr_ram([0xAA]), L.palette(0xA6)).screen(0x0A)   # one screen as a PIL image

Run from anywhere (reads <repo>/roms/rm6j.nes). Format summary (details and evidence in levels.md):
  stage table $3E:$DF25..$DFB4 (9 x 16 bytes: layout bank, layout lo/page, tileset bank, metatile page,
  block page, BG CHR set, palette, music); layout = 8 rows x 256 columns of 32x32 block ids (column =
  screen*8 + x/32); block = 4 metatile ids (TL TR BL BR); metatile = 4 CHR tiles + attribute
  (bits 0-1 palette, 4-7 collision); alternate metatile set at pages $9B-$9F selected by the bitfield $0340;
  CHR sets bank $37 $8000+4*id; palettes bank $37 (bank $28 on a revisit) $9000/$9100 pointers;
  object lists bank $3A $80BF/$80CF/$80DF; screen scripts bank $39 $82EB/$836B (pointers may point into
  the fixed banks); object type -> AI bank/address $3A:$84C9/$83C9/$82C9, 4-byte header before the AI code
  (CHR set, ?, HP, flags).
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(_HERE, '..'))
_RAW = open(os.path.join(_REPO, 'roms', 'rm6j.nes'), 'rb').read()
HEADER, ROM = _RAW[:16], _RAW[16:]

NAMES = ['blizzard', 'wind', 'plant', 'flame', 'yamato', 'tomahawk', 'knight', 'centaur',
         'mrx1', 'mrx2', 'mrx3', 'mrx4', 'wily1', 'wily2', 'wily3', 'wily4']
TITLES = ['Blizzard Man', 'Wind Man', 'Plant Man', 'Flame Man', 'Yamato Man', 'Tomahawk Man', 'Knight Man',
          'Centaur Man', 'Mr. X Fortress 1', 'Mr. X Fortress 2', 'Mr. X Fortress 3', 'Mr. X Fortress 4',
          'Wily Fortress 1', 'Wily Fortress 2', 'Wily Fortress 3', 'Wily Fortress 4']

# ------------------------------------------------------------------------------------------------ ROM access
def boff(bank, a):
    """file offset (no header) of CPU address a when 8 KB bank `bank` is mapped at a's 8 KB window."""
    return bank * 0x2000 + (a & 0x1FFF)

def rb(bank, a): return ROM[boff(bank, a)]

def cpu(a, lo, hi=None):
    """read CPU address a with bank `lo` at $8000 and `hi` (default lo+1) at $A000; $C000+ = fixed $3E/$3F."""
    if a >= 0xE000: return ROM[boff(0x3F, a)]
    if a >= 0xC000: return ROM[boff(0x3E, a)]
    if a >= 0xA000: return ROM[boff(lo + 1 if hi is None else hi, a)]
    return ROM[boff(lo, a)]

def cpu_off(a, lo, hi=None):
    if a >= 0xE000: return boff(0x3F, a)
    if a >= 0xC000: return boff(0x3E, a)
    if a >= 0xA000: return boff(lo + 1 if hi is None else hi, a)
    return boff(lo, a)

def fixed(a): return cpu(a, 0x3E)

# ------------------------------------------------------------------------------------------------ stage table
STAGE_TABLE = 0xDF25            # 9 tables x 16 stages, fixed bank $3E
FIELDS = ['layout_bank', 'layout_lo', 'layout_page', 'tile_bank', 'mt_page', 'blk_page', 'chr', 'pal', 'music']
RAMOF = dict(layout_bank='$6F', layout_lo='$52', layout_page='$53', tile_bank='$6E', mt_page='$63',
             blk_page='$67', chr='$064E', pal='$069E', music='$DC')
COLL_GROUP = 0xDB03             # per-stage collision group (16 bytes)
COLL_REMAP = 0xDB13             # group*16 + type -> type actually tested
BITMASK = 0xDFB5                # 01 02 04 .. 80 (bit for id & 7)

def header(s):
    return {f: fixed(STAGE_TABLE + 16 * i + s) for i, f in enumerate(FIELDS)}

def coll_map(s):
    g = fixed(COLL_GROUP + s)
    return [fixed(COLL_REMAP + g * 16 + t) for t in range(16)]

# ------------------------------------------------------------------------------------------------ layout / tiles
class Stage:
    """All static data of one stage, decoded from the ROM.  Re-encode with the encode_* functions."""
    def __init__(self, s):
        self.id = s; self.name = NAMES[s]; self.hdr = h = header(s)
        lb, lo, pg = h['layout_bank'], h['layout_lo'], h['layout_page']
        self.layout_off = boff(lb, (pg << 8) + lo)
        raw = ROM[self.layout_off:self.layout_off + 0x800]
        self.screens = decode_layout(raw)               # [32][8 rows][8 cols] block ids
        tb = h['tile_bank']
        self.tiles_off = boff(tb, h['mt_page'] << 8)
        self.metatiles, self.blocks = decode_tileset(ROM[self.tiles_off:self.tiles_off + 9 * 256])
        self.alt_off = boff(tb, 0x9B00)
        self.alt_metatiles = decode_metatiles(ROM[self.alt_off:self.alt_off + 5 * 256])
        self.objects, self.obj_sentinels = decode_objects(s)
        self.coll = coll_map(s)
    def block_at(self, scr, row, col): return self.screens[scr][row][col]
    def used_screens(self):
        """screens that hold any object (the object list is sorted by screen), plus screens reached by walk()."""
        return sorted({o[0] for o in self.objects})

def decode_layout(raw):
    return [[[raw[r * 256 + sc * 8 + c] for c in range(8)] for r in range(8)] for sc in range(32)]

def encode_layout(screens):
    out = bytearray(0x800)
    for sc in range(32):
        for r in range(8):
            for c in range(8): out[r * 256 + sc * 8 + c] = screens[sc][r][c]
    return bytes(out)

def decode_metatiles(raw):
    """5 pages -> 256 x dict(tiles=[TL,TR,BL,BR], pal=attr&3, coll=attr>>4, attr=raw attribute)"""
    out = []
    for m in range(256):
        a = raw[4 * 256 + m]
        out.append(dict(tiles=[raw[k * 256 + m] for k in range(4)], pal=a & 3, coll=a >> 4, attr=a))
    return out

def encode_metatiles(mts):
    out = bytearray(5 * 256)
    for m, d in enumerate(mts):
        for k in range(4): out[k * 256 + m] = d['tiles'][k]
        out[4 * 256 + m] = (d['pal'] & 3) | (d['coll'] & 15) << 4     # bits 2-3 are 0 in every stage
    return bytes(out)

def decode_tileset(raw):
    mts = decode_metatiles(raw[:5 * 256])
    blocks = [list(raw[5 * 256 + b * 4: 5 * 256 + b * 4 + 4]) for b in range(256)]
    return mts, blocks

def encode_tileset(mts, blocks):
    return encode_metatiles(mts) + bytes(v for b in blocks for v in b)

# ------------------------------------------------------------------------------------------------ CHR sets
CHR_TABLE = (0x37, 0x8000)      # 256 x 4 bytes
def chr_set(i):
    """CHR set i -> dict(count tiles, ppu dest, bank, src offset in bank pair, data bytes).  [code] $3E:$C95C"""
    e = [rb(0x37, 0x8000 + i * 4 + k) for k in range(4)]
    cnt = e[0] or 256
    ppu = e[1] * 16 + (0x1000 if e[3] & 0x80 else 0)
    bank = (e[3] & 0x7E) >> 1
    src = (e[3] & 1) * 0x1000 + e[2] * 16          # offset from the start of `bank` (spills into bank+1)
    data = ROM[bank * 0x2000 + src: bank * 0x2000 + src + cnt * 16]
    return dict(id=i, raw=e, count=cnt, ppu=ppu, bank=bank, src=src, file=bank * 0x2000 + src + 16, data=data)

def chr_ram(sets, ram=None):
    """apply CHR sets in order to an 8 KB CHR-RAM image (what $CAA4 does)."""
    ram = bytearray(ram) if ram is not None else bytearray(0x2000)
    for i in sets:
        if not i: continue
        c = chr_set(i)
        n = min(len(c['data']), 0x2000 - c['ppu'])
        ram[c['ppu']:c['ppu'] + n] = c['data'][:n]
    return ram

# ------------------------------------------------------------------------------------------------ palettes
PAL_BANK, PAL_BANK_REVISIT = 0x37, 0x28
def palette_raw(pid, bank=PAL_BANK):
    """palette program: (start, [values]) exactly as stored (b6 = write $0F first, b7 = last).  [code] $3E:$C9EF"""
    p = rb(bank, 0x9000 + pid) | rb(bank, 0x9100 + pid) << 8
    start = rb(bank, p); vals = []; y = 1
    while True:
        v = rb(bank, p + y); vals.append(v); y += 1
        if v & 0x80 or y > 80: break
    return p, start, vals

def palette(pid, buf=None, bank=PAL_BANK):
    """apply palette program pid to a 32-entry buffer (cumulative partial update, like $0360)."""
    buf = list(buf) if buf is not None else [0x0F] * 32
    _, x, vals = palette_raw(pid, bank)
    for v in vals:
        if v & 0x40:
            if x < 32: buf[x] = 0x0F
            x += 1
        if x < 32: buf[x] = v & 0x3F
        x += 1
    return buf

def encode_palette(start, vals): return bytes([start] + list(vals))

# ------------------------------------------------------------------------------------------------ objects
OBJ_PTR_LO, OBJ_PTR_HI, OBJ_COUNT = 0x80BF, 0x80CF, 0x80DF   # bank $3A
def r3a(a): return cpu(a, 0x3A)

def decode_objects(s):
    """[(screen, x, y, type)] in list order; sentinels = the 4 bytes before each array ($FF except stage 0)."""
    P = r3a(OBJ_PTR_LO + s) | r3a(OBJ_PTR_HI + s) << 8; n = r3a(OBJ_COUNT + s)
    arr = [[r3a(P + 1 + k * (n + 1) + i) for i in range(n)] for k in range(4)]
    sent = [r3a(P + k * (n + 1)) for k in range(4)]
    return list(zip(*arr)), sent

def encode_objects(objs, sentinels):
    n = len(objs); out = bytearray()
    for k in range(4):
        out.append(sentinels[k]); out += bytes(o[k] for o in objs)
    return bytes(out) + b''          # the next stage's first sentinel follows (or $FF fill after stage 15)

AI_LO, AI_HI, AI_BANK, AI_SPRBANK = 0x82C9, 0x83C9, 0x84C9, 0x85C9   # bank $3A, indexed by type
def ai(t):
    """object type -> (AI bank, AI address, 4-byte header at address-4: CHR set, ?, HP, flags)."""
    bank = r3a(AI_BANK + t); a = r3a(AI_HI + t) << 8 | r3a(AI_LO + t)
    hdr = [cpu(a - 4 + k, bank) for k in range(4)]
    return dict(type=t, bank=bank, addr=a, chr=hdr[0], hdr=hdr, hp=hdr[2], sprbank=r3a(AI_SPRBANK + (t >> 4)))

# ------------------------------------------------------------------------------------------------ screen scripts
SCR_LO, SCR_HI = 0x82EB, 0x836B     # bank $39, 128 entries; pointer may be in $C000-$FFFF (fixed banks)
EXIT_HANDLERS = {0xD587: 1, 0xD612: 2, 0xD540: 3, 0xD5D1: 4, 0xD653: 5, 0xD6B3: 6}  # $39:$9A88/$9A8F
EXIT_DIR = {1: 'down', 2: 'up', 3: 'down', 4: 'up', 5: 'right', 6: 'left'}
EXIT_STEP = {1: 1, 2: 1, 3: -1, 4: -1, 5: 1, 6: -1}
CKPT_ROUTINE = 0x8416               # LDA #s / JMP $8416 : checkpoint s when $57 == s ; $841A = unconditional
SHUTTERS = {0x8480: 1, 0x848E: 2}
def r39(a): return cpu(a, 0x39)
def script_ptr(i): return r39(SCR_LO + i) | r39(SCR_HI + i) << 8

def decode_script(i):
    """script i -> dict(ptr, init, mode, pf, exits=[(type, chr, pal, target|None)], size, init_info).
    The exit list is only part of the script when the init routine returns ($39:$824D)."""
    p = script_ptr(i); b = lambda k: r39(p + k)
    d = dict(idx=i, ptr=p, init=None, mode=None, pf=None, exits=[], term=None)
    y = 0
    if b(0) & 0x80:
        d['init'] = b(0) << 8 | b(1); d['mode'] = b(2); y = 3
        info = trace(d['init'])
        d['init_info'] = info; d['returns'] = info['returns']
        if not info['returns']:
            d['size'] = 3; return d
    else:
        d['mode'] = b(0); y = 1
    d['pf'] = (b(y) << 8 | b(y + 1)) if b(y) else None
    d['pf_lo'] = b(y + 1)                   # stored even when hi = 0 (round trip)
    y += 2
    while True:
        t = b(y)
        if t == 0 or t & 0x80: d['term'] = t; y += 1; break
        c, pl = b(y + 1), b(y + 2); y += 3; tg = None
        if b(y) & 0x80: tg = b(y) & 0x7F; y += 1
        d['exits'].append((t, c, pl, tg))
    d['size'] = y
    return d

def encode_script(d):
    out = bytearray()
    if d['init'] is not None:
        out += bytes([d['init'] >> 8, d['init'] & 0xFF, d['mode']])
        if not d['returns']: return bytes(out)
    else:
        out.append(d['mode'])
    out += bytes([d['pf'] >> 8, d['pf'] & 0xFF]) if d['pf'] else bytes([0, d['pf_lo']])
    for t, c, pl, tg in d['exits']:
        out += bytes([t, c, pl]) + (bytes([0x80 | tg]) if tg is not None else b'')
    out.append(d['term'])
    return bytes(out)

# ---- a tiny static tracer for init / per-frame routines (bank $39 + $3A, fixed $3E/$3F) ----
_DIS = {}
def _dis(bank=0x39):
    if bank not in _DIS:
        sys.path.insert(0, os.path.join(_REPO, '.pylib'))
        from py65.devices.mpu6502 import MPU
        from py65.disassembler import Disassembler
        m = MPU(); mem = m.memory
        mem[0x8000:0xC000] = list(ROM[bank * 0x2000:(bank + 2) * 0x2000])
        mem[0xC000:0x10000] = list(ROM[0x3E * 0x2000:0x40 * 0x2000])
        _DIS[bank] = (Disassembler(m), mem)
    return _DIS[bank]
PAL_HELPERS = {0xC9EF: 0x39, 0x8110: 0x39, 0x8114: 0x39}   # $39:$8110/$8114 = palette A + fade-in

NEVER_RETURN = {0xE45A}             # kill current object/thread
INTERP_RESUME = {0x827C, 0x827E}    # JMP back into the script interpreter's exit loop = 'returns'
WARP_ROUTINES = {0x89F5}            # $39:$89F5: STA $57 / STA $046F / JMP $D716 (teleport to screen A)
# Wily 3 teleporter hub ($39:$8E3B): teleporter k -> boss id $8ED2[k], screen 9 + id, palette $9A + id
HUB = {14: dict(screen=0x08, ids=0x8ED2, first=0x09, pal=0x9A)}
def trace(addr, limit=400, bank=0x39):
    """follow a routine (both branch paths, JMP abs, not JSR) and collect what it does:
    pal (LDA #n + JSR $C9EF / STA $069E), chr (LDA #n + STA $064F / JSR $CAA4 / $CAAA), mode (STA $71),
    exit-handler calls (JSR $D540.. with the $73/$72/$0697 values set before), checkpoint, screen tests
    (LDA $57 / CMP #n), effect threads (LDX #n / JSR $C5C7), and whether an RTS is reachable."""
    dis, mem = _dis(bank)
    out = dict(spawns=[], addr=addr, returns=False, pal=[], chr=[], mode=[], exits=[], ckpt=[], screen_tests=[],
               threads=[], calls=[], ends=False, warps=[])
    seen = set(); todo = [(addr, None, None, {})]; n = 0; Y = None
    while todo and n < limit:
        pc, A, X, ctx = todo.pop()
        lastlda57 = False
        while n < limit:
            if pc in seen or pc < 0x8000: break
            seen.add(pc); n += 1
            ln, txt = dis.instruction_at(pc)
            op = mem[pc]; arg = mem[pc + 1] | (mem[pc + 2] << 8) if ln == 3 else mem[pc + 1]
            nxt = pc + ln
            if op == 0xA9: A = arg
            elif op == 0xA2: X = arg
            elif op == 0xA0: Y = arg
            elif op == 0xA5 and arg == 0x57: A = 'scr'
            elif op in (0xA5, 0xAD, 0xB9, 0xBD, 0xB1, 0x68): A = None
            elif op == 0xC9 and A == 'scr': out['screen_tests'].append((pc, arg))
            elif op == 0x85 and arg == 0x71 and A is not None: out['mode'].append((pc, A))
            elif op == 0x85 and arg == 0x73: ctx = dict(ctx, chr=A)
            elif op == 0x85 and arg == 0x72: ctx = dict(ctx, pal=A)
            elif op == 0x8D and arg == 0x0697: ctx = dict(ctx, tgt=A)
            elif op == 0x8D and arg == 0x069E and isinstance(A, int): out['pal'].append((pc, A))
            elif op == 0x8D and arg == 0x064F and isinstance(A, int): out['chr'].append((pc, A))
            elif op == 0x85 and arg == 0x57 and isinstance(A, int): out['warps'].append((pc, A))
            elif op == 0x20:                       # JSR
                if (arg == 0xC9EF or (arg in PAL_HELPERS and PAL_HELPERS[arg] == bank)) and isinstance(A, int):
                    out['pal'].append((pc, A))
                elif arg == 0xCB28 and mem[pc + 3] == 0x41 and isinstance(Y, int): out['spawns'].append((pc, Y))
                elif arg in (0xCAA4, 0xCAAA) and isinstance(A, int): out['chr'].append((pc, A))
                elif arg == 0xC5C7 and isinstance(X, int): out['threads'].append((pc, X))
                elif arg in EXIT_HANDLERS:
                    out['exits'].append((pc, EXIT_HANDLERS[arg], ctx.get('chr'), ctx.get('pal'), ctx.get('tgt')))
                elif arg in (CKPT_ROUTINE, CKPT_ROUTINE + 4): out['ckpt'].append((pc, A))
                elif arg in WARP_ROUTINES and isinstance(A, int): out['warps'].append((pc, A))
                else: out['calls'].append((pc, arg))
                if arg == 0xCB28: nxt += 1         # far call: one inline byte
                A = None if arg not in (0xC9EF, 0xCAA4, 0xCAAA, 0xE46C) else A
            elif op == 0x4C:                       # JMP abs
                if arg in NEVER_RETURN: out['ends'] = True; break
                if arg in INTERP_RESUME: out['returns'] = True; break
                if arg in (CKPT_ROUTINE, CKPT_ROUTINE + 4): out['ckpt'].append((pc, A)); out['returns'] = True; break
                if arg in EXIT_HANDLERS:
                    out['exits'].append((pc, EXIT_HANDLERS[arg], ctx.get('chr'), ctx.get('pal'), ctx.get('tgt')))
                    out['returns'] = True; break
                if (arg == 0xC9EF or (arg in PAL_HELPERS and PAL_HELPERS[arg] == bank)) and isinstance(A, int):
                    out['pal'].append((pc, A))
                elif arg == 0xCB28 and mem[pc + 3] == 0x41 and isinstance(Y, int): out['spawns'].append((pc, Y)); out['returns'] = True; break
                if arg in (0xCAA4, 0xCAAA) and isinstance(A, int): out['chr'].append((pc, A)); out['returns'] = True; break
                if arg == 0xC5C7 and isinstance(X, int): out['threads'].append((pc, X)); out['returns'] = True; break
                nxt = arg
            elif op == 0x6C: break                 # JMP (ind)
            elif op == 0x60: out['returns'] = True; break
            elif op in (0x40, 0x00): break         # RTI / BRK
            elif op in (0x10, 0x30, 0x50, 0x70, 0x90, 0xB0, 0xD0, 0xF0):
                off = mem[pc + 1]; tgt = pc + 2 + (off - 256 if off > 127 else off)
                todo.append((tgt, A, X, ctx))
            pc = nxt
    return out

# ------------------------------------------------------------------------------------------------ screen graph
class Node:
    __slots__ = ('scr', 'x', 'y', 'comp', 'chrs', 'pal', 'how', 'mode', 'pal_id', 'src')
    def __init__(self, **k):
        for a in self.__slots__: setattr(self, a, k.get(a))
    def __repr__(self):
        return 'Node(%02X @%d,%d c%d %s mode %s chr %s pal %s)' % (self.scr, self.x, self.y, self.comp, self.how,
                                                                  self.mode, '/'.join('%02X' % c for c in self.chrs),
                                                                  '%02X' % self.pal_id if self.pal_id is not None else '-')

def scripts_by_screen(s, objs=None):
    objs = objs if objs is not None else decode_objects(s)[0]
    out = {}
    for (sc, x, y, t) in objs:
        if t == 0x80: out.setdefault(sc, []).append(dict(decode_script(y), x=x, scr=sc))
    return out

def screen_effects(d):
    """what the script d does when the camera reaches its screen:
    pre_pal/pre_chr  palette / CHR ids its init applies on the screen itself,
    post_pal/post_chr ids an init applies only after its own exit fired (they reach the next screen),
    exits            [(type, chr, pal, target|None, 'list'|'init'|'pf')],
    warps            [(screen, 'init'|'pf')] (STA $57 / JSR $89F5 teleports),
    pf_pal           [(palette, screen or None)] palettes a per-frame routine loads (None = this screen,
                     n = only when the camera is on screen n: 'LDA $57 / CMP #n'),
    ckpt             checkpoint screen set by the per-frame routine, mode, shutter (1/2) and the boss room flag."""
    out = dict(pre_pal=[], pre_chr=[], post_pal=[], post_chr=[], exits=[], warps=[], pf_pal=[], pf_chr=[],
               ckpt=None, mode=d['mode'], pf=d.get('pf'), shutter=SHUTTERS.get(d.get('pf')),
               boss=d.get('init') == 0xF94A)
    if d.get('init') is not None:
        ii = d['init_info']
        ex_at = [e[0] for e in ii['exits']] + [w[0] for w in ii['warps']]
        first = min(ex_at) if ex_at else 0x10000
        for pc, v in ii['pal']: (out['pre_pal'] if pc < first else out['post_pal']).append(v)
        for pc, v in ii['chr']: (out['pre_chr'] if pc < first else out['post_chr']).append(v)
        for pc, t, c, p, tg in ii['exits']:
            out['exits'].append((t, c if isinstance(c, int) else 0, p if isinstance(p, int) else 0,
                                 tg & 0x7F if isinstance(tg, int) else None, 'init'))
        for pc, v in ii['warps']: out['warps'].append((v, 'init'))
        for pc, v in ii['mode']:
            if pc < first: out['mode'] = v
        for pc, v in ii['ckpt']: out['ckpt'] = v
        for pc, n in ii['threads']:
            tp = thread_palettes(n)
            if tp and pc < first: out['pre_pal'].append(tp[0]); out.setdefault('cyclers', []).append((n, tp))
        for pc, t in ii['spawns']:          # e.g. a fortress boss whose AI loads the room palette
            a = ai(t); ti = trace(a['addr'], 300, a['bank'])
            if ti['pal'] and not any(q < pc for q, _ in ii['pal']): out['pre_pal'].append(ti['pal'][0][1])
            out.setdefault('spawns', []).append(t)
    for t, c, p, tg in d['exits']: out['exits'].append((t, c, p, tg, 'list'))
    pf = out['pf']
    if pf and pf not in SHUTTERS and pf >= 0x8000:
        pi = trace(pf, 200)
        tests = [t[1] for t in pi['screen_tests']]
        cond = tests[0] if len(set(tests)) == 1 else None
        for pc, v in pi['pal']: out['pf_pal'].append((v, cond))
        for pc, v in pi['chr']: out['pf_chr'].append((v, cond))
        for pc, t, c, p, tg in pi['exits']:
            out['exits'].append((t, c if isinstance(c, int) else 0, p if isinstance(p, int) else 0,
                                 tg & 0x7F if isinstance(tg, int) else None, 'pf'))
        for pc, v in pi['warps']: out['warps'].append((v, 'pf'))
        for pc, n in pi['threads']:
            tp = thread_palettes(n)
            if tp: out['pf_pal'].append((tp[0], cond)); out.setdefault('cyclers', []).append((n, tp))
        for pc, v in pi['ckpt']: out['ckpt'] = v
    return out

THREAD_SLOT, THREAD_HI, THREAD_LO, THREAD_BANK = 0xC632, 0xC64D, 0xC668, 0xC683   # $3E, indexed by thread n
def thread_palettes(n):
    """effect thread n (started by LDX #n / JSR $C5C7): if it is one of the bank-$3B palette cyclers
    ('LDY #i / BNE $911C'; data at $3B:$9143+i = delay, palette ids..., 0 = loop, $FF = end), return its
    palette ids in order, else []."""
    a = fixed(THREAD_HI + n) << 8 | fixed(THREAD_LO + n); bank = fixed(THREAD_BANK + n)
    if bank != 0x3B or cpu(a, 0x3B) != 0xA0 or cpu(a + 2, 0x3B) != 0xD0: return []
    if a + 4 + (cpu(a + 3, 0x3B) - 256 if cpu(a + 3, 0x3B) > 127 else cpu(a + 3, 0x3B)) != 0x911C: return []
    i = cpu(a + 1, 0x3B); out = []
    for k in range(1, 40):
        v = cpu(0x9143 + i + k, 0x3B)
        if v in (0, 0xFF): break
        out.append(v)
    return out

DXY = {'down': (0, 1), 'up': (0, -1), 'right': (1, 0), 'left': (-1, 0)}
def walk(s, extra_starts=None):
    """Build the screen graph: a BFS from screen 0 over the scroll modes, the exits (exit list, init and
    per-frame routines), boss shutters and teleports, carrying the cumulative CHR sets and palette.
    Forward edges (scroll right, exits of type 1/2/5, any exit with an explicit target, shutters, warps) are
    taken before back edges (types 3/4/6 without a target, scroll left), so a screen is placed where the
    player first reaches it.  A screen that would land on an occupied grid cell starts a new component.
    Returns {screen: Node}; walk.edges = [(from, to, how)]."""
    import heapq
    st = Stage(s); h = st.hdr
    S = scripts_by_screen(s, st.objects)
    E = {sc: screen_effects(ds[0]) for sc, ds in S.items()}
    pal0 = palette(h['pal'])
    nodes = {}; cells = {}; comp = [0]; pending_pal = {}; seq = [0]; q = []; edges = []
    def push(prio, item):
        seq[0] += 1; heapq.heappush(q, (prio, seq[0], item))
    push(0, (0, 0, 0, 0, (h['chr'],), tuple(pal0), 'start', h['pal'], None))
    for es in (extra_starts or []): push(0, es)
    hub = HUB.get(s)
    while q:
        prio, _, (sc, x, y, cp, chrs, pal, how, pid, src) = heapq.heappop(q)
        if sc in nodes or not 0 <= sc < 32: continue
        if (cp, x, y) in cells:
            comp[0] += 1; cp, x, y = comp[0], 0, 0
        eff = E.get(sc)
        pal = list(pal); chrs = list(chrs)
        for p in pending_pal.pop(sc, []): pal = palette(p, pal); pid = p
        mode = 3
        if eff:
            mode = eff['mode']
            chrs += eff['pre_chr']
            for p in eff['pre_pal']: pal = palette(p, pal); pid = p
            for p, cond in eff['pf_pal']:
                if cond is None or cond == sc: pal = palette(p, pal); pid = p
                elif cond not in nodes: pending_pal.setdefault(cond, []).append(p)
            for c, cond in eff['pf_chr']:
                if cond is None or cond == sc: chrs.append(c)
        nodes[sc] = Node(scr=sc, x=x, y=y, comp=cp, chrs=tuple(chrs), pal=tuple(pal), how=how, mode=mode,
                         pal_id=pid, src=src)
        cells[(cp, x, y)] = sc
        out = []                      # (prio, item)
        spal, schr, spid = list(pal), list(chrs), pid      # what scrolling away carries (init 'post' code)
        if eff:
            # an exit replaces the script thread (the new screen's script takes slot 22), so code after an
            # init's own exit loop runs only when the script scrolls away: 'post' effects go on scroll edges
            pchr = chrs; ppal = list(pal); ppid = pid
            schr = chrs + eff['post_chr']
            for p in eff['post_pal']: spal = palette(p, spal); spid = p
            for t, c, p, tg, kind in eff['exits']:
                if t not in EXIT_DIR: continue
                n = (tg if tg is not None else sc) + EXIT_STEP[t]
                dx, dy = DXY[EXIT_DIR[t]]
                fwd = t in (1, 2, 5) or tg is not None
                c2 = pchr + ([c] if c else []); p2 = palette(p, ppal) if p else ppal
                out.append((0 if fwd else 1, (n, x + dx, y + dy, cp, tuple(c2), tuple(p2),
                                              '%s(%d%s)' % (EXIT_DIR[t], t, '' if kind == 'list' else ',' + kind),
                                              p or ppid, sc)))
            for n, kind in eff['warps']:
                out.append((0, (n, 0, 0, -1, tuple(pchr), tuple(ppal), 'warp(%s)' % kind, ppid, sc)))
            if eff['shutter']:
                out.append((0, (sc + 1, x + 1, y, cp, tuple(chrs), tuple(pal), 'shutter', pid, sc)))
        if hub and sc == hub['screen']:
            for k in range(8):
                bid = r39(hub['ids'] + k); n = hub['first'] + bid
                out.append((0, (n, 0, 0, -1, tuple(chrs), tuple(palette(hub['pal'] + bid, pal)),
                                'teleport %d' % k, hub['pal'] + bid, sc)))
        targets = {o[1][0] for o in out}
        if mode & 1 and sc + 1 not in targets and not (eff and (eff['shutter'] or eff['boss'])):
            out.append((0, (sc + 1, x + 1, y, cp, tuple(schr), tuple(spal), 'scroll', spid, sc)))
        if mode & 2 and sc - 1 not in targets:
            out.append((1, (sc - 1, x - 1, y, cp, tuple(schr), tuple(spal), 'scroll-left', spid, sc)))
        for pr, it in out:
            if it[3] == -1:            # teleport / warp: always its own component
                comp[0] += 1; it = (it[0], 0, 0, comp[0]) + it[4:]
            edges.append((sc, it[0], it[6])); push(pr, it)
    walk.edges = edges
    return nodes

# ------------------------------------------------------------------------------------------------ rendering
def nes_rgb(i):
    from emu import nes_rgb as f
    return f(i)

class Renderer:
    """draw screens of a stage with a given CHR-RAM image and 32-entry palette (BG uses entries 0-15)."""
    def __init__(self, st, chrram, pal32, altbits=None):
        self.st = st if isinstance(st, Stage) else Stage(st)
        self.chr = chrram; self.pal = list(pal32); self.alt = altbits or bytes(32); self.cache = {}
    def mt(self, m):
        from PIL import Image
        alt = bool(self.alt[m >> 3] >> (m & 7) & 1)
        if (m, alt) in self.cache: return self.cache[(m, alt)]
        d = (self.st.alt_metatiles if alt else self.st.metatiles)[m]
        p = d['pal']; pal4 = [nes_rgb(self.pal[0])] + [nes_rgb(self.pal[p * 4 + k]) for k in (1, 2, 3)]
        im = Image.new('RGB', (16, 16)); px = im.load()
        for q, t in enumerate(d['tiles']):
            o = t * 16; ox, oy = (q & 1) * 8, (q >> 1) * 8
            for yy in range(8):
                lo, hi = self.chr[o + yy], self.chr[o + yy + 8]
                for xx in range(8):
                    px[ox + xx, oy + yy] = pal4[(lo >> (7 - xx) & 1) | (hi >> (7 - xx) & 1) << 1]
        self.cache[(m, alt)] = im
        return im
    def screen(self, sc, full=False):
        from PIL import Image
        im = Image.new('RGB', (256, 256))
        for r in range(8):
            for c in range(8):
                b = self.st.screens[sc][r][c]
                for q, m in enumerate(self.st.blocks[b]):
                    im.paste(self.mt(m), (c * 32 + (q & 1) * 16, r * 32 + (q >> 1) * 16))
        return im if full else im.crop((0, 0, 256, 240))
    def collision(self, sc, raw=False):
        """15 x 16 grid of collision nibbles (attr >> 4), remapped through the stage group unless raw."""
        g = []
        for ry in range(15):
            row = []
            for cx in range(16):
                b = self.st.screens[sc][ry >> 1][cx >> 1]
                m = self.st.blocks[b][(ry & 1) * 2 + (cx & 1)]
                v = self.st.metatiles[m]['coll']
                row.append(v if raw else self.st.coll[v])
            g.append(row)
        return g

def screen_tile_ids(st, sc):
    """the 30 x 32 nametable tile ids and 15 x 16 palette numbers a screen produces (for PPU comparisons)."""
    st = st if isinstance(st, Stage) else Stage(st)
    t = [[0] * 32 for _ in range(30)]; p = [[0] * 16 for _ in range(15)]
    for r in range(8):
        for c in range(8):
            b = st.screens[sc][r][c]
            for q, m in enumerate(st.blocks[b]):
                my, mx = r * 2 + (q >> 1), c * 2 + (q & 1)
                if my >= 15: continue
                d = st.metatiles[m]; p[my][mx] = d['pal']
                for k, tile in enumerate(d['tiles']):
                    t[my * 2 + (k >> 1)][mx * 2 + (k & 1)] = tile
    return t, p

OBJ_KIND = {0x37: '1UP', 0x38: 'e', 0x39: 'E', 0x1D: 'ET', 0x49: 'w', 0x4A: 'W', 0x8A: 'BAL'}
def render_map(s, path, scale=None, labels=True, objects=True, max_bytes=1000000, graph=None):
    """stitch every reached screen (and every other screen that holds objects) into one PNG.
    Components (branches that would overlap, unreached screens) are stacked below the main map."""
    from PIL import Image, ImageDraw
    st = Stage(s); g = graph or walk(s)
    used = set(st.used_screens())
    extra = sorted(sc for sc in used if sc not in g)
    comps = {}
    for n in g.values(): comps.setdefault(n.comp, []).append(n)
    # unreached screens: one component each run of consecutive screens, default CHR/palette
    if extra:
        c0 = max(comps) + 1 if comps else 0
        run = []
        for sc in extra:
            if run and sc != run[-1] + 1:
                comps[c0] = [Node(scr=v, x=i, y=0, comp=c0, chrs=(st.hdr['chr'],), pal=tuple(palette(st.hdr['pal'])),
                                  how='unreached', mode=None, pal_id=st.hdr['pal'], src=None) for i, v in enumerate(run)]
                c0 += 1; run = []
            run.append(sc)
        if run:
            comps[c0] = [Node(scr=v, x=i, y=0, comp=c0, chrs=(st.hdr['chr'],), pal=tuple(palette(st.hdr['pal'])),
                              how='unreached', mode=None, pal_id=st.hdr['pal'], src=None) for i, v in enumerate(run)]
    boxes = {}
    for c, ns in comps.items():
        xs = [n.x for n in ns]; ys = [n.y for n in ns]
        boxes[c] = (min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
    W = max(b[2] for b in boxes.values()) * 256
    gap = 24
    H = sum(b[3] * 240 + gap for b in boxes.values())
    im = Image.new('RGB', (W, H), (32, 32, 32)); dr = ImageDraw.Draw(im)
    rcache = {}
    oy = 0
    for c in sorted(comps):
        bx, by, bw, bh = boxes[c]
        if c:
            ns = comps[c]; first = min(ns, key=lambda n: (n.y, n.x))
            src = first.src
            txt = ('branch: screen %02X entered %s from screen %02X' % (first.scr, first.how, src)) if src is not None \
                else 'screens never reached by the walker (default CHR/palette): ' + ' '.join('%02X' % n.scr for n in ns)
            dr.text((4, oy + 6), txt, fill=(255, 255, 255))
            oy += gap
        for n in comps[c]:
            key = (n.chrs, n.pal)
            if key not in rcache: rcache[key] = Renderer(st, chr_ram(n.chrs), n.pal)
            px, py = (n.x - bx) * 256, oy + (n.y - by) * 240
            im.paste(rcache[key].screen(n.scr), (px, py))
            dr.rectangle([px, py, px + 255, py + 239], outline=(110, 110, 110))
            if labels:
                lab = '%02X %s' % (n.scr, n.how)
                dr.rectangle([px, py, px + 6 * len(lab) + 3, py + 10], fill=(0, 0, 0))
                dr.text((px + 2, py), lab, fill=(255, 255, 0))
            if objects:
                for (osc, ox, oyy, t) in st.objects:
                    if osc != n.scr: continue
                    if t == 0x80:
                        dr.rectangle([px + ox - 1, py + 12, px + ox + 22, py + 22], fill=(0, 0, 150))
                        dr.text((px + ox, py + 12), 'S%02X' % oyy, fill=(255, 255, 255))
                    else:
                        yy = min(oyy, 230)
                        lab = OBJ_KIND.get(t, '%02X' % t)
                        col = (0, 255, 128) if t in OBJ_KIND else (255, 96, 255)
                        dr.rectangle([px + ox - 7, py + yy - 5, px + ox + 7 + 6 * (len(lab) - 2), py + yy + 5],
                                     outline=col, fill=(0, 0, 0))
                        dr.text((px + ox - 5, py + yy - 6), lab, fill=col)
        oy += bh * 240 + (0 if c == max(comps) else 0)
        if c != max(comps): oy += 0
    im = im.crop((0, 0, W, oy))
    _save_small(im, path, scale, max_bytes)
    return im

def _save_small(im, path, scale=None, max_bytes=1000000):
    from PIL import Image
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    f = scale or 1.0
    while True:
        out = im if f == 1.0 else im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
        out.save(path, optimize=True)
        if os.path.getsize(path) <= max_bytes or f < 0.2: return f
        f = round(f * 0.8, 3)

def render_strip(s, path, cols=8, screens=None, max_bytes=1000000, scale=0.5):
    """all 32 screens of a stage's layout in index order (reached ones with their walk() CHR/palette,
    the others with the stage's base CHR set and start palette), cols per row, labelled."""
    from PIL import Image, ImageDraw
    st = Stage(s); g = walk(s); used = set(st.used_screens())
    screens = list(range(32)) if screens is None else screens
    rows = (len(screens) + cols - 1) // cols
    im = Image.new('RGB', (cols * 260, rows * 244), (32, 32, 32)); dr = ImageDraw.Draw(im); rc = {}
    for i, sc in enumerate(screens):
        n = g.get(sc)
        key = (n.chrs, n.pal) if n else ((st.hdr['chr'],), tuple(palette(st.hdr['pal'])))
        if key not in rc: rc[key] = Renderer(st, chr_ram(key[0]), key[1])
        px, py = (i % cols) * 260 + 2, (i // cols) * 244 + 2
        im.paste(rc[key].screen(sc), (px, py))
        tag = 'reached' if n else ('objects' if sc in used else 'UNUSED')
        lab = '%02X %s' % (sc, tag)
        dr.rectangle([px, py, px + 6 * len(lab) + 3, py + 10], fill=(0, 0, 0))
        dr.text((px + 2, py), lab, fill=(255, 255, 0) if n else (255, 80, 80))
    return _save_small(im, path, scale, max_bytes)

# ------------------------------------------------------------------------------------------------ round trip
def roundtrip(verbose=True):
    """re-encode every structure from its decoded form and compare with the ROM bytes.
    Returns (rebuilt ROM bytes, report lines).  Covered: the 4 layout banks, the 6 tileset banks (3 sets +
    alternate set each), the object-list region of bank $3A, all 128 screen scripts, all 256 palette
    programs (banks $37 and $28), the CHR set table, and the stage table."""
    rom = bytearray(ROM); rep = []
    def put(off, data, what):
        old = bytes(rom[off:off + len(data)]); ok = old == data
        rom[off:off + len(data)] = data
        rep.append('%-58s 0x%05X %5d bytes %s' % (what, off + 16, len(data), 'OK' if ok else 'DIFF'))
        return ok
    allok = True
    # stage table
    tab = bytearray()
    hs = [header(s) for s in range(16)]
    for f in FIELDS: tab += bytes(h[f] for h in hs)
    allok &= put(boff(0x3E, STAGE_TABLE), bytes(tab), 'stage table $3E:$DF25 (9 x 16)')
    # layouts: whole banks
    for lb in (0x26, 0x27, 0x32, 0x33):
        bank = bytearray(0x2000)
        for s in range(16):
            h = hs[s]
            if h['layout_bank'] != lb: continue
            st = Stage(s); o = ((h['layout_page'] << 8) + h['layout_lo']) & 0x1FFF
            bank[o:o + 0x800] = encode_layout(st.screens)
        allok &= put(lb * 0x2000, bytes(bank), 'layout bank $%02X (4 stages x 8 rows x 256)' % lb)
    # tilesets: whole banks (3 sets + alternate set); unused set slots are decoded/re-encoded too
    for tb in (0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F):
        bank = bytearray(0x2000)
        for pg in (0x80, 0x89, 0x92):
            raw = ROM[boff(tb, pg << 8):boff(tb, pg << 8) + 9 * 256]
            o = (pg << 8) & 0x1FFF
            if not any(hs[s]['tile_bank'] == tb and hs[s]['mt_page'] == pg for s in range(16)):
                bank[o:o + 9 * 256] = raw          # unused slot ($2B:$92, $2D:$92): Capcom fill, kept raw
                continue
            mts, blocks = decode_tileset(raw)
            bank[o:o + 9 * 256] = encode_tileset(mts, blocks)
        alt = decode_metatiles(ROM[boff(tb, 0x9B00):boff(tb, 0x9B00) + 5 * 256])
        bank[0x1B00:0x2000] = encode_metatiles(alt)
        users = [NAMES[s] for s in range(16) if hs[s]['tile_bank'] == tb]
        allok &= put(tb * 0x2000, bytes(bank), 'tileset bank $%02X (%s)' % (tb, ', '.join(users)))
    # object lists: pointer/count tables + lists
    ptr_lo, ptr_hi, cnt, data = bytearray(), bytearray(), bytearray(), bytearray()
    base = r3a(OBJ_PTR_LO) | r3a(OBJ_PTR_HI) << 8
    for s in range(16):
        objs, sent = decode_objects(s)
        p = base + len(data); ptr_lo.append(p & 0xFF); ptr_hi.append(p >> 8); cnt.append(len(objs))
        data += encode_objects(objs, sent)
    allok &= put(boff(0x3A, OBJ_PTR_LO), bytes(ptr_lo + ptr_hi + cnt), 'object list pointers/counts $3A:$80BF')
    allok &= put(boff(0x3A, base), bytes(data), 'object lists $3A:$%04X-$%04X (16 stages)' % (base, base + len(data) - 1))
    # screen scripts
    nsc = 0; bad = []
    for i in range(128):
        d = decode_script(i); enc = encode_script(d)
        o = cpu_off(d['ptr'], 0x39)
        if bytes(rom[o:o + len(enc)]) != enc: bad.append(i)
        rom[o:o + len(enc)] = enc; nsc += len(enc)
    rep.append('%-58s %13d bytes %s' % ('128 screen scripts (bank $39 / fixed)', nsc, 'OK' if not bad else 'DIFF %s' % bad))
    allok &= not bad
    # palettes
    for bank in (PAL_BANK, PAL_BANK_REVISIT):
        n = 0; bad = []
        for pid in range(256):
            p, start, vals = palette_raw(pid, bank)
            enc = encode_palette(start, vals); o = boff(bank, p)
            if bytes(rom[o:o + len(enc)]) != enc: bad.append(pid)
            rom[o:o + len(enc)] = enc; n += len(enc)
        rep.append('%-58s %13d bytes %s' % ('256 palette programs, bank $%02X' % bank, n, 'OK' if not bad else 'DIFF %s' % bad))
        allok &= not bad
    # CHR set table
    t = bytes(v for i in range(256) for v in chr_set(i)['raw'])
    allok &= put(boff(0x37, 0x8000), t, 'CHR set table $37:$8000 (256 x 4)')
    same = bytes(rom) == ROM
    rep.append('rebuilt ROM identical to original: %s' % same)
    if verbose: print('\n'.join(rep))
    return bytes(rom), rep, allok and same

def encode_stage(js):
    """rebuild the ROM bytes of one stage from its exported JSON (see export()).  Returns
    [(what, file offset without header, bytes)]: layout (2 KB), tileset slot (2304 bytes), alternate set
    (1280 bytes, shared by the bank), object list (4 + 4n bytes), stage-table column (9 bytes), and every
    screen script the stage uses."""
    h = js['header']; out = []
    screens = [js['screens']['%02X' % sc] for sc in range(32)]
    out.append(('layout', boff(h['layout_bank'], (h['layout_page'] << 8) + h['layout_lo']), encode_layout(screens)))
    out.append(('tileset', boff(h['tile_bank'], h['mt_page'] << 8), encode_tileset(js['metatiles'], js['blocks'])))
    out.append(('alt set', boff(h['tile_bank'], 0x9B00), encode_metatiles(js['alt_metatiles'])))
    objs = [(o['screen'], o['x'], o['y'], o['type']) for o in js['objects']]
    P = r3a(OBJ_PTR_LO + js['id']) | r3a(OBJ_PTR_HI + js['id']) << 8
    out.append(('objects', boff(0x3A, P), encode_objects(objs, js['sentinels'])))
    for i, f in enumerate(FIELDS):
        out.append(('table %s' % f, boff(0x3E, STAGE_TABLE + 16 * i + js['id']), bytes([h[f]])))
    for k, d in sorted(js['script_defs'].items()):
        out.append(('script %s' % k, cpu_off(d['ptr'], 0x39), encode_script(d)))
    return out

def build_rom(jss, path=None):
    """write a ROM with every stage re-encoded from its JSON dict (jss = list of 16 export() dicts, edited or
    not).  Object lists are re-packed (and their pointer / count tables rewritten), so lists may grow as
    long as all 16 fit in $3A:$85D8-$9FFF.  Returns the ROM bytes (with the iNES header); writes path."""
    rom = bytearray(ROM)
    base = r3a(OBJ_PTR_LO) | r3a(OBJ_PTR_HI) << 8; data = bytearray()
    for js in jss:
        for what, o, b in encode_stage(js):
            if what == 'objects': continue
            rom[o:o + len(b)] = b
        s = js['id']; objs = [(o['screen'], o['x'], o['y'], o['type']) for o in js['objects']]
        objs.sort(key=lambda o: (o[0], o[1]))               # the spawner needs (screen, X) order
        assert len(objs) < 256
        pt = base + len(data)
        rom[boff(0x3A, OBJ_PTR_LO + s)] = pt & 0xFF; rom[boff(0x3A, OBJ_PTR_HI + s)] = pt >> 8
        rom[boff(0x3A, OBJ_COUNT + s)] = len(objs)
        data += encode_objects(objs, js['sentinels'])
    end = base + len(data)
    assert end <= 0xA000, 'object lists overflow bank $3A ($%04X)' % end
    o = boff(0x3A, base); rom[o:o + len(data)] = data
    if end < 0x95D4:                                         # pad what the lists used to occupy with $FF
        rom[boff(0x3A, end):boff(0x3A, 0x95D4)] = b'\xff' * (0x95D4 - end)
    out = HEADER + bytes(rom)
    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True); open(path, 'wb').write(out)
    return out

def json_roundtrip(stages=range(16), outdir=None, verbose=True):
    """export each stage to JSON on disk, read it back, re-encode, and compare every region with the ROM."""
    import tempfile
    outdir = outdir or tempfile.mkdtemp()
    os.makedirs(outdir, exist_ok=True); ok = True; rows = []
    for s in stages:
        p = os.path.join(outdir, '%02d_%s.json' % (s, NAMES[s]))
        json.dump(export(s), open(p, 'w'))
        js = json.load(open(p))
        regs = encode_stage(js); good = sum(ROM[o:o + len(b)] == b for _, o, b in regs)
        nbytes = sum(len(b) for _, o, b in regs)
        bad = [w for w, o, b in regs if ROM[o:o + len(b)] != b]
        ok &= not bad
        rows.append('%2d %-9s %3d regions %6d bytes  %s' % (s, NAMES[s], len(regs), nbytes, 'identical' if not bad else 'DIFF ' + ', '.join(bad)))
    if verbose: print('\n'.join(rows))
    return ok

def appendix():
    """markdown: per stage, one row per screen (placement, entry, script, exits, CHR, palette, objects) and the
    object types with their AI entry, sprite CHR set and HP.  Written to docs/research/rm6/levels_stages.md."""
    L = ['# Rockman 6 (J) stage data, screen by screen (generated by `levels.py appendix`)', '',
         'Companion to `levels.md`. Columns: **pos** = component:x,y of the map grid (y grows downwards),',
         '**entry** = how `walk()` first reached the screen, **script** = id / mode / per-frame kind, **exits** =',
         'direction(type)/CHR/palette/target, **BG CHR** = CHR sets applied so far (base first), **pal** = last',
         'palette id applied, **objects** = type ids in list order (items named), **spr CHR** = the sprite CHR',
         'sets `$3A:$826F` queues for the screen (AI header byte 0). All [code], from ROM data.', '']
    for s in range(16):
        st = Stage(s); g = walk(s); S = scripts_by_screen(s, st.objects)
        h = st.hdr
        L += ['## %d %s' % (s, TITLES[s]), '',
              'layout `$%02X:$%02X00`, tileset `$%02X` (metatiles `$%02X00`, blocks `$%02X00`), base CHR `$%02X`, '
              'palette `$%02X`, music `$%02X`, collision group %d' % (h['layout_bank'], h['layout_page'], h['tile_bank'],
              h['mt_page'], h['blk_page'], h['chr'], h['pal'], h['music'], fixed(COLL_GROUP + s)), '',
              '| scr | pos | entry | script | exits | BG CHR | pal | objects | spr CHR |', '|---|---|---|---|---|---|---|---|---|']
        for sc in sorted(set(g) | set(st.used_screens())):
            n = g.get(sc)
            ds = S.get(sc, [])
            scr_txt = ex_txt = ''
            for d in ds:
                pf = d.get('pf'); kind = ''
                if d.get('init') == 0xF94A: kind = 'boss room'
                elif pf in SHUTTERS: kind = 'shutter %d' % SHUTTERS[pf]
                elif pf:
                    ti = trace(pf, 60); kind = ('ckpt %02X' % ti['ckpt'][0][1]) if ti['ckpt'] and isinstance(ti['ckpt'][0][1], int) else 'pf $%04X' % pf
                if d.get('init') is not None and d.get('init') != 0xF94A:
                    kind = ('init $%04X%s ' % (d['init'], '' if d['returns'] else ' (no return)')) + kind
                scr_txt = 'S%02X m%X %s' % (d['idx'], d['mode'], kind)
                ex_txt = ' '.join('%s(%d)/%02X/%02X%s' % (EXIT_DIR.get(t, '?'), t, c, p, '/%02X' % tg if tg is not None else '')
                                  for t, c, p, tg in d['exits'])
            objs = [o for o in st.objects if o[0] == sc and o[3] != 0x80]
            ot = ' '.join(OBJ_KIND.get(o[3], '%02X' % o[3]) for o in objs)
            spr = sorted({ai(o[3])['chr'] for o in objs} - {0})
            L.append('| %02X | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                sc, '%d:%d,%d' % (n.comp, n.x, n.y) if n else '-', n.how if n else 'not reached', scr_txt, ex_txt,
                ' '.join('%02X' % c for c in n.chrs) if n else '', '%02X' % n.pal_id if n and n.pal_id is not None else '',
                ot, ' '.join('%02X' % c for c in spr)))
        types = sorted({o[3] for o in st.objects if o[3] != 0x80})
        L += ['', 'Object types: ' + ', '.join('`%02X` (AI $%02X:$%04X, CHR %02X, HP %d)' % (
            t, ai(t)['bank'], ai(t)['addr'], ai(t)['chr'], ai(t)['hp']) for t in types), '']
    return '\n'.join(L) + '\n'

# ------------------------------------------------------------------------------------------------ export / info
def export(s):
    st = Stage(s); g = walk(s)
    S = scripts_by_screen(s, st.objects)
    return dict(id=s, name=st.name, title=TITLES[s], header=st.hdr, collision_remap=st.coll,
                screens={'%02X' % sc: st.screens[sc] for sc in range(32)},
                blocks=st.blocks, metatiles=[{k: m[k] for k in ('tiles', 'pal', 'coll')} for m in st.metatiles],
                alt_metatiles=[{k: m[k] for k in ('tiles', 'pal', 'coll')} for m in st.alt_metatiles],
                script_defs={'%02X' % d['idx']: {k: v for k, v in d.items() if k != 'init_info'}
                             for d in (decode_script(i) for i in sorted({o[2] for o in st.objects if o[3] == 0x80}))},
                objects=[dict(screen=o[0], x=o[1], y=o[2], type=o[3]) for o in st.objects], sentinels=st.obj_sentinels,
                scripts={'%02X' % sc: [{k: v for k, v in d.items() if k != 'init_info'} for d in ds] for sc, ds in S.items()},
                graph={'%02X' % k: dict(x=n.x, y=n.y, comp=n.comp, how=n.how, mode=n.mode, chr=list(n.chrs),
                                        pal_id=n.pal_id, pal=list(n.pal), src=n.src) for k, n in g.items()})

def info(s):
    st = Stage(s)
    print('== stage %d %s  %s' % (s, st.name, ' '.join('%s=%02X' % (k, v) for k, v in st.hdr.items())))
    print('   collision remap', ' '.join('%X' % v for v in st.coll))
    for sc, ds in sorted(scripts_by_screen(s, st.objects).items()):
        for d in ds:
            ii = d.get('init_info')
            print('   scr %02X x%02X S%02X ptr %04X init %s mode %02X pf %s exits %s %s' % (
                sc, d['x'], d['idx'], d['ptr'], '%04X%s' % (d['init'], '' if ii['returns'] else '!') if d['init'] else '-',
                d['mode'], '%04X' % d['pf'] if d['pf'] else '-',
                ' '.join('%s/%02X/%02X/%s' % (EXIT_DIR.get(t, t), c, p, '%02X' % tg if tg is not None else '-')
                         for t, c, p, tg in d['exits']),
                ('init: pal %s chr %s exits %s' % (['%02X' % v for _, v in ii['pal']], ['%02X' % v for _, v in ii['chr']],
                                                   [(t, c, p, tg) for _, t, c, p, tg in ii['exits']])) if ii else ''))
    g = walk(s)
    for sc in sorted(g): print('  ', g[sc])

if __name__ == '__main__':
    a = sys.argv[1:] or ['info']
    if a[0] == 'info':
        for s in ([int(v) for v in a[1:]] or range(16)): info(s)
    elif a[0] == 'roundtrip':
        _, _, ok = roundtrip()
        print('-- JSON round trip (export -> file -> load -> encode -> compare):')
        ok &= json_roundtrip(outdir=os.path.join(_REPO, 'build', 'research', 'rm6', 'rm6-levels', 'json'))
        sys.exit(0 if ok else 1)
    elif a[0] == 'maps':
        for s in ([int(v) for v in a[1:]] or range(16)):
            p = os.path.join(_REPO, 'docs', 'research', 'rm6', 'img', 'maps', '%02d_%s.png' % (s, NAMES[s]))
            render_map(s, p); print('wrote', p, os.path.getsize(p))
    elif a[0] == 'appendix':
        p = os.path.join(_REPO, 'docs', 'research', 'rm6', 'levels_stages.md')
        open(p, 'w').write(appendix()); print('wrote', p)
    elif a[0] == 'strips':
        for s in ([int(v) for v in a[1:]] or range(16)):
            p = os.path.join(_REPO, 'build', 'research', 'rm6', 'rm6-levels', 'strip_%02d_%s.png' % (s, NAMES[s]))
            render_strip(s, p); print('wrote', p, os.path.getsize(p))
    elif a[0] == 'json':
        os.makedirs(a[1], exist_ok=True)
        for s in range(16):
            json.dump(export(s), open(os.path.join(a[1], '%02d_%s.json' % (s, NAMES[s])), 'w'))
        print('wrote', a[1])
