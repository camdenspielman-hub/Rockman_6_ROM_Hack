"""Headless NES harness on stable-retro's FCEUmm core (MMC3/MMC5, CHR-RAM, battery RAM).

    import sys; sys.path.insert(0, 'tools/analysis')
    from emu import Emu, BTN
    e = Emu('roms/rm6j.nes')            # LIB defaults to <repo>/.pylib or $R6_PYLIB
    e.run(120)                          # idle frames
    e.tap('START'); e.run(60)           # press for 2 frames, release
    e.hold(['RIGHT', 'B'], 90)          # hold buttons for N frames
    e.shot('build/shots/x.png')         # what the TV shows (240x224, overscan cropped)
    e.peek(0x00F3); e.poke(0x06C0, 28)  # CPU RAM $0000-$07FF, ExRAM $5C00-$5FFF, WRAM $6000-$7FFF
    e.freeze(0x06C0, 28)                # re-poke every frame (cheats: HP, lives, energy)
    e.save('s.state'); e.load('s.state')
    e.ppu()                             # dict: chr (8 KB), nt (2 KB), pal (32), oam (256), ctrl ($2000 shadow)
    e.render_nametables('nt.png')       # both nametables, 512x240, using live CHR + palette
    e.render_chr('chr.png')             # live CHR-RAM as two 128x128 sheets
Buttons: A B SELECT START UP DOWN LEFT RIGHT.  Player 2 via player=1.
"""
import glob, importlib.util, os, shutil, struct, sys, tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.environ.get('R6_PYLIB', os.path.join(_HERE, '..', '..', '.pylib'))
if LIB not in sys.path:
    sys.path.insert(0, LIB)
import numpy as np
from PIL import Image

_R = None
def _core():
    global _R
    if _R is None:
        lib = os.path.join(LIB, 'stable_retro')
        spec = importlib.util.spec_from_file_location('_retro', glob.glob(lib + '/_retro*.so')[0])
        _R = importlib.util.module_from_spec(spec); spec.loader.exec_module(_R)
        _R.core_path(lib + '/cores')
        _R.RetroEmulator.load_core_info(open(lib + '/cores/fceumm.json').read())
    return _R

# retro NES button order: B, (unused), SELECT, START, UP, DOWN, LEFT, RIGHT, A
BTN = {'B': 0, 'SELECT': 2, 'START': 3, 'UP': 4, 'DOWN': 5, 'LEFT': 6, 'RIGHT': 7, 'A': 8}

# 2C02 palette (FCEUX default) for nametable/CHR renders
_PAL = [int(x, 16) for x in (
 '747474 24188C 0000A8 44009C 8C0074 A80010 A40000 7C0800 402C00 004400 005000 003C14 183C5C 000000 000000 000000 '
 'BCBCBC 0070EC 2038EC 8000F0 BC00BC E40058 D82800 C84C0C 887000 009400 00A800 009038 008088 000000 000000 000000 '
 'FCFCFC 3CBCFC 5C94FC CC88FC F478FC FC74B4 FC7460 FC9838 F0BC3C 80D010 4CDC48 58F898 00E8D8 787878 000000 000000 '
 'FCFCFC A8E4FC C4D4FC D4C8FC FCC4FC FCC4D8 FCBCB0 FCD8A8 FCE4A0 E0FCA0 A8F0BC B0FCCC 9CFCF0 C4C4C4 000000 000000'
).split()]
def nes_rgb(i):
    v = _PAL[i & 0x3F]; return (v >> 16, (v >> 8) & 255, v & 255)

def _chunks(state):
    """Parse an FCEUX 'FCS' savestate into {name: bytes}."""
    out, i = {}, 16
    while i + 5 <= len(state):
        size = struct.unpack_from('<I', state, i + 1)[0]; j, end = i + 5, i + 5 + size
        while j + 8 <= end:
            name = state[j:j + 4].rstrip(b'\0').decode('latin1'); n = struct.unpack_from('<I', state, j + 4)[0]
            out[name] = state[j + 8:j + 8 + n]; j += 8 + n
        i = end
    return out

