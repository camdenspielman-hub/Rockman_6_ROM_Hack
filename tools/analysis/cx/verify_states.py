"""Verify every Rockman CX savestate in build/research/cx/states/ and draw a contact sheet.

    python3 -I tools/analysis/cx/verify_states.py [out.png]

For each state: load, run 1 frame, screenshot, and test cheats.playable() (LEFT/RIGHT moves the player).
Menu states (title, stage_select*) are only screenshotted.  Prints one line per state.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from emu import Emu, contact
from PIL import Image
import cheats as cx

ORDER = ['title', 'opening_start', 'opening_cp1', 'opening_boss', 'stage_select', 'stage_select_allbosses']
for s in range(8):
    n = cx.STAGES[s]
    ORDER += [n] + ['%s_cp%d' % (n, k) for k in range(1, len(cx.CP_ROOMS[s]))] + [n + '_midboss', n + '_boss']
for s in range(8, 15):
    n = cx.STAGES[s]
    ORDER += [n] + ['%s_cp%d' % (n, k) for k in range(1, len(cx.CP_ROOMS[s]))] + [n + '_boss']

def main(out):
    e = Emu(os.path.join(cx.REPO, 'roms', 'cx_en.nes'))
    shots, labels = [], []
    names = [n for n in ORDER if os.path.exists(cx.state(n))]
    extra = sorted(f[:-6] for f in os.listdir(cx.STATES) if f.endswith('.state') and f[:-6] not in ORDER)
    for n in names + extra:
        e.load(cx.state(n)); e.run(1)
        menu = n.startswith(('title', 'stage_select'))
        ok = True if menu else cx.playable(e)
        shots.append(Image.fromarray(e.screen()))
        labels.append(n + ('' if ok else ' (NOT PLAYABLE)'))
        print('%-24s %-5s %s' % (n, 'menu' if menu else ok, cx.info(e)), flush=True)
    contact(shots, out, cols=8, labels=labels)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(cx.REPO, 'docs', 'research', 'cx', 'img', 'cheats_states.png'))
