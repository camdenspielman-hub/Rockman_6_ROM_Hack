"""(cx-stages-2) python3 -I bossgal.py <boss-state> <out> [frames] [policy]: godmode; for each new object type in slots $10-$1F crop it (with the boss)
10 frames after it appears; label type, frame, boss type."""
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx')
from emu import Emu, contact
import cheats as cx
from PIL import Image, ImageDraw
st, out = sys.argv[1], sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 4000; pol = sys.argv[4] if len(sys.argv) > 4 else 'walk'
e = Emu('roms/cx_en.nes'); e.load(cx.state(st)); e.run(1); cx.godmode(e); g = e.peek
pend = {}; done = set(); ims = []
for t in range(N):
    b = []
    if pol == 'walk': b = ['LEFT' if (t // 90) % 2 else 'RIGHT'] + (['A'] if t % 45 < 12 else [])
    if pol == 'jump' and t % 60 < 20: b = ['A']
    e.step(b)
    for s in range(16, 32):
        if not g(0x420 + s) & 0x80: continue
        ty = g(0x400 + s)
        if ty in done: continue
        if ty not in pend: pend[ty] = (t, s)
        elif t - pend[ty][0] == 8:
            ss = pend[ty][1]; x, y = g(0x460 + ss), g(0x4a0 + ss); done.add(ty)
            im = Image.fromarray(e.screen()); x0 = max(0, min(256 - 112, x - 56)); y0 = max(0, min(224 - 96, y - 8 - 48))
            c = im.crop((x0, y0, x0 + 112, y0 + 96)).resize((224, 192), Image.NEAREST)
            d = ImageDraw.Draw(c); d.rectangle((0, 0, 120, 10), fill=(0, 0, 0)); d.text((2, -1), 'obj %02X t%d boss %02X' % (ty, t, g(0x401)), fill=(255, 255, 0))
            ims.append(c); print('obj %02X first t %d at %02X,%02X' % (ty, pend[ty][0], x, y))
contact(ims, out, cols=6)