class Emu:
    def __init__(self, rom, state=None):
        R = _core()
        self._tmp = tempfile.mkdtemp(); path = os.path.join(self._tmp, 'game.nes'); shutil.copy(rom, path)
        self.e = R.RetroEmulator(path); self.d = R.GameDataGlue(); self.e.configure_data(self.d)
        self.frame = 0; self._frozen = {}; self._mask = [np.zeros(16, np.uint8), np.zeros(16, np.uint8)]
        if state: self.load(state)

    # --- input / time -------------------------------------------------
    def _set(self, buttons, player=0):
        m = np.zeros(16, np.uint8)
        for b in ([buttons] if isinstance(buttons, str) else buttons or []): m[BTN[b.upper()]] = 1
        self._mask[player] = m
    def step(self, buttons=None, player=0):
        self._set(buttons, player)
        self.e.set_button_mask(self._mask[0], 0); self.e.set_button_mask(self._mask[1], 1)
        self.e.step(); self.frame += 1
        for a, v in self._frozen.items(): self.poke(a, v)
    def run(self, n, buttons=None, player=0):
        for _ in range(n): self.step(buttons, player)
    hold = lambda self, buttons, n, player=0: self.run(n, buttons, player)
    def tap(self, buttons, frames=2, after=0, player=0):
        self.run(frames, buttons, player); self.run(max(after, 1), None, player)

    # --- memory ---------------------------------------------------------
    def peek(self, a): return self.d.memory.extract(a, '|u1')
    def poke(self, a, v): self.d.memory.assign(a, '|u1', v & 0xFF)
    def peek16(self, a): return self.peek(a) | self.peek(a + 1) << 8
    def ram(self, start=0, n=0x800): return bytes(self.peek(a) for a in range(start, start + n))
    def freeze(self, a, v): self._frozen[a] = v
    def unfreeze(self, a=None):
        if a is None: self._frozen.clear()
        else: self._frozen.pop(a, None)

    # --- states ---------------------------------------------------------
    def save(self, path=None):
        s = self.e.get_state()
        if path: open(path, 'wb').write(s)
        return s
    def load(self, path_or_bytes):
        s = open(path_or_bytes, 'rb').read() if isinstance(path_or_bytes, str) else path_or_bytes
        self.e.set_state(s)

    # --- video ----------------------------------------------------------
    def screen(self): return self.e.get_screen()
    def shot(self, path, scale=1):
        im = Image.fromarray(self.screen())
        if scale != 1: im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True); im.save(path); return path
    def ppu(self):
        c = _chunks(self.save())
        ppur = c.get('PPUR', b'\0\0\0\0')
        return {'chr': c.get('CHRR', b''), 'nt': c.get('NTAR', b''), 'pal': c.get('PRAM', b''),
                'oam': c.get('SPRA', b''), 'ctrl': ppur[0], 'mask': ppur[1], 'chunks': sorted(c)}
    @staticmethod
    def _tile(chr_, idx, pal4):
        t = chr_[idx * 16: idx * 16 + 16]; px = np.zeros((8, 8, 3), np.uint8)
        for y in range(8):
            lo, hi = t[y], t[y + 8]
            for x in range(8):
                c = ((lo >> (7 - x)) & 1) | (((hi >> (7 - x)) & 1) << 1); px[y, x] = pal4[c]
        return px
    def render_nametables(self, path):
        p = self.ppu(); chr_, nt, pal = p['chr'], p['nt'], p['pal']; base = 256 if p['ctrl'] & 0x10 else 0
        img = np.zeros((240, 512, 3), np.uint8)
        for n in range(2):
            t = nt[n * 1024:(n + 1) * 1024]
            for ty in range(30):
                for tx in range(32):
                    at = t[0x3C0 + (ty // 4) * 8 + tx // 4]; sh = ((ty % 4) // 2) * 4 + ((tx % 4) // 2) * 2
                    pi = (at >> sh) & 3
                    pal4 = [nes_rgb(pal[0])] + [nes_rgb(pal[pi * 4 + k]) for k in (1, 2, 3)]
                    img[ty * 8:ty * 8 + 8, n * 256 + tx * 8:n * 256 + tx * 8 + 8] = self._tile(chr_, base + t[ty * 32 + tx], pal4)
        Image.fromarray(img).save(path); return path
    def render_chr(self, path, palette=None):
        chr_ = self.ppu()['chr']; pal4 = palette or [(0, 0, 0), (85, 85, 85), (170, 170, 170), (255, 255, 255)]
        img = np.zeros((128, 256, 3), np.uint8)
        for i in range(512):
            x, y = (i % 16) * 8 + (128 if i >= 256 else 0), ((i % 256) // 16) * 8
            img[y:y + 8, x:x + 8] = self._tile(chr_, i, pal4)
        Image.fromarray(img).resize((512, 256), Image.NEAREST).save(path); return path

    # --- exploration helpers ------------------------------------------------
    def record(self, n, every=30, buttons=None):
        """Run n frames (buttons: list/str, or callable(emu, i) -> buttons) and grab a frame every `every`."""
        frames = []
        for i in range(n):
            self.step(buttons(self, i) if callable(buttons) else buttons)
            if i % every == every - 1: frames.append(Image.fromarray(self.screen()))
        return frames
    def cpu(self):
        """CPU registers from the savestate: dict PC/A/X/Y/S/P (PC = where the game is executing)."""
        c = _chunks(self.save()); g = lambda k, n=1: int.from_bytes(c.get(k, b'\0' * n)[:n], 'little')
        return {'PC': g('PC', 2), 'A': g('A'), 'X': g('X'), 'Y': g('Y'), 'S': g('S'), 'P': g('P')}

def contact(images, path, cols=6, scale=1, labels=None):
    """Tile a list of PIL images into one contact sheet (fast way to review a run)."""
    from PIL import ImageDraw
    if not images: return None
    w, h = images[0].width * scale, images[0].height * scale; rows = (len(images) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * h))
    for i, im in enumerate(images):
        x, y = (i % cols) * w, (i // cols) * h; sheet.paste(im.resize((w, h), Image.NEAREST), (x, y))
        if labels: ImageDraw.Draw(sheet).text((x + 2, y + 2), str(labels[i]), fill=(255, 255, 0))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True); sheet.save(path); return path

def chr_sheet(data, path, cols=16, scale=2):
    """Render raw bytes as 2bpp tiles (static graphics discovery in PRG)."""
    n = len(data) // 16; rows = (n + cols - 1) // cols; img = np.zeros((rows * 8, cols * 8, 3), np.uint8)
    pal4 = [(0, 0, 0), (85, 85, 85), (170, 170, 170), (255, 255, 255)]
    for i in range(n):
        img[(i // cols) * 8:(i // cols) * 8 + 8, (i % cols) * 8:(i % cols) * 8 + 8] = Emu._tile(data, i, pal4)
    Image.fromarray(img).resize((cols * 8 * scale, rows * 8 * scale), Image.NEAREST).save(path); return path

if __name__ == '__main__':
    # quick self-test: python3 emu.py rom.nes out_prefix
    e = Emu(sys.argv[1]); e.run(300); e.tap('START'); e.run(200)
    print('frame', e.frame, 'ppu chunks', e.ppu()['chunks'])
    e.shot(sys.argv[2] + '_screen.png'); e.render_nametables(sys.argv[2] + '_nt.png'); e.render_chr(sys.argv[2] + '_chr.png')
