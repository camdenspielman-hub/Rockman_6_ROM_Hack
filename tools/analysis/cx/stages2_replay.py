"""(cx-stages-2) python3 -I replay.py <start-state> <tag> [every]: replay <tag>.path (tour2, godmode+onehit) and write
<tag>_tour_NN.png sheets (one frame per `every` frames, room/x/y stamped) and <tag>_log.txt (room entries, objects seen)."""
import sys, json; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx'); sys.path.insert(0, 'tools/analysis/cx')
from emu import Emu, contact
import cheats as cx, stages2_tour as tour2
from PIL import Image, ImageDraw
D = 'build/research/cx/cx-stages-2/'
start, tag = sys.argv[1], sys.argv[2]; every = int(sys.argv[3]) if len(sys.argv) > 3 else 16
path = json.load(open(D + tag + '.path'))
e = Emu('roms/cx_en.nes'); e.load(cx.state(start) if '/' not in start else start); e.run(1); cx.godmode(e); e.step(None)
g = e.peek; fr = []; t = 0; room = None; log = []; seen = {}
for a, n in path:
    act = tour2.ACTS[a]; mash = any(b.endswith('*') for b in act)
    for j in range(n):
        tour2.step(e, cx._press(act, j) if mash else act, True); t += 1
        if g(0x440) != room:
            room = g(0x440); log.append('t %5d room %02X x %02X y %02X' % (t, room, g(0x460), g(0x4a0)))
        for s in range(16, 32):
            if g(0x420 + s) & 0x80:
                k = (room, g(0x400 + s))
                if k not in seen: seen[k] = t
        if t % every == 0:
            im = Image.fromarray(e.screen()); d = ImageDraw.Draw(im)
            d.rectangle((0, 0, 92, 9), fill=(0, 0, 0)); d.text((1, -1), 't%d r%02X %02X,%02X' % (t, room, g(0x460), g(0x4a0)), fill=(255, 255, 0))
            fr.append(im)
for i in range(0, len(fr), 48): contact(fr[i:i + 48], D + '%s_tour_%02d.png' % (tag, i // 48), cols=8)
rooms = {}
for (r, ty), tt in seen.items(): rooms.setdefault(r, []).append('%02X' % ty)
log += ['room %02X objects: %s' % (r, ' '.join(sorted(v))) for r, v in sorted(rooms.items())]
open(D + tag + '_log.txt', 'w').write('\n'.join(log)); print('\n'.join(log)); print('sheets', (len(fr) + 47) // 48)
