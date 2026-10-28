"""Rockman 6 (J) text toolkit: PPU scripts (all story/menu text), the intro bytecode and the boss-intro panel.

Written by agent rm6-text; documented in docs/research/rm6/text.md.

    python3 -I tools/analysis/rm6/rm6_ppuscript.py roms/rm6j.nes text            # all text, right table per script
    python3 -I tools/analysis/rm6/rm6_ppuscript.py roms/rm6j.nes dump 5C 6C      # every command of some scripts
    python3 -I tools/analysis/rm6/rm6_ppuscript.py roms/rm6j.nes intro           # intro cutscene bytecode
    python3 -I tools/analysis/rm6/rm6_ppuscript.py roms/rm6j.nes boss            # boss-intro panel records
    python3 -I tools/analysis/rm6/rm6_ppuscript.py roms/rm6j.nes selftest        # re-encode all 168 scripts

Library use:

    from rm6_ppuscript import *
    prg = load_prg('roms/rm6j.nes'); ops = parse(prg, 0x5C)
    tbl = load_tbl('docs/research/rm6/tables/rm6_main.tbl')
    data = encode([text_cmd(0x22C6, 'しょうぶだ!!', tbl)])     # -> bytes for a new script (ends with $00)

PPU-script format (interpreter $3C:$8631, pointer table lo $3C:$8787 / hi $3C:$882F, 168 entries):
    b0 = 0: end.  b0 & $3F = count (1-63), b0 & $40 = CONTINUE (no address), b0 & $80 = SEQUENCE (1 payload byte s:
    writes s, s+1, ...).  Unless CONTINUE, b1: & $40 = SKIP (addr = end of previous write + (b1 & $3F)), else absolute
    (hi = (b1 & $3F) | RAM $F1, lo = b2).  b1 & $80 = RLE (1 payload byte repeated).  Default payload: count literal
    bytes.  Nametable addresses are $20xx-$2Bxx, attributes $23C0+/$27C0+, palette $3F00+.
"""
import sys, unicodedata

BANK3C = 0x3C * 0x2000          # CPU $8000-$BFFF = banks $3C/$3D
N_SCRIPTS = 168

def load_prg(rom_path):
    rom = open(rom_path, 'rb').read()
    return rom[16:16 + 0x80000]

def cpu2off(cpu):
    """CPU address in $8000-$BFFF (banks $3C/$3D mapped) -> PRG offset (file offset = +16)."""
    return BANK3C + cpu - 0x8000

def pointers(prg):
    lo = prg[cpu2off(0x8787):cpu2off(0x8787) + N_SCRIPTS]
    hi = prg[cpu2off(0x882F):cpu2off(0x882F) + N_SCRIPTS]
    return [l | h << 8 for l, h in zip(lo, hi)]

def parse(prg, sid, f1=0x20):
    """Return the list of commands of script sid: dicts addr, mode (lit/rle/seq), kind (abs/skip/cont), data, raw."""
    i = cpu2off(pointers(prg)[sid]); ops = []; addr = 0
    while True:
        start = i; b0 = prg[i]; i += 1
        if b0 == 0:
            break
        n = b0 & 0x3F
        rle = False
        if b0 & 0x40:
            kind = 'cont'
        else:
            b1 = prg[i]; i += 1
            if b1 & 0x40:
                addr += b1 & 0x3F; kind = 'skip'
            else:
                addr = (((b1 & 0x3F) | f1) << 8) | prg[i]; i += 1; kind = 'abs'
            rle = bool(b1 & 0x80)
        a0 = addr; addr += n
        if b0 & 0x80:
            s = prg[i]; i += 1; data = bytes((s + k) & 0xFF for k in range(n)); mode = 'seq'
        elif rle:
            v = prg[i]; i += 1; data = bytes([v]) * n; mode = 'rle'
        else:
            data = bytes(prg[i:i + n]); i += n; mode = 'lit'
        ops.append(dict(addr=a0, mode=mode, kind=kind, data=data, raw=bytes(prg[start:i])))
    return ops

def encode(ops, f1=0x20):
    """Encode commands back to script bytes (+ terminating $00). Each op: dict(addr, mode, data[, kind]).
    Uses CONTINUE when the address follows the previous write, SKIP for short forward jumps, else absolute."""
    out = bytearray(); end = None
    for op in ops:
        a, mode, data = op['addr'], op.get('mode', 'lit'), bytes(op['data'])
        n = len(data)
        assert 1 <= n <= 63, 'count must be 1..63'
        kind = op.get('kind')
        if kind is None:
            if end is not None and a == end and mode == 'lit':
                kind = 'cont'
            elif end is not None and 0 <= a - end < 0x40:
                kind = 'skip'
            else:
                kind = 'abs'
        b0 = n | (0x80 if mode == 'seq' else 0) | (0x40 if kind == 'cont' else 0)
        out.append(b0)
        if kind == 'cont':
            assert mode != 'rle', 'RLE cannot use CONTINUE (the flag lives in byte 1)'
        elif kind == 'skip':
            out.append(0x40 | (a - end) | (0x80 if mode == 'rle' else 0))
        else:
            hi = a >> 8
            assert 0x20 <= hi <= 0x3F, 'absolute address must be $2000-$3FFF'
            out.append((hi & 0x3F) | (0x80 if mode == 'rle' else 0)); out.append(a & 0xFF)   # engine ORs in $F1
        if mode == 'seq':
            out.append(data[0])
        elif mode == 'rle':
            out.append(data[0])
        else:
            out += data
        end = a + n
    out.append(0)
    return bytes(out)

# ---------------------------------------------------------------- tables / text
def load_tbl(path):
    t = {}
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1); t[int(k, 16)] = v
    return t

def decode(data, tbl, unk='[%02X]'):
    return ''.join(tbl.get(b, unk % b) for b in data)

def merge_dakuten(s):
    """は゛ -> ば, は゜ -> ぱ (display form; the ROM stores two tiles)."""
    out = ''
    for ch in s:
        if ch in '゛゜' and out:
            c = unicodedata.normalize('NFC', out[-1] + ('゙' if ch == '゛' else '゚'))
            if len(c) == 1:
                out = out[:-1] + c; continue
        out += ch
    return out

def split_dakuten(s):
    """ば -> は゛ (ROM form)."""
    out = ''
    for ch in s:
        d = unicodedata.normalize('NFD', ch)
        if len(d) == 2 and d[1] in '゙゚':
            out += d[0] + ('゛' if d[1] == '゙' else '゜')
        else:
            out += ch
    return out

def encode_text(s, tbl):
    """Text -> tile bytes with a table (greedy longest match, so 'r.' becomes the Dr./Mr. ligature)."""
    inv = {}
    for k, v in sorted(tbl.items()):
        inv.setdefault(v, k)
    s = split_dakuten(s); out = bytearray(); i = 0
    keys = sorted(inv, key=len, reverse=True)
    while i < len(s):
        for k in keys:
            if k and s.startswith(k, i):
                out.append(inv[k]); i += len(k); break
        else:
            raise ValueError('no tile for %r in %r' % (s[i], s))
    return bytes(out)

def text_cmd(addr, s, tbl):
    return dict(addr=addr, mode='lit', data=encode_text(s, tbl))

def rc(row, col, nt=0):
    """Nametable address of row/col (nt 0-3)."""
    return 0x2000 + nt * 0x400 + row * 32 + col

# Which table each script uses (see docs/research/rm6/text.md section 3)
def table_name(sid):
    if sid == 0x00: return 'title'
    if sid == 0x07: return 'license07'
    if sid in (0x08, 0x09): return 'debug_ascii'
    if 0x0A <= sid <= 0x11 or 0x38 <= sid <= 0x40 or sid in (0x89, 0x8A): return 'pause'
    if sid == 0x12 or 0x71 <= sid <= 0x80: return 'stagesel'
    if sid == 0x13: return 'bossintro_labels'
    if sid in (0x6C, 0x6D, 0x6E): return 'main_hi'
    return 'main'

TEXT_SCRIPTS = ([0x00, 0x07, 0x08, 0x0A, 0x12, 0x16, 0x18, 0x19, 0x1A, 0x1F] + list(range(0x38, 0x41)) +
                [0x49, 0x4A, 0x50, 0x51, 0x52, 0x5C, 0x5E] + list(range(0x5F, 0x6F)) + list(range(0x70, 0x8B)) +
                list(range(0x92, 0x97)))

def text_lines(prg, sid, tables):
    t = dict(tables[table_name(sid)])
    if 0x81 <= sid <= 0x87:
        t.update(tables['staffroll_roles'])
    out = []
    for o in parse(prg, sid):
        a = o['addr']
        if a >= 0x3F00 or (a & 0x3FF) >= 0x3C0 or o['mode'] != 'lit':
            continue
        known = sum(1 for b in o['data'] if b in t and not t[b].startswith('['))
        if known < max(1, len(o['data']) * 0.6):
            continue
        out.append((a, decode(o['data'], t).replace('_', ' ').rstrip()))
    return out

# ---------------------------------------------------------------- intro bytecode / boss panel
INTRO_OPS = {0: 'CLRSCR', 1: 'PALETTE', 2: 'DRAW', 3: 'CHRSET', 4: 'FADEIN', 5: 'WAIT', 6: 'FADEOUT+CALL', 7: 'SAVEPAL',
             8: 'FADEIN_BG', 9: 'FADEIN_ALL', 0xA: 'FADEOUT_BG', 0xB: 'FADEOUT_ALL', 0xC: 'MRX_SPRITE', 0xD: 'TYPE',
             0xE: 'RUSH_SPRITES'}

def intro_program(prg):
    """(cpu_addr, op, name, arg) of the intro bytecode at $3D:$BD7C (run by $3D:$BD00)."""
    i = 0xBD7C; out = []
    while prg[cpu2off(i)] < 0x80:
        op, arg = prg[cpu2off(i)], prg[cpu2off(i) + 1]
        out.append((i, op, INTRO_OPS.get(op, '?'), arg)); i += 2
    return out

BOSS_FIELDS = ['HEIGHT', 'WEIGHT', 'ATTACK', 'DEFENCE', 'MOBILE', 'ENERGY', 'LOCATION', 'SPECIALTY', 'NAME']

def boss_records(prg, tbl):
    """8 boss-intro panel records ($3C:$832E..., pointers $8606/$860E), each 9 fields ended by a byte >= $80."""
    lo = prg[cpu2off(0x8606):cpu2off(0x8606) + 8]; hi = prg[cpu2off(0x860E):cpu2off(0x860E) + 8]
    recs = []
    for l, h in zip(lo, hi):
        i = cpu2off(l | h << 8); fields = []; cur = bytearray()
        while len(fields) < 9:
            c = prg[i]; i += 1
            if c & 0x80:
                fields.append(decode(cur, tbl).strip()); cur = bytearray()
            else:
                cur.append(c)
        recs.append(dict(zip(BOSS_FIELDS, fields)))
    return recs

def _tables(root='docs/research/rm6/tables/'):
    names = ['main', 'main_hi', 'stagesel', 'pause', 'staffroll_roles', 'bossintro_labels', 'title', 'license07',
             'debug_ascii']
    return {n: load_tbl(root + 'rm6_%s.tbl' % n) for n in names}

if __name__ == '__main__':
    prg = load_prg(sys.argv[1]); cmd = sys.argv[2] if len(sys.argv) > 2 else 'text'
    ptr = pointers(prg)
    if cmd == 'text':
        T = _tables()
        for sid in TEXT_SCRIPTS:
            lines = text_lines(prg, sid, T)
            if not lines:
                continue
            print('## script %02X  $%04X  file 0x%05X  [%s]' % (sid, ptr[sid], cpu2off(ptr[sid]) + 16, table_name(sid)))
            for a, s in lines:
                print('  $%04X r%02d c%02d  %s' % (a, (a & 0x3FF) // 32, a % 32, merge_dakuten(s)))
    elif cmd == 'dump':
        for x in sys.argv[3:]:
            sid = int(x, 16); print('== script %02X $%04X' % (sid, ptr[sid]))
            for o in parse(prg, sid):
                print('  $%04X %-4s %-4s %s' % (o['addr'], o['kind'], o['mode'], o['data'].hex(' ')))
    elif cmd == 'intro':
        for a, op, name, arg in intro_program(prg):
            print('$%04X %X %-12s %02X' % (a, op, name, arg))
    elif cmd == 'boss':
        for r in boss_records(prg, _tables()['main']):
            print(r)
    elif cmd == 'selftest':
        bad = 0
        for sid in range(N_SCRIPTS):
            ops = parse(prg, sid); raw = b''.join(o['raw'] for o in ops) + b'\0'
            enc = encode(ops)
            if enc != raw:
                bad += 1; print('mismatch', '%02X' % sid)
        T = _tables()
        assert encode_text('しょうぶだ!! Dr.ワイリー', T['main']) == bytes.fromhex('4b71425b3e4f3e2929000e3275343d26')
        print('selftest: %d/%d scripts re-encode byte-identically' % (N_SCRIPTS - bad, N_SCRIPTS))
